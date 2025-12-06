# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-12-06

### Added
- Python 3 shebang and full Python 3 compatibility
- Comprehensive docstrings for all functions
- Input file validation (existence and type checking)
- Support for multiple video formats (.webm, .mp4, .avi, .mov, .mkv, .flv, .wmv, .m4v)
- Video file filtering when processing directories
- Verbose mode (`-v` flag) with progress tracking and file size reporting
- Long-form argument names (e.g., `--input`, `--output`, `--directory`)
- Automatic output directory creation
- Success/failure tracking and summary reporting
- Proper exit codes (0 for success, 1 for failures, 2 for invalid arguments)
- requirements.txt with dependency installation instructions
- Enhanced README with comprehensive usage examples
- This CHANGELOG to track project changes

### Fixed
- **Critical:** Fixed `-r` (remove) flag not being parsed in getopt string
- **Critical:** Fixed crash when using `-r` flag (attempted to remove list instead of files)
- **Critical:** Fixed directory processing not including directory path in filenames
- **Critical:** Fixed directory processing attempting to convert non-video files
- Fixed missing error messages when ffmpeg/gifsicle fail
- Fixed typo in README ("diretory" → "directory")
- Fixed ffmpeg commands being too verbose in normal mode
- Fixed no validation of subprocess return codes

### Changed
- Migrated from Python 2 to Python 3
- Replaced `getopt` with `argparse` for better CLI experience
- Replaced bare `except:` with specific exception handling
- Replaced `subprocess.Popen` with `subprocess.run` for better error handling
- Changed to use `pathlib.Path` for more robust path handling
- Improved error messages with specific details and stderr output
- Only remove original files after successful conversion (safety improvement)
- Gifsicle failures now show warnings instead of silent failures
- Made gifsicle optional (warns if not installed but continues)

### Improved
- More descriptive variable names throughout
- Better code organization with separate validation and processing steps
- Comprehensive help text with usage examples
- Better handling of edge cases (missing directories, no video files, etc.)
- More professional output formatting

## [0.1.0] - Initial Release

### Original Features
- Basic video to GIF conversion using ffmpeg
- GIF optimization using gifsicle
- Single file conversion with `-i` and `-o` flags
- Directory processing with `-d` flag
- Python 2 implementation
