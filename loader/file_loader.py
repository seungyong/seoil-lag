from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import BSHTMLLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
import json
from pathlib import Path
import os

ALLOW_TEXT = [".txt", ".md"]
ALLOW_HTML = [".html", ".htm"]
ALLOW_PDF = [".pdf"]
ALLOW_CSV = [".csv"]
ALLOW_JSON = [".json"]
ALLOW_ZIP = [".zip"]


def universal_file_loader(source):
    filename, file_extension = os.path.splitext(source)
    file_extension = file_extension.lower()

    data, loader = '', None

    if file_extension in ALLOW_TEXT:
        loader = TextLoader(source, autodetect_encoding=True)
    elif file_extension in ALLOW_HTML:
        loader = BSHTMLLoader(source, open_encoding='utf-8')
    elif file_extension in ALLOW_PDF:
        loader = PyPDFLoader(source)
    elif file_extension in ALLOW_CSV:
        loader = CSVLoader(file_path=source, encoding="utf-8")
    elif file_extension in ALLOW_JSON:
        data = json.loads(Path(source).read_text(), encoding="utf-8")
    else:
        print("Not recognize file type :", file_extension)
    if loader:
        data = loader.load()

    return data
