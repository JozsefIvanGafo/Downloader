# Downloader

A simple and efficient utility for downloading content from various websites including YouTube and other platforms using yt-dlp.

## Features

- Download videos from YouTube and other supported platforms

## Requirements

- Python 3.8+
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/JozsefIvanGafo/downloader.git
   cd downloader
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv .myenv
   # On Windows
   .myenv\Scripts\activate
   # On macOS/Linux
   source .myenv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Python File Manually

To run the downloader directly using Python:

```
python main.py
```

If you need to specify options:

```
python main.py 
```

## Building an Executable

To create a standalone executable with the application icon:

1. Make sure PyInstaller is installed:
   ```
   pip install pyinstaller
   ```

2. Build the executable with the icon:
   ```
   pyinstaller --onefile  --icon=icon.ico main.py
   ```



3. Alternatively, you can use the provided build script:
   ```
   python build.py
   ```

The executable will be created in the `dist` directory.

### Building Options Explained

- `--onefile`: Create a single executable file
- `--icon=icon.ico`: Use the specified icon for the executable

## Troubleshooting

- For Windows Store Python installations, PyInstaller versions below 4.4 are not supported without using a virtual environment.

- If you get file not found errors, ensure all paths are correctly specified.

## License

[Apache License Version 2.0]

## Credits

This project uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading functionality.