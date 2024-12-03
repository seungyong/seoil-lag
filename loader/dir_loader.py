import os

from loader.file_loader import universal_file_loader


def universal_dir_loader(source):
    dir_list = os.listdir(source) # 현재 폴더에 있는것만 읽어 들임.
    docs = []
    dir_list.sort()

    for file_name in dir_list:
        if file_name[0] == ".":
            continue

        if os.path.isdir(file_name):
            doc = universal_dir_loader(source + "/" + file_name)
        else:
            doc = universal_file_loader(source + "/" + file_name)

        if doc:
            docs.extend(doc)

    return docs