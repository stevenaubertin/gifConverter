# gifConverter

Convert video files to optimized GIF format using ffmpeg and gifsicle.

## Features

- ✓ Convert multiple video formats (webm, mp4, avi, mov, mkv, flv, wmv, m4v) to GIF
- ✓ Automatic optimization using gifsicle for smaller file sizes
- ✓ Batch process entire directories
- ✓ Option to remove original files after conversion
- ✓ Verbose mode for detailed progress tracking
- ✓ Proper error handling and validation
- ✓ Python 3 compatible

## Requirements

This tool requires the following external dependencies:

- [ffmpeg](https://www.ffmpeg.org/) - For video to GIF conversion
- [gifsicle](https://www.lcdf.org/gifsicle/) - For GIF optimization (optional but recommended)
- Python 3.6 or higher

### Installation of Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg gifsicle
```

**macOS (with Homebrew):**
```bash
brew install ffmpeg gifsicle
```

**Windows (with Chocolatey):**
```bash
choco install ffmpeg gifsicle
```

## Usage

### Basic Usage

Convert a single video file:
```bash
python3 gifConverter.py -i inputfile.webm -o outputfile.gif
```

### Process a Directory

Convert all video files in a directory:
```bash
python3 gifConverter.py -d ./videos
```

Convert all videos and save GIFs to a specific output directory:
```bash
python3 gifConverter.py -d ./videos -o ./gifs
```

### Advanced Options

Remove original files after conversion:
```bash
python3 gifConverter.py -i video.mp4 -o output.gif -r
```

Verbose output with progress information:
```bash
python3 gifConverter.py -i video.mp4 -o output.gif -v
```

Custom pixel format:
```bash
python3 gifConverter.py -i video.mp4 -o output.gif --format rgb24
```

### All Options

```
  -h, --help            Show help message and exit
  -i INPUT, --input INPUT
                        Input video file
  -o OUTPUT, --output OUTPUT
                        Output GIF file or directory
  -d DIRECTORY, --directory DIRECTORY
                        Process all video files in directory
  -r, --remove          Remove original file(s) after conversion
  -v, --verbose         Verbose output
  --format FORMAT       Pixel format for ffmpeg (default: rgb24)
```

## Examples

1. Convert a single WebM file:
   ```bash
   python3 gifConverter.py -i video.webm -o output.gif
   ```

2. Convert and delete the original:
   ```bash
   python3 gifConverter.py -i video.mp4 -r
   ```

3. Batch convert all videos in a folder with verbose output:
   ```bash
   python3 gifConverter.py -d ./my_videos -v
   ```

4. Convert directory and save to different location:
   ```bash
   python3 gifConverter.py -d ./source_videos -o ./output_gifs
   ```

## Improvements from Original Version

This improved version includes:

- **Python 3 compatibility** - Updated from Python 2 to Python 3
- **Fixed critical bugs** - Fixed `-r` flag parsing and directory processing
- **Better error handling** - Proper exception handling with user-friendly error messages
- **Input validation** - Validates files exist and are correct type before processing
- **Path handling** - Correctly handles absolute and relative paths
- **File filtering** - Only processes actual video files from directories
- **Progress tracking** - Verbose mode shows conversion progress and file sizes
- **Better CLI** - Uses argparse for better help and argument handling
- **Documentation** - Complete docstrings and improved README
- **Return codes** - Proper exit codes for success/failure
- **Safety** - Only removes original files after successful conversion
