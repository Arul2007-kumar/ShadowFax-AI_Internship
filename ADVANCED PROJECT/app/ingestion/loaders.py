from pathlib import Path
import fitz

def load_pdf(file_path:str)->list[dict]:
    pages=[]
    document=fitz.open(file_path)
    for page_number,page in enumerate(document):
        text=page.get_text()
        pages.append({
            "page":page_number+1,
            "text":text
        })
    document.close=()
    return pages

def load_text(file_path:str)->list[dict]:
    text=Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    )
    return[{
        "page":None,
        "text":text
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
            "Only PDF, TXT and Markdown are supported."
        )