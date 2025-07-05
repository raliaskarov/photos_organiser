#!/usr/bin/env python3
"""
Script to copy photos and videos from a source directory into a target directory,
organizing them into subdirectories by year and month.

Dependencies:
  - Python 3.x
  - Pillow (for reading EXIF data): pip install Pillow

Usage:
  python organize_photos.py --source "path/to/source" --dest "path/to/destination"
"""
import os
import sys
import argparse
import shutil
from datetime import datetime

try:
    from PIL import Image, ExifTags
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Supported file extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp', '.heic'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.mts', '.wmv'}

# EXIF tag for original date/time
EXIF_DATETIME_TAG = 'DateTimeOriginal'


def get_creation_date(path):
    """
    Get the creation date for a file.
    For images, attempt to read EXIF DateTimeOriginal.
    Otherwise, fallback to file modification time.
    """
    # Try EXIF for images
    ext = os.path.splitext(path)[1].lower()
    if PIL_AVAILABLE and ext in IMAGE_EXTENSIONS:
        try:
            img = Image.open(path)
            exif_data = img._getexif() or {}
            for tag, value in exif_data.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                if decoded == EXIF_DATETIME_TAG:
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        except Exception:
            pass

    # Fallback: file modification time
    mod_time = os.path.getmtime(path)
    return datetime.fromtimestamp(mod_time)


def organize_files(source_dir, dest_dir, move_files=False):
    """
    Walk through source_dir, find photos/videos, and copy (or move) into dest_dir organized by year/month.
    """
    if not os.path.isdir(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        sys.exit(1)
    os.makedirs(dest_dir, exist_ok=True)

    for root, _, files in os.walk(source_dir):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in IMAGE_EXTENSIONS or ext in VIDEO_EXTENSIONS:
                src_path = os.path.join(root, filename)
                date = get_creation_date(src_path)
                year = date.strftime('%Y')
                month = date.strftime('%m')
                target_folder = os.path.join(dest_dir, year, month)
                os.makedirs(target_folder, exist_ok=True)

                dest_path = os.path.join(target_folder, filename)
                # Handle filename collisions
                base, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(target_folder, f"{base}_{counter}{extension}")
                    counter += 1

                if move_files:
                    shutil.move(src_path, dest_path)
                else:
                    shutil.copy2(src_path, dest_path)
                print(f"{'Moved' if move_files else 'Copied'}: {src_path} -> {dest_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Organize photos and videos by year and month."
    )
    parser.add_argument(
        '--source', '-s', required=True,
        help="Source directory containing photos and videos"
    )
    parser.add_argument(
        '--dest', '-d', required=True,
        help="Destination base directory for organized files"
    )
    parser.add_argument(
        '--move', action='store_true',
        help="Move files instead of copying"
    )

    args = parser.parse_args()
    organize_files(args.source, args.dest, move_files=args.move)
