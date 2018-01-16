from copy import copy
from files import rootpath
from bs4 import BeautifulSoup

filename = f"{rootpath}/OEBPS/GBF_PopTrio_TV_copy-27.xhtml"
new_contents = []
file = open(filename)
contents = file.readlines()

def reverse_sup_with_anchor(tag):
    sup = tag.sup.extract()
    num = sup.string.extract()
    a = copy(tag)
    a.append(num)
    sup.append(a)
    print (sup)
    return sup

for line in contents:
    soup = BeautifulSoup(line)
    tags = soup.find_all("a", {"epub:type": "noteref"})
    if len(tags) > 0:
        for tag in tags:
            new_tag = reverse_sup_with_anchor(tag)
            tag.replace_with(new_tag)

        new_contents.append(str(soup))
    else:
        new_contents.append(line)

file.close()

file = open(filename, "w")
file.writelines(new_contents)
file.close()
