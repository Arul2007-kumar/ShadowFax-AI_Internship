from pathlib import Path
from io import BytesIO

import fitz
import pytesseract
from PIL import Image


def extract_ocr_text(page) -> str:
    """
    Convert PDF page into image and extract text using OCR.
    """

    # Render PDF page as high-resolution image
    pix = page.get_pixmap(
        matrix=fitz.Matrix(2, 2),
        alpha=False
    )

    # Convert image bytes to PIL Image
    image = Image.open(
        BytesIO(pix.tobytes("png"))
    )

    # Extract text using Tesseract OCR
    text = pytesseract.image_to_string(
        image
    )

    return text.strip()


def load_pdf(file_path: str) -> list[dict]:

    pages = []

    document = fitz.open(file_path)

    for page_number, page in enumerate(document):

        # First try normal PDF text extraction
        text = page.get_text().strip()

        # If no text is found, use OCR
        if not text:

            print(
                f"Page {page_number + 1}: "
                "No text found. Running OCR..."
            )

            text = extract_ocr_text(page)

        else:

            print(
                f"Page {page_number + 1}: "
                "Text extracted normally."
            )

        pages.append({
            "page": page_number + 1,
            "text": text
        })

    document.close()

    return pages


def load_text(file_path: str) -> list[dict]:

    text = Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    )

    return [{
        "page": None,
        "text": text
    }]


def load_document(file_path: str) -> list[dict]:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = path.suffix.lower()

    print("File:", path)
    print("Extension:", extension)

    if extension == ".pdf":

        return load_pdf(file_path)

    elif extension in [".txt", ".md"]:

        return load_text(file_path)

    else:

        raise ValueError(
            f"Unsupported file format: {extension}. "
            "Only PDF, TXT and Markdown files are supported."
        )