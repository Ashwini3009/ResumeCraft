import os
from pathlib import Path
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mini_project.settings")
django.setup()

from ATS_Project_Mini.models import UploadedFile

# Define the uploads folder path
UPLOADS_FOLDER = Path(__file__).resolve().parent.parent / 'media' / 'uploads'

def clear_uploads():
    """
    Clear the uploads folder and delete corresponding entries from the database.
    """
    # Get all files in the uploads folder
    files_in_folder = list(UPLOADS_FOLDER.glob("*"))

    if not files_in_folder:
        print("No files found in the uploads folder.")
        return

    print(f"Found {len(files_in_folder)} file(s) in the uploads folder.")

    # Iterate through files and delete them
    for file_path in files_in_folder:
        try:
            # Delete file from the filesystem
            os.remove(file_path)
            print(f"Deleted file: {file_path.name}")

            # Delete file entry from the database if it exists
            db_entry = UploadedFile.objects.filter(file=f"uploads/{file_path.name}").first()
            if db_entry:
                db_entry.delete()
                print(f"Deleted entry from database: {file_path.name}")
            else:
                print(f"No database entry found for: {file_path.name}")

        except Exception as e:
            print(f"Error deleting file {file_path.name}: {e}")

if __name__ == "__main__":
    clear_uploads()
