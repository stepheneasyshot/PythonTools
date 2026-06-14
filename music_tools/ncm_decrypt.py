"""Decrypt NetEase Cloud Music .ncm files to standard audio formats.

Uses AES-ECB decryption with NetEase's proprietary key derivation.
"""

import base64
import binascii
import json
import os
import struct

from Crypto.Cipher import AES


CORE_KEY = binascii.a2b_hex("687A4852416D736F356B496E62617857")
META_KEY = binascii.a2b_hex("2331346C6A6B5F215C5D2630553C2728")
NCM_HEADER_MAGIC = b"4354454e4644414d"


def _unpad(s):
    """Remove PKCS7 padding from a decrypted string."""
    return s[: -(s[-1] if isinstance(s[-1], int) else ord(s[-1]))]


def _build_key_box(key_data):
    """Build the RC4-style key box used for NCM content decryption."""
    key_length = len(key_data)
    key_box = bytearray(range(256))
    c = 0
    last_byte = 0
    key_offset = 0

    for i in range(256):
        swap = key_box[i]
        c = (swap + last_byte + key_data[key_offset]) & 0xFF
        key_offset += 1
        if key_offset >= key_length:
            key_offset = 0
        key_box[i] = key_box[c]
        key_box[c] = swap
        last_byte = c

    return key_box


def dump_ncm_file(file_path, output_dir=None):
    """Decrypt a single .ncm file and write the decoded audio to disk.

    Args:
        file_path: Path to the .ncm file.
        output_dir: Optional output directory. Defaults to the same directory as the input.

    Returns:
        Name of the output audio file, or None on failure.

    Raises:
        ValueError: If the file header is invalid.
        FileNotFoundError: If the input file does not exist.
    """
    with open(file_path, "rb") as f:
        header = f.read(8)
        if binascii.b2a_hex(header) != NCM_HEADER_MAGIC:
            raise ValueError(f"Invalid NCM file header: {file_path}")

        f.seek(2, 1)
        key_data = f.read(struct.unpack("<I", f.read(4))[0])
        key_data = bytes(b ^ 0x64 for b in bytearray(key_data))

        cryptor = AES.new(CORE_KEY, AES.MODE_ECB)
        key_data = _unpad(cryptor.decrypt(key_data))[17:]

        key_box = _build_key_box(bytearray(key_data))

        meta_data = f.read(struct.unpack("<I", f.read(4))[0])
        meta_data = bytes(b ^ 0x63 for b in bytearray(meta_data))
        meta_data = base64.b64decode(meta_data[22:])

        cryptor = AES.new(META_KEY, AES.MODE_ECB)
        meta_data = json.loads(_unpad(cryptor.decrypt(meta_data)).decode("utf-8")[6:])

        f.read(4)  # crc32
        f.seek(5, 1)
        f.read(struct.unpack("<I", f.read(4))[0])  # image data

        output_name = os.path.splitext(os.path.basename(file_path))[0] + "." + meta_data["format"]
        output_dir = output_dir or os.path.dirname(file_path)
        output_path = os.path.join(output_dir, output_name)

        with open(output_path, "wb") as out:
            while True:
                chunk = bytearray(f.read(0x8000))
                if not chunk:
                    break
                for i in range(1, len(chunk) + 1):
                    j = i & 0xFF
                    chunk[i - 1] ^= key_box[(key_box[j] + key_box[(key_box[j] + j) & 0xFF]) & 0xFF]
                out.write(chunk)

    print(f"Decrypted: {file_path} -> {output_path}")
    return output_name


def get_all_files(directory):
    """Recursively list all files in a directory.

    Args:
        directory: Root directory to scan.

    Returns:
        List of full file paths.
    """
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def decrypt_ncm(directory_path):
    """Decrypt all .ncm files in a directory.

    Args:
        directory_path: Directory containing .ncm files.
    """
    all_files = get_all_files(directory_path)
    for file_path in all_files:
        if file_path.lower().endswith(".ncm"):
            print(f"{file_path}: processing...")
            try:
                dump_ncm_file(file_path, output_dir=directory_path)
                print(f"{file_path}: done")
            except Exception as e:
                print(f"{file_path}: failed - {e}")


if __name__ == "__main__":
    decrypt_ncm("/path/to/ncm/files")