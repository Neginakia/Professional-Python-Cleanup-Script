#!/usr/bin/env python3
"""
Professional System Cleanup Tool
Author: Negin Kianiamrvast
Description: Cleans temporary files and improves disk space.
Compatible: Windows, macOS, Linux
"""

import os
import shutil
import tempfile
import platform
import logging
from datetime import datetime

# ------------------ CONFIG ------------------

DRY_RUN = False  # Set True to simulate only
LOG_FILE = "cleanup.log"

# --------------------------------------------

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def get_disk_usage():
    total, used, free = shutil.disk_usage("/")
    return total, used, free

def format_size(bytes_size):
    return f"{bytes_size / (1024**3):.2f} GB"

def clean_temp_folder(path):
    """Delete files in a temp directory safely"""
    if not os.path.exists(path):
        return 0

    deleted_size = 0

    for root, dirs, files in os.walk(path):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                size = os.path.getsize(file_path)

                if not DRY_RUN:
                    os.remove(file_path)

                deleted_size += size
                logging.info(f"Deleted: {file_path}")

            except Exception as e:
                logging.warning(f"Failed to delete {file_path}: {e}")

    return deleted_size

def empty_recycle_bin_windows():
    """Empty recycle bin on Windows"""
    if platform.system() != "Windows":
        return

    try:
        import ctypes
        SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
        SHEmptyRecycleBin(None, None, 0x00000007)
        logging.info("Recycle Bin emptied.")
    except Exception as e:
        logging.warning(f"Recycle bin cleanup failed: {e}")

def main():
    print("=== Professional System Cleanup ===\n")

    total_before, used_before, free_before = get_disk_usage()

    print(f"Free space before: {format_size(free_before)}")

    system_os = platform.system()
    cleaned_bytes = 0

    # ---------- OS-specific temp paths ----------

    temp_paths = []

    if system_os == "Windows":
        temp_paths = [
            tempfile.gettempdir(),
            os.environ.get("TEMP", ""),
            r"C:\Windows\Temp",
        ]
    elif system_os == "Darwin":  # macOS
        temp_paths = [
            tempfile.gettempdir(),
            "/private/var/tmp",
        ]
    else:  # Linux
        temp_paths = [
            tempfile.gettempdir(),
            "/tmp",
        ]

    # ---------- CLEAN ----------

    for path in temp_paths:
        cleaned_bytes += clean_temp_folder(path)

    empty_recycle_bin_windows()

    total_after, used_after, free_after = get_disk_usage()

    print(f"\nFreed space: {format_size(cleaned_bytes)}")
    print(f"Free space after: {format_size(free_after)}")
    print("\nLog saved to cleanup.log")

    logging.info("Cleanup completed successfully.")

if __name__ == "__main__":
    main()
