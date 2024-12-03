import re, os

from loader.dir_loader import universal_dir_loader
from loader.file_loader import universal_file_loader, ALLOW_ZIP
from loader.url_loader import universal_url_loader
from loader.zip_loader import universal_zip_loader

regex = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")
p = re.compile(regex)


def universal_loader_v2(source):
    docs = []

    if re.search(p, source):
        docs = universal_url_loader(source)
    elif os.path.isdir(source):
        docs = universal_dir_loader(source)
    elif os.path.isfile(source):
        docs = universal_file_loader(source)
    else:
        filename, file_extension = os.path.splitext(source)
        file_extension = file_extension.lower()
        if file_extension in ALLOW_ZIP:
            docs = universal_zip_loader(source)

    return docs
