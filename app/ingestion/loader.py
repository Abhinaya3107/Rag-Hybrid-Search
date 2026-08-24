from pathlib import Path
from pypdf import PdfReader
import docx

def load_document(path: Path) -> str:
    """Extract raw text from a pdf, docx, or txt/md file."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif suffix == ".docx":
        doc = docx.Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    elif suffix in (".txt", ".md"):
        return path.read_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

def load_all_documents(folder: Path) -> list[dict]:
    """Returns [{"source": filename, "text": content}, ...]"""
    docs = []
    for path in folder.glob("**/*"):
        if path.is_file() and path.suffix.lower() in (".pdf", ".docx", ".txt", ".md"):
            docs.append({"source": path.name, "text": load_document(path)})
    return docs