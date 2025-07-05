#!/usr/bin/env python3
"""
N0va Desktop Wallpaper Extractor
==================================

A tool to extract wallpapers from N0va Desktop's cache files (.ndf format)
and convert them back to standard PNG images.

Usage:
    python n0va_extractor.py [cache_path] [output_path]

Author: Open Source Community
License: MIT
"""

import os
import sys
import shutil
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Color:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Print the application banner"""
    banner = f"""
{Color.HEADER}╔══════════════════════════════════════════════════════════════╗
║                   N0va Desktop Wallpaper Extractor          ║
║                          v1.0.0                             ║
║                                                              ║
║   Extract wallpapers from N0va Desktop cache files          ║
║   Convert .ndf files back to standard PNG images            ║
╚══════════════════════════════════════════════════════════════╝{Color.ENDC}
"""
    print(banner)

def get_file_hash(file_path: Path) -> str:
    """Generate MD5 hash of a file for duplicate detection"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logger.error(f"Error hashing file {file_path}: {e}")
        return ""

def verify_image_format(file_path: Path) -> Optional[str]:
    """
    Verify if a file is a valid image and return its format
    
    Returns:
        str: Image format ('PNG', 'JPEG', 'WebP', etc.) or None if not an image
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(16)
            
        # Check for PNG signature
        if header.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'PNG'
        
        # Check for JPEG signature
        if header.startswith(b'\xff\xd8\xff'):
            return 'JPEG'
        
        # Check for WebP signature
        if header.startswith(b'RIFF') and header[8:12] == b'WEBP':
            return 'WebP'
        
        # Check for GIF signature
        if header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
            return 'GIF'
        
        # Check for BMP signature
        if header.startswith(b'BM'):
            return 'BMP'
        
        return None
        
    except Exception as e:
        logger.error(f"Error verifying file format for {file_path}: {e}")
        return None

def find_ndf_files(cache_path: Path) -> List[Path]:
    """
    Find all .ndf files in the cache directory
    
    Args:
        cache_path: Path to the N0va Desktop cache directory
        
    Returns:
        List of Path objects for .ndf files
    """
    ndf_files = []
    
    if not cache_path.exists():
        logger.error(f"Cache directory does not exist: {cache_path}")
        return ndf_files
    
    # Look for .ndf files recursively
    for file_path in cache_path.rglob("*.ndf"):
        if file_path.is_file():
            ndf_files.append(file_path)
    
    # Also check for .ndf_tmp files (incomplete downloads)
    for file_path in cache_path.rglob("*.ndf_tmp"):
        if file_path.is_file() and file_path.stat().st_size > 0:
            ndf_files.append(file_path)
    
    return sorted(ndf_files)

def extract_wallpapers(cache_path: Path, output_path: Path, skip_duplicates: bool = True, min_size_mb: float = 1.0) -> Tuple[int, int, int]:
    """
    Extract wallpapers from .ndf files to the output directory
    
    Args:
        cache_path: Path to N0va Desktop cache directory
        output_path: Path to output directory for extracted images
        skip_duplicates: Whether to skip duplicate files
        min_size_mb: Minimum file size in MB to avoid thumbnails
        
    Returns:
        Tuple of (successful_extractions, skipped_files, failed_extractions)
    """
    print(f"{Color.OKBLUE}🔍 Scanning for .ndf files...{Color.ENDC}")
    
    ndf_files = find_ndf_files(cache_path)
    
    if not ndf_files:
        print(f"{Color.WARNING}❌ No .ndf files found in {cache_path}{Color.ENDC}")
        return 0, 0, 0
    
    print(f"{Color.OKGREEN}✓ Found {len(ndf_files)} .ndf files{Color.ENDC}")
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Track statistics
    successful = 0
    skipped = 0
    failed = 0
    file_hashes = set()
    
    print(f"{Color.OKBLUE}🚀 Starting extraction...{Color.ENDC}")
    
    for i, ndf_file in enumerate(ndf_files, 1):
        try:
            # Progress indicator
            progress = f"[{i}/{len(ndf_files)}]"
            print(f"{Color.OKCYAN}{progress} Processing: {ndf_file.name}{Color.ENDC}")
            
            # Verify it's an image
            image_format = verify_image_format(ndf_file)
            if not image_format:
                print(f"{Color.WARNING}  ⚠️  Skipping (not a valid image): {ndf_file.name}{Color.ENDC}")
                skipped += 1
                continue
            
            # Check file size to skip thumbnails
            file_size = ndf_file.stat().st_size
            size_mb = file_size / (1024 * 1024)
            if size_mb < min_size_mb:
                print(f"{Color.WARNING}  ⚠️  Skipping (too small - {size_mb:.1f}MB): {ndf_file.name}{Color.ENDC}")
                skipped += 1
                continue
            
            # Check for duplicates if requested
            if skip_duplicates:
                file_hash = get_file_hash(ndf_file)
                if file_hash in file_hashes:
                    print(f"{Color.WARNING}  ⚠️  Skipping (duplicate): {ndf_file.name}{Color.ENDC}")
                    skipped += 1
                    continue
                file_hashes.add(file_hash)
            
            # Generate output filename
            base_name = ndf_file.stem
            extension = '.png' if image_format == 'PNG' else f'.{image_format.lower()}'
            output_file = output_path / f"{base_name}{extension}"
            
            # Handle filename conflicts
            counter = 1
            while output_file.exists():
                output_file = output_path / f"{base_name}_{counter}{extension}"
                counter += 1
            
            # Copy the file
            shutil.copy2(ndf_file, output_file)
            
            print(f"{Color.OKGREEN}  ✓ Extracted: {output_file.name} ({size_mb:.1f}MB, {image_format}){Color.ENDC}")
            successful += 1
            
        except Exception as e:
            print(f"{Color.FAIL}  ❌ Error processing {ndf_file.name}: {e}{Color.ENDC}")
            failed += 1
            logger.error(f"Failed to process {ndf_file}: {e}")
    
    return successful, skipped, failed

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Extract wallpapers from N0va Desktop cache files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python n0va_extractor.py
  python n0va_extractor.py "C:\\Program Files\\N0vaDesktop\\N0vaDesktopCache"
  python n0va_extractor.py "C:\\Program Files\\N0vaDesktop\\N0vaDesktopCache" "./extracted_wallpapers"
  python n0va_extractor.py --min-size 2.0 --verbose
        """
    )
    
    parser.add_argument(
        'cache_path', 
        nargs='?',
        default=r"C:\Program Files\N0vaDesktop\N0vaDesktopCache",
        help='Path to N0va Desktop cache directory (default: C:\\Program Files\\N0vaDesktop\\N0vaDesktopCache)'
    )
    
    parser.add_argument(
        'output_path',
        nargs='?',
        default='./extracted_wallpapers',
        help='Output directory for extracted wallpapers (default: ./extracted_wallpapers)'
    )
    
    parser.add_argument(
        '--allow-duplicates',
        action='store_true',
        help='Allow duplicate files (don\'t skip based on file hash)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--min-size',
        type=float,
        default=1.0,
        help='Minimum file size in MB (default: 1.0MB to skip thumbnails)'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print_banner()
    
    cache_path = Path(args.cache_path)
    output_path = Path(args.output_path)
    
    print(f"{Color.BOLD}Configuration:{Color.ENDC}")
    print(f"  Cache Path: {cache_path}")
    print(f"  Output Path: {output_path}")
    print(f"  Skip Duplicates: {not args.allow_duplicates}")
    print(f"  Minimum Size: {args.min_size}MB (skip thumbnails)")
    print()
    
    # Validate cache path
    if not cache_path.exists():
        print(f"{Color.FAIL}❌ Error: Cache directory does not exist: {cache_path}{Color.ENDC}")
        print(f"{Color.WARNING}💡 Make sure N0va Desktop is installed or specify the correct cache path{Color.ENDC}")
        sys.exit(1)
    
    # Start extraction
    start_time = datetime.now()
    
    try:
        successful, skipped, failed = extract_wallpapers(
            cache_path, 
            output_path, 
            skip_duplicates=not args.allow_duplicates,
            min_size_mb=args.min_size
        )
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Print summary
        print(f"\n{Color.BOLD}🎉 Extraction Complete!{Color.ENDC}")
        print(f"  ✅ Successfully extracted: {Color.OKGREEN}{successful}{Color.ENDC} wallpapers")
        print(f"  ⏭️  Skipped: {Color.WARNING}{skipped}{Color.ENDC} files")
        print(f"  ❌ Failed: {Color.FAIL}{failed}{Color.ENDC} files")
        print(f"  ⏱️  Duration: {duration.total_seconds():.1f} seconds")
        print(f"  📁 Output location: {Color.OKCYAN}{output_path.absolute()}{Color.ENDC}")
        
        if successful > 0:
            print(f"\n{Color.OKGREEN}🎨 Your N0va Desktop wallpapers have been successfully extracted!{Color.ENDC}")
            print(f"{Color.OKBLUE}💡 You can now use these wallpapers with any wallpaper manager or set them manually.{Color.ENDC}")
        
    except KeyboardInterrupt:
        print(f"\n{Color.WARNING}⚠️ Extraction interrupted by user{Color.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Color.FAIL}❌ An unexpected error occurred: {e}{Color.ENDC}")
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 