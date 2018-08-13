from os import listdir
import re

rootpath = "/Users/dylanonelson/Dropbox/Ebook-projects/Nature-of-Life/epub/9780945159797.epub"

def is_xhtml(filename):
    return re.search(r"\.xhtml$", filename) != None

def get_xhtml_filenames():
    return [f"{rootpath}/OEBPS/{file}" for file in listdir(f"{rootpath}/OEBPS") if is_xhtml(file)]
