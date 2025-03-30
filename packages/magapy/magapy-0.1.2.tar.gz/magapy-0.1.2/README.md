# Magapy - Music Library Management Tool

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A comprehensive Python tool for managing music libraries, with a focus on high-quality audio files. Magapy helps you organize, deduplicate, and maintain a well-structured music collection.

## Features

- **Multi-source Downloads**: Download tracks from Qobuz and Tidal
- **Quality Analysis**: Automatically detect and categorize audio quality (HiRes, MQA, Standard)
- **Duplicate Detection**: Find and manage duplicate tracks based on audio content
- **Library Organization**: Keep your music collection tidy and well-structured
- **Beets Integration**: Seamless integration with the beets music library manager
- **Metadata Management**: Extract and update audio file metadata
- **Audio file analysis**
- **Integration with MusicBrainz and other music databases**
- **Support for various audio formats**

## Installation

### From PyPI

```bash
pip install magapy
```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/geooooooorges/magapy.git
   cd magapy
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

## Configuration

### Required Third-Party Tools

Magapy depends on external tools for downloading content:

#### 1. qobuz-dl (for Qobuz downloads)

Install qobuz-dl:
```bash
pip install qobuz-dl
```

Configure qobuz-dl with your credentials:
```bash
qobuz-dl config init
# Follow the interactive prompts to enter your Qobuz credentials
```

#### 2. tidal-wave through "UVX" (for Tidal downloads)

Install UVX for Tidal downloads:
```bash
pip install uvx
```

Configure Tidal authentication:
```bash
uvx tidal-wave auth
# Follow the interactive prompts to log in to Tidal
```

### Magapy Configuration

Magapy offers flexible configuration through environment variables, config files, or command-line options:

### 1. Environment Variables

Set environment variables for quick configuration:

```bash
# Set core directories
export MUSIC_DIR="/path/to/your/music"
export DOWNLOAD_DIR="/path/to/downloads"
export REVIEW_DIR="/path/to/review/directory"

# Set API keys
export ACOUSTID_API_KEY="your-acoustid-api-key"
export MUSICBRAINZ_API_KEY="your-musicbrainz-api-key"
```

### 2. Configuration File

Create a configuration file at one of these locations:
- `./magapy.ini` (current directory)
- `~/.config/magapy/config.ini` (user config directory)
- `/etc/magapy/config.ini` (system-wide)

Generate an example configuration:

```bash
magapy config --create-example
```

Example config file structure:

```ini
[paths]
music_dir = /path/to/your/music/library
download_dir = /path/to/downloads
review_dir = /path/to/review/directory

[settings]
dry_run = false
detailed_logging = true
use_beets = false

[api_keys]
acoustid = your_acoustid_api_key
musicbrainz = your_musicbrainz_api_key
```

### 3. Command Line Options

Override configuration with command-line options:

```bash
magapy download "https://play.qobuz.com/track/12345678" --download-dir ~/Downloads/NewMusic
```

## Usage

### Command Line Interface

Magapy provides a simple command line interface:

```bash
# Download a track
magapy download "https://play.qobuz.com/track/12345678" 

# Using shorter alias
magapy d "https://play.qobuz.com/track/12345678"

# Review library for duplicates
magapy review --music-dir /path/to/music

# Update the track database
magapy update

# Analyze library and generate statistics
magapy analyze --output stats.json --format json

# Extract cover art from files
magapy cover /path/to/audio.flac --output-dir /path/to/covers --resize 500
```

### Direct URL Handling

For convenience, you can also download directly by providing a URL:

```bash
magapy "https://play.qobuz.com/track/12345678"
```

### Beets Integration

Magapy integrates with Beets for advanced library management:

```bash
# Process downloads with beets
magapy download "https://play.qobuz.com/track/12345678" --use-beets --beets-move
```

### Basic usage

```python
import magapy

# Analyze your music library
magapy.analyze_library("path/to/music/library")
```

### Command line usage

```bash
magapy-cli analyze "path/to/music/library"
```

## Quality Ranking System

Magapy categorizes audio files by quality:

1. **HiRes** (Rank 3): Sample rate ≥ 96kHz or bitrate ≥ 2500kbps
2. **MQA** (Rank 2): Contains MQA encoding
3. **Standard** (Rank 1): Standard CD quality or less

## Troubleshooting

### 1. Download Issues

- **Check Credentials**: Ensure your Qobuz and Tidal credentials are correct.
- **Verify Links**: Make sure the Qobuz/Tidal links are valid and accessible.
- **Network Connection**: Check your internet connection.
- **Rate Limiting**: If downloads fail intermittently, you may be hitting rate limits. Try again later.

### 2. Beets Integration

- **Configuration**: Ensure your Beets configuration is correct (check `~/.config/beets/config.yaml`).
- **Plugin Issues**: If certain Beets plugins are not working, make sure they are installed and configured correctly.
- **Library Path**: Verify that the `directory:` setting in your Beets config points to the correct music library path.

### 3. General Issues

- **Permissions**: Ensure you have the necessary permissions to read/write files in your music and download directories.
- **Dependencies**: Make sure all required Python packages are installed (`pip install -r requirements.txt`).
- **Logging**: Check the log files for detailed error messages.

## Requirements

- Python 3.7+
- Dependencies listed in requirements.txt

## Development

### Testing

Run tests with pytest:

```bash
pytest
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Structure
```
