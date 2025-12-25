from pathlib import Path

def get_image_files(folder_path):
    """
    Return a list of valid image file paths from the folder.
    Supports .png, .jpg, .jpeg
    """
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Folder not found: {folder_path}")

    valid_extensions = [".png", ".jpg", ".jpeg"]
    return [file for file in folder.iterdir() if file.suffix.lower() in valid_extensions]