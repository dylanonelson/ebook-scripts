import re
from files import rootpath

filenames = [
    f"{rootpath}/OEBPS/toc.ncx",
    f"{rootpath}/OEBPS/toc.xhtml"
]

add_selection = [
]

replacements = [
]

for filename in filenames:
    with open(filename, "r") as f:
        data = f.read()

        for pattern in replacements:
            data = re.sub(f"{pattern[0]}<", f"{pattern[1]}<", data)

        for pattern in add_selection:
            data = re.sub(f"{pattern}<", f"{pattern} (selection)<", data)


    with open(filename, "w") as f:
        f.write(data)
