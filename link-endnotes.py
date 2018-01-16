import re
from files import rootpath

def create_link_href(filename, prefix, number):
    return f"{filename}#{prefix}-{number}"

def create_id(prefix, number):
    return f"{prefix}-{number}"

note_item_regex = r"(&#9;\d{1,2})"
note_sup_regex = r"(<sup.*?</sup>)"
selection_prefix = ""

full_selection_filename = f"{rootpath}/OEBPS/GBF_PopTrio_Film-7.xhtml"
selection_filename = "GBF_PopTrio_Film-7.xhtml"

full_endnotes_filename = f"{rootpath}/OEBPS/GBF_PopTrio_Film-27.xhtml"
endnotes_filename = "GBF_PopTrio_Film-27.xhtml"

endnotes_lines = [182, 210]

def wrap_string_with_link(str, regex, filename, number):
    href = create_link_href(filename, selection_prefix, number)
    id = create_id(selection_prefix, number)
    newstr = f"<a id=\"{id}\" href=\"{href}\">{str}</a>"
    return re.sub(regex, newstr, str)

note_idx = 1

with open(full_endnotes_filename) as f:
    lines = f.readlines()
    start = endnotes_lines[0] - 1
    end = endnotes_lines[1]
    slicer = slice(start, end)

    for idx, line in enumerate(lines[slicer]):
        real_idx = start + idx
        match = re.search(note_item_regex, line)
        if match != None:
            sub = wrap_string_with_link(match.group(0), note_item_regex, selection_filename, note_idx)
            note_idx = note_idx + 1
            next = re.sub(note_item_regex, sub, line)
            lines[real_idx] = next

    print (note_idx)

with open(full_endnotes_filename, "w") as f:
    f.write("".join(lines))

note_idx = 1

with open(full_selection_filename) as f:
    lines = f.readlines()

    for idx, line in enumerate(lines):
        matches = re.finditer(note_sup_regex, line)
        has_match = False
        next = line

        for match in matches:
            has_match = True
            group = match.group(0)
            sub = wrap_string_with_link(group, note_sup_regex, endnotes_filename, note_idx)
            note_idx = note_idx + 1
            next = re.sub(group, sub, next)

        if has_match is True:
            lines[idx] = next

    print (note_idx)

with open(full_selection_filename, "w") as f:
    f.write("".join(lines))
