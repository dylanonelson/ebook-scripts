from os import listdir
import re

rootpath = ""

def get_xhtml_filenames():
    files = []

    for file in listdir(f"{rootpath}/OEBPS"):
        if re.search(r"\.xhtml$", file) != None:
            files.append(f"{rootpath}file")

    return files
