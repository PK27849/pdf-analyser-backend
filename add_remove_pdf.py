import os

current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_dir, "search_pdf_api/pdf_temp_storage")

async def save_pdf(file):
    target_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf_temp_storage")
    os.makedirs(target_directory, exist_ok=True)
    file_path = os.path.join(target_directory, file.filename)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    return file_path

def rem_pdf(file_path):
    # Deleting the file at the given file path
    try:
        os.remove(file_path)
        print("File deleted successfully:", file_path)
    except FileNotFoundError:
        print("File not found:", file_path)
    except Exception as e:
        print("An error occurred while deleting the file:", str(e))


