import os


def count_pdf_files(folder_path):
    """Count the number of PDF files in the given folder."""
    if not os.path.exists(folder_path):
        return 0
    return len([f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')])