import os

def ensure_folder_exists(folder_path):
    """
    Tworzy folder, jeśli nie istnieje.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
