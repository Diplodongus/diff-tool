import os

def get_config_files(base_dir):
    config_files = {}
    for root, dirs, files in os.walk(base_dir):
        os_type = os.path.basename(root)
        if os_type not in config_files:
            config_files[os_type] = []
        for file in files:
            if file.endswith('.cfg'):  # Assuming config files have .cfg extension
                config_files[os_type].append(os.path.join(root, file))
    return config_files

def read_config_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()