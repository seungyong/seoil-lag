from io import BytesIO
from zipfile import ZipFile
import requests

from loader.file_loader import universal_file_loader


def universal_zip_loader(file_url):
    url = requests.get(file_url)
    zipfile = ZipFile(BytesIO(url.content))
    zipfile.extractall("/tmp")
    docs = []
    
    for file_name in zipfile.namelist():
        doc = universal_file_loader("/tmp/"+file_name)

        if doc:
            docs.extend(doc)
    return docs