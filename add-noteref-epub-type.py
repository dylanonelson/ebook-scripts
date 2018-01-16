import re
from bs4 import BeautifulSoup
from files import rootpath, get_xhtml_filenames
from os import listdir

counter = 0
files = get_xhtml_filenames()

def find_tags(soup):
    return soup.find_all(name="a", href=re.compile(r"_idFootnoteLink"))

for file in files:
    full_path = file
    full_lines = []
    with open(full_path) as contents:
        lines = contents.readlines()
        for line in lines:
            soup = BeautifulSoup(line)
            tags = find_tags(soup)
            if len(tags) > 0:
                for tag in tags:
                    tag['epub:type'] = 'noteref'
                    counter += 1
                full_lines.append(str(soup))

                print ("BEFORE:")
                print (line)
                print ("AFTER:")
                print (str(soup))
            else:
                full_lines.append(line)

    with open(full_path, "w") as new_contents:
        new_contents.writelines(full_lines)

print (counter)
