"""Monitor a directory and delete .scr files (e.g., annoying corporate screensavers).

Runs continuously, checking every N seconds.
"""

import logging
import os
import signal
import sys
import time


def delete_scr_files(target_dir):
    """Delete all .scr files in the specified directory.

    Args:
        target_dir: Directory to scan for .scr files.

    Returns:
        Number of files deleted.
    """
    deleted = 0
    try:
        for filename in os.listdir(target_dir):
            if filename.lower().endswith(".scr"):
                file_path = os.path.join(target_dir, filename)
                try:
                    os.remove(file_path)
                    logging.info("Deleted: %s", file_path)
                    deleted += 1
                except Exception as e:
                    logging.error("Failed to delete %s: %s", file_path, e)
        if deleted > 0:
            logging.info("Deleted %d .scr file(s) this cycle", deleted)
    except Exception as e:
        logging.error("Directory scan error: %s", e)
    return deleted


def start_monitoring(target_dir, interval=10):
    """Start continuous monitoring and deletion of .scr files.

    Args:
        target_dir: Directory to monitor.
        interval: Seconds between scans. Defaults to 10.

    Press Ctrl+C to stop.
    """
    logging.info("Started monitoring: %s", target_dir)
    running = True

    def _signal_handler(sig, frame):
        nonlocal running
        logging.info("Received interrupt signal, stopping...")
        running = False

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    while running:
        delete_scr_files(target_dir)
        time.sleep(interval)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    start_monitoring("D:\\")