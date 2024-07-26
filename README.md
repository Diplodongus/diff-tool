# Configuration Diff Tool

## Overview

This tool provides a graphical user interface for comparing network device configurations against a golden (standard) configuration. It's designed to help network administrators quickly identify discrepancies between actual device configurations and the desired standard configuration.

## Features

- GUI for easy file and folder selection
- Comparison of multiple device configurations against a single golden config
- Detailed HTML diff output for each comparison
- Progress tracking for bulk comparisons
- Summary statistics for each comparison (added, removed, and modified lines)

## Requirements

- Python 3.6+
- tkinter (usually comes pre-installed with Python)
- fuzzywuzzy (for string matching)

## Installation

1. Clone this repository:
git clone https://github.com/diplodongus/diff-tool.git

cd diff-tool

3. (Optional) Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate

4. Install the required packages:
pip install -r requirements.txt

## Usage

1. Run the GUI:
python main_gui.py

2. In the GUI:
- Select the golden configuration file
- Select the folder containing device configuration files
- Click "Compare" to start the comparison process

3. The tool will generate HTML diff files in a `diff_output` folder within the selected device config folder.

## File Structure

- `main_gui.py`: Entry point for the GUI application
- `gui.py`: Contains the GUI implementation
- `config_parser.py`: Functions for reading and parsing configuration files
- `config_comparator.py`: Core logic for comparing configurations
- `html_generator.py`: Functions for generating HTML diff output
- `main.py`: Way to launch the program using the command line. Takes files from configs/ folder, and compares with a "config.cfg" file in a "golden" folder. Would recommend to just use the GUI unless you are testing something.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
