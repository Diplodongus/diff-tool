import os
import logging
from config_parser import get_config_files, read_config_file
from config_comparator import compare_with_golden
from html_generator import generate_html_diff

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    base_dir = 'configs'  # Update this to your config folder path
    golden_config_path = 'golden\\config.cfg'
    output_dir = 'output'  # New directory for output files

    logging.info(f"Reading golden config from {golden_config_path}")
    golden_config = read_config_file(golden_config_path)
    logging.info(f"Golden config read. Length: {len(golden_config)} characters")

    config_files = get_config_files(base_dir)
    logging.info(f"Found {sum(len(files) for files in config_files.values())} config files")

    for os_type, files in config_files.items():
        logging.info(f"Processing {os_type} configs:")
        for file in files:
            logging.info(f"  Processing {file}")
            config = read_config_file(file)
            logging.info(f"  Config file read. Length: {len(config)} characters")
            
            # Compare with golden config
            diff = compare_with_golden(config, golden_config)
            logging.info(f"  Comparison complete. Diff entries: {len(diff)}")
            
            # Write raw diff to text file
            file_name = sanitize_filename(os.path.basename(file))
            raw_diff_file = os.path.join(output_dir, f"{file_name}_vs_golden_raw_diff.txt")
            with open(raw_diff_file, 'w', encoding='utf-8') as f:
                for diff_type, line in diff:
                    f.write(f"{diff_type}: {line}\n")
            logging.info(f"    Raw diff file written: {raw_diff_file}")
            
            # Generate HTML diff
            html_diff = generate_html_diff(diff, file, golden_config_path)
            logging.info(f"  HTML diff generated. Length: {len(html_diff)} characters")
            
            # Write HTML diff to file
            diff_file = os.path.join(output_dir, f"{file_name}_vs_golden_diff.html")
            ensure_dir(diff_file)
            with open(diff_file, 'w', encoding='utf-8') as f:
                f.write(html_diff)
            
            logging.info(f"    HTML diff file written: {diff_file}")

if __name__ == "__main__":
    main()