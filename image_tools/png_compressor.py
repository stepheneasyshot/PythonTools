"""Compress PNG images with color quantization (TinyPNG-style).

Reduces file size by converting truecolor PNGs to indexed palette mode,
typically achieving 50-80% size reduction with minimal visual difference.
"""

import os
from PIL import Image


def _get_size(path):
    return os.path.getsize(path)


def _format_size(size_bytes):
    for unit in ("B", "KB", "MB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} GB"


_DITHER_MAP = {
    "none": Image.Dither.NONE,
    "floyd-steinberg": Image.Dither.FLOYDSTEINBERG,
    "ordered": Image.Dither.ORDERED,
}


def compress_png(source_path, target_path=None, colors=256, dither="none"):
    """Compress one or more PNG images using color quantization.

    Converts truecolor PNG to indexed palette mode, similar to TinyPNG.
    Supports single files and batch directory processing.

    Args:
        source_path: Path to a PNG file or a directory containing PNG files.
        target_path: Optional output path (file or directory). If omitted,
            appends '_compressed' to the filename.
        colors: Max colors to retain (2-256). Fewer colors = smaller file.
            Default 256 is a good balance of quality and size.
        dither: Dithering mode: "none" (default), "floyd-steinberg",
            or "ordered".

    Returns:
        List of (original_path, output_path, original_size, compressed_size,
        ratio_pct) tuples for each processed file.
    """
    results = []

    if os.path.isfile(source_path):
        files = [source_path]
        target_is_file = target_path is not None and not os.path.isdir(target_path)
        if target_path and target_is_file:
            out_dir = os.path.dirname(target_path) or "."
            targets = [target_path]
        else:
            out_dir = target_path
            targets = [None]
    else:
        files = [
            os.path.join(source_path, f)
            for f in os.listdir(source_path)
            if f.lower().endswith(".png")
        ]
        if not files:
            print(f"No PNG files found in: {source_path}")
            return results
        out_dir = target_path
        targets = [None] * len(files)

    quantize_dither = _DITHER_MAP.get(dither, Image.Dither.NONE)
    color_count = max(2, min(colors, 256))

    for i, file_path in enumerate(files):
        try:
            orig_size = _get_size(file_path)

            with Image.open(file_path) as img:
                # Strip metadata by copying pixel data
                cleaned = Image.new(img.mode, img.size)
                cleaned.putdata(list(img.getdata()))

                mode = cleaned.mode
                if mode in ("RGBA", "RGB", "LA"):
                    quantized = _quantize(cleaned, color_count, quantize_dither)
                elif mode == "P":
                    # Already palette-based; convert to RGBA then quantize
                    quantized = _quantize(
                        cleaned.convert("RGBA"), color_count, quantize_dither
                    )
                else:
                    # L, CMYK, etc. — save as-is with optimize
                    save_path = targets[i] or _default_target(file_path, out_dir)
                    cleaned.save(save_path, "PNG", optimize=True)
                    compressed_size = _get_size(save_path)
                    ratio = (1 - compressed_size / orig_size) * 100
                    _log_result(file_path, orig_size, compressed_size, ratio)
                    results.append(
                        (file_path, save_path, orig_size, compressed_size, ratio)
                    )
                    continue

                save_path = targets[i] or _default_target(file_path, out_dir)
                quantized.save(save_path, "PNG", optimize=True)

            compressed_size = _get_size(save_path)
            ratio = (1 - compressed_size / orig_size) * 100
            _log_result(file_path, orig_size, compressed_size, ratio)
            results.append((file_path, save_path, orig_size, compressed_size, ratio))
        except Exception as e:
            print(f"Error compressing {file_path}: {e}")

    return results


def _quantize(image, colors, dither):
    """Quantize image using the best available method.

    Tries libimagequant first (same library as pngquant/TinyPNG), falls
    back to FastOctree which handles both RGB and RGBA natively.
    """
    try:
        return image.quantize(
            colors=colors,
            method=Image.Quantize.LIBIMAGEQUANT,
            dither=dither,
        )
    except (ValueError, OSError):
        return image.quantize(
            colors=colors,
            method=Image.Quantize.FASTOCTREE,
            dither=dither,
        )


def _log_result(file_path, orig_size, compressed_size, ratio):
    print(
        f"Compressed: {os.path.basename(file_path)}  "
        f"{_format_size(orig_size)} → {_format_size(compressed_size)}  "
        f"({ratio:.1f}% smaller)"
    )


def _default_target(file_path, out_dir):
    base, ext = os.path.splitext(os.path.basename(file_path))
    target_dir = out_dir if out_dir else os.path.dirname(file_path)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    return os.path.join(target_dir, f"{base}_compressed{ext}")


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    files = filedialog.askopenfilenames(
        title="Select PNG images to compress",
        filetypes=[("PNG images", "*.png"), ("All files", "*.*")],
    )

    if not files:
        print("No files selected.")
    else:
        for picked in files:
            compress_png(picked)
