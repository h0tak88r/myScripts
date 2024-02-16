import os

def move_files(source_dir, destination_dir):
    """
    Move all files from the source directory to the destination directory.
    If a file with the same name already exists in the destination directory,
    it will be overwritten.
    """
    for filename in os.listdir(source_dir):
        if os.path.isfile(os.path.join(source_dir, filename)):
            source_file = os.path.join(source_dir, filename)
            destination_file = os.path.join(destination_dir, filename)
            os.rename(source_file, destination_file)

def remove_empty_directories(top_dir):
    """
    Remove all empty directories from the specified directory and its subdirectories.
    """
    for root, _, files in os.walk(top_dir, topdown=True):
        if not files:
            os.rmdir(root)

if __name__ == "__main__":
    source_dir = "directory1"
    destination_dir = "directory1"

    # Move files from nested directories to directory1
    for root, _, files in os.walk(source_dir):
        for filename in files:
            source_file = os.path.join(root, filename)
            destination_file = os.path.join(destination_dir, filename)
            os.rename(source_file, destination_file)

    # Remove empty directories
    remove_empty_directories(source_dir)
