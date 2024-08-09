import os
import json
import csv

def check_required_files(directory):
    required_files = ['metadata.json', 'model.obj', 'site_map.csv']
    optional_folders = ['hardware', 'scripts']

    files = os.listdir(directory)
    files_set = set(files)

    for file in required_files:
        if file not in files_set:
            print(f"Missing required file: {file} in {directory}")
            return False

    for folder in optional_folders:
        if folder in files_set and not os.path.isdir(os.path.join(directory, folder)):
            print(f"Optional folder {folder} is listed but is not a directory in {directory}")
            return False

    return True

def validate_metadata(metadata_file):
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    required_keys = ['name', 'type', 'producer', 'sites', 'shanks']
    for key in required_keys:
        if key not in metadata:
            print(f"Missing required key in metadata: {key}")
            return False

    # Additional validation for types
    if not isinstance(metadata['name'], str) or \
       not isinstance(metadata['producer'], str) or \
       not isinstance(metadata['type'], str) or \
       not isinstance(metadata['sites'], str) or \
       not isinstance(metadata['shanks'], str):
        print("Metadata fields have incorrect types")
        return False

    return True

def validate_site_map(site_map_file):
    try:
        with open(site_map_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get('index') or not row.get('x') or not row.get('y') or not row.get('z'):
                    print("Site map CSV is missing required fields")
                    return False
                # Check that numerical values are correct
                for field in ['x', 'y', 'z', 'w', 'h', 'd']:
                    try:
                        float(row.get(field, 0))
                    except ValueError:
                        print(f"Invalid value for {field} in site map CSV")
                        return False
    except Exception as e:
        print(f"Error reading site map CSV: {e}")
        return False

    return True

def main():
    for subdir in os.listdir('.'):
        if os.path.isdir(subdir) and not subdir.startswith('.') and not subdir.startswith('tests'):
            print(f"Checking {subdir}...")
            if check_required_files(subdir):
                metadata_file = os.path.join(subdir, 'metadata.json')
                if validate_metadata(metadata_file):
                    site_map_file = os.path.join(subdir, 'site_map.csv')
                    validate_site_map(site_map_file)
                else:
                    print(f"Invalid metadata in {subdir}")
            else:
                print(f"Required files missing in {subdir}")

if __name__ == "__main__":
    main()
