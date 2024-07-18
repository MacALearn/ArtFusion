import os


def is_valid_directory(path):
    """
    Check if the directory path is valid.

    Parameters:
        path (str): Directory path to check.

    Returns:
        bool: True if the directory exists and is valid, False otherwise.
    """
    if not isinstance(path, str):
        return False

    return os.path.isdir(path)


# Example usage:
directory_path = r"E:\kaggle\archive"
if is_valid_directory(directory_path):
    print("Directory is valid.")
else:
    print("Directory is not valid.")



