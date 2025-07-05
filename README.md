# N0va Desktop Wallpaper Extractor

**🎨 Extract your favorite wallpapers from N0va Desktop's cache files!**

## ✨ Features

- **🔍 Automatic Detection**: Finds all cached wallpapers in N0va Desktop's storage
- **🖼️ Format Recognition**: Identifies and preserves original image formats (PNG, JPEG, WebP, etc.)
- **🚀 Batch Processing**: Extracts multiple wallpapers simultaneously with progress tracking
- **🔄 Duplicate Handling**: Intelligently skips duplicate files to save space
- **🎯 Cross-Platform**: Works on Windows, macOS, and Linux
- **📊 Progress Tracking**: Real-time progress with colored terminal output
- **🛡️ Error Handling**: Robust error handling for corrupted files and permissions
- **📝 Detailed Logging**: Comprehensive logging for troubleshooting

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- N0va Desktop previously installed (cache files present)

### Installation

1. **Clone or Download**
   ```bash
   git clone https://github.com/your-username/n0va-extractor.git
   cd n0va-extractor
   ```

2. **No additional dependencies required!** The script uses only Python standard library.

### Basic Usage

**Windows:**
```bash
python n0va_extractor.py
```

**macOS/Linux:**
```bash
python3 n0va_extractor.py
```

This will:
- Look for cache files in the default location: `C:\Program Files\N0vaDesktop\N0vaDesktopCache`
- Extract wallpapers to `./extracted_wallpapers/`
- Skip duplicate files automatically

## Edit ^ accordingly if needed.

## 📖 Usage Examples

### Extract from default location
```bash
python n0va_extractor.py
```

### Specify custom cache path
```bash
python n0va_extractor.py "C:\CustomPath\N0vaDesktopCache"
```

### Specify custom output directory
```bash
python n0va_extractor.py "C:\Program Files\N0vaDesktop\N0vaDesktopCache" "./my_wallpapers"
```

### Allow duplicate files
```bash
python n0va_extractor.py --allow-duplicates
```

### Enable verbose logging
```bash
python n0va_extractor.py --verbose
```

## 🔧 Command Line Options

```
usage: n0va_extractor.py [-h] [--allow-duplicates] [--verbose] [cache_path] [output_path]

Extract wallpapers from N0va Desktop cache files

positional arguments:
  cache_path         Path to N0va Desktop cache directory 
                     (default: C:\Program Files\N0vaDesktop\N0vaDesktopCache)
  output_path        Output directory for extracted wallpapers 
                     (default: ./extracted_wallpapers)

optional arguments:
  -h, --help         show this help message and exit
  --allow-duplicates Allow duplicate files (don't skip based on file hash)
  --verbose          Enable verbose logging
```

## 🗂️ Default Cache Locations

### Windows
```
C:\Program Files\N0vaDesktop\N0vaDesktopCache\game\
```

### macOS
```
/Applications/N0vaDesktop.app/Contents/Resources/cache/
```

### Linux
```
~/.local/share/N0vaDesktop/cache/
```

## 🔍 How It Works

1. **Discovery**: Scans the cache directory for `.ndf` files
2. **Verification**: Checks file magic bytes to identify image formats
3. **Deduplication**: Uses MD5 hashing to detect and skip duplicate files
4. **Extraction**: Copies files with proper extensions (`.png`, `.jpg`, etc.)
5. **Organization**: Creates organized output directory with proper naming

## 🎯 File Format Detection

The tool automatically detects various image formats:

- **PNG**: `\x89PNG\r\n\x1a\n`
- **JPEG**: `\xff\xd8\xff`
- **WebP**: `RIFF...WEBP`
- **GIF**: `GIF87a` or `GIF89a`
- **BMP**: `BM`

## 📊 Output

The tool provides detailed progress information:

```
╔══════════════════════════════════════════════════════════════╗
║                   N0va Desktop Wallpaper Extractor          ║
║                          v1.0.0                             ║
║                                                              ║
║   Extract wallpapers from N0va Desktop cache files          ║
║   Convert .ndf files back to standard PNG images            ║
╚══════════════════════════════════════════════════════════════╝

Configuration:
  Cache Path: C:\Program Files\N0vaDesktop\N0vaDesktopCache
  Output Path: ./extracted_wallpapers
  Skip Duplicates: True

🔍 Scanning for .ndf files...
✓ Found 127 .ndf files
🚀 Starting extraction...
[1/127] Processing: 1690886536185_483.ndf
  ✓ Extracted: 1690886536185_483.png (0.1MB, PNG)
[2/127] Processing: 1696848238106_665.ndf
  ✓ Extracted: 1696848238106_665.png (0.2MB, PNG)
...

🎉 Extraction Complete!
  ✅ Successfully extracted: 125 wallpapers
  ⏭️  Skipped: 2 files
  ❌ Failed: 0 files
  ⏱️  Duration: 12.3 seconds
  📁 Output location: /path/to/extracted_wallpapers
```

## 🛠️ Troubleshooting

### Common Issues

**"Cache directory does not exist"**
- Make sure N0va Desktop was previously installed
- Check if the cache path is correct
- Try running as administrator on Windows

**"Permission denied"**
- Run the terminal as administrator (Windows)
- Use `sudo` on macOS/Linux if needed
- Check file permissions in the cache directory

**"No .ndf files found"**
- Verify N0va Desktop was used and downloaded wallpapers
- Check subdirectories like `game/` folder
- Try different cache locations

### Enable Verbose Logging

```bash
python n0va_extractor.py --verbose
```

This will show detailed information about file processing and any errors.

## 🎨 Tips for Students & Developers

### Learning Opportunities

1. **File Format Analysis**: Learn about magic bytes and file signatures
2. **Binary Data Handling**: Understand how to work with binary files in Python
3. **Error Handling**: See robust error handling patterns
4. **CLI Design**: Learn how to create user-friendly command-line interfaces
5. **Progress Tracking**: Implement progress indicators for long-running operations

### Code Architecture

The tool follows clean code principles:
- **Modular Functions**: Each function has a single responsibility
- **Type Hints**: Full type annotation for better code clarity
- **Error Handling**: Comprehensive exception handling
- **Documentation**: Detailed docstrings and comments
- **User Experience**: Colored output and progress tracking

### Extending the Tool

You can extend this tool by:
- Adding support for more image formats
- Implementing GUI interface
- Adding thumbnail generation
- Creating automated wallpaper setting
- Adding metadata extraction

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🙏 Acknowledgments

- **HoYoverse** for creating the beautiful N0va Desktop wallpapers
- **Python** for excellent tools

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Enable verbose logging to get more details
3. Create an issue on GitHub with:
   - Your operating system
   - Python version
   - Full error message
   - Cache directory path

---
