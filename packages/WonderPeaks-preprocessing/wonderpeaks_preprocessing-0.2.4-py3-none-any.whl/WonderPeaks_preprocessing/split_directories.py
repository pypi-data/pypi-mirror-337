
import os
import shutil


def split_files_by_suffix(directory, reads = ["R1"]):
    """
    Splits files in a directory into new subdirectories based on their suffix 
    (R1, R2, I1, I2 in the filename).
    
    Parameters:
    - directory (str): Path to the directory containing the files to split.
    """
    # Define suffixes and corresponding subdirectory names
    suffixes = reads
    raw_directory = os.path.join(directory, "raw_data")
    subdirs = {suffix: os.path.join(raw_directory,f"raw_data_{suffix}") for suffix in suffixes}



    # Create new subdirectories
    for subdir in subdirs.values():
        os.makedirs(subdir, exist_ok=True)

    # Iterate over files in the directory
    for file in os.listdir(raw_directory):
        file_path = os.path.join(raw_directory, file)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Check if the file name contains one of the suffixes and move it
        for suffix in suffixes:
            if suffix in file:
                shutil.move(file_path, os.path.join(subdirs[suffix], file))
                print(f"Moved file '{file}' to '{subdirs[suffix]}'")
                break  # Stop checking other suffixes once a match is found
