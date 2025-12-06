#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
gifConverter - Convert video files to optimized GIF format
Uses ffmpeg for conversion and gifsicle for optimization
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


# Supported video file extensions
VIDEO_EXTENSIONS = {'.webm', '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v'}


def convert(input_file, output_file, fmt='rgb24', verbose=False):
    """
    Convert a video file to an optimized GIF.

    Args:
        input_file: Path to input video file
        output_file: Path to output GIF file
        fmt: Pixel format for ffmpeg (default: rgb24)
        verbose: Print detailed output

    Returns:
        True if conversion succeeded, False otherwise
    """
    input_path = Path(input_file)
    output_path = Path(output_file)

    # Validate input file
    if not input_path.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        return False

    if not input_path.is_file():
        print(f"Error: Input path is not a file: {input_file}", file=sys.stderr)
        return False

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"Converting {input_file} to {output_file}...")

    # Step 1: Convert video to GIF using ffmpeg
    try:
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-pix_fmt', fmt,
            '-y',  # Overwrite output file if exists
            str(output_path)
        ]

        if not verbose:
            ffmpeg_cmd.extend(['-loglevel', 'error'])

        result = subprocess.run(
            ffmpeg_cmd,
            check=True,
            capture_output=True,
            text=True
        )

        if verbose:
            print("✓ FFmpeg conversion completed")

    except subprocess.CalledProcessError as e:
        print(f"Error: FFmpeg conversion failed for {input_file}", file=sys.stderr)
        if e.stderr:
            print(f"FFmpeg error: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.", file=sys.stderr)
        return False

    # Step 2: Optimize GIF using gifsicle
    try:
        gifsicle_cmd = [
            'gifsicle',
            '-O3',  # Maximum optimization
            '-i', str(output_path),
            '-o', str(output_path)
        ]

        result = subprocess.run(
            gifsicle_cmd,
            check=True,
            capture_output=True,
            text=True
        )

        if verbose:
            print("✓ Gifsicle optimization completed")
            # Show file size
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"  Output size: {size_mb:.2f} MB")

    except subprocess.CalledProcessError as e:
        print(f"Warning: Gifsicle optimization failed for {output_file}", file=sys.stderr)
        if e.stderr and verbose:
            print(f"Gifsicle error: {e.stderr}", file=sys.stderr)
        # Don't return False - we still have a valid GIF, just not optimized
    except FileNotFoundError:
        print("Warning: gifsicle not found. GIF will not be optimized.", file=sys.stderr)
        print("Install gifsicle for smaller file sizes.", file=sys.stderr)

    return True


def is_video_file(filename):
    """Check if a file has a video extension."""
    return Path(filename).suffix.lower() in VIDEO_EXTENSIONS


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Convert video files to optimized GIF format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i video.webm -o output.gif
  %(prog)s -i video.mp4 -o output.gif -r
  %(prog)s -d ./videos
  %(prog)s -d ./videos -o ./gifs
        """
    )

    parser.add_argument('-i', '--input',
                        help='Input video file')
    parser.add_argument('-o', '--output',
                        help='Output GIF file or directory')
    parser.add_argument('-d', '--directory',
                        help='Process all video files in directory')
    parser.add_argument('-r', '--remove',
                        action='store_true',
                        help='Remove original file(s) after conversion')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Verbose output')
    parser.add_argument('--format', '--fmt',
                        default='rgb24',
                        help='Pixel format for ffmpeg (default: rgb24)')

    args = parser.parse_args()

    # Validate arguments
    if not args.input and not args.directory:
        parser.print_help()
        return 0

    if args.input and args.directory:
        print("Error: Cannot use both -i and -d options together", file=sys.stderr)
        return 2

    input_files = []
    files_to_remove = []

    # Build list of input files
    if args.directory:
        dir_path = Path(args.directory)
        if not dir_path.is_dir():
            print(f"Error: Invalid directory: {args.directory}", file=sys.stderr)
            return 2

        # Filter for video files only
        input_files = [
            str(f) for f in dir_path.iterdir()
            if f.is_file() and is_video_file(f.name)
        ]

        if not input_files:
            print(f"Warning: No video files found in {args.directory}", file=sys.stderr)
            return 0

        if args.verbose:
            print(f"Found {len(input_files)} video file(s) to process")
    else:
        input_files = [args.input]

    # Process each file
    success_count = 0
    fail_count = 0

    for input_file in input_files:
        input_path = Path(input_file)

        # Determine output path
        if args.output:
            output_arg = Path(args.output)
            if args.directory and output_arg.is_dir():
                # Output to specified directory with same name
                output_path = output_arg / f"{input_path.stem}.gif"
            elif args.directory:
                # Output directory doesn't exist, create it
                output_arg.mkdir(parents=True, exist_ok=True)
                output_path = output_arg / f"{input_path.stem}.gif"
            else:
                # Single file output
                output_path = output_arg
        else:
            # Default: same directory, change extension to .gif
            output_path = input_path.with_suffix('.gif')

        # Convert the file
        if convert(str(input_path), str(output_path), args.format, args.verbose):
            success_count += 1
            if args.remove:
                files_to_remove.append(input_path)
        else:
            fail_count += 1

    # Remove original files if requested
    if args.remove and files_to_remove:
        for file_path in files_to_remove:
            try:
                file_path.unlink()
                if args.verbose:
                    print(f"Removed original file: {file_path}")
            except Exception as e:
                print(f"Warning: Failed to remove {file_path}: {e}", file=sys.stderr)

    # Summary
    if args.verbose or fail_count > 0:
        total = success_count + fail_count
        print(f"\nCompleted: {success_count}/{total} conversions successful")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())