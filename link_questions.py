import re
from files import rootpath, get_xhtml_filenames

Q_REGEX = re.compile(r"((.*?)(\d(.*?)))( \(\d+\))(.*?)$")
Q_SANS_P = re.compile(r"((.*?)(\d+\.(.*?)))(.*?)$")
QUOTE_REGEX = re.compile(r"(“.*?”)")

def extract_quote(line):
    q_result = re.search(Q_REGEX, line)
    if q_result != None:
        quote_result = re.search(QUOTE_REGEX, line)
        if quote_result:
            return quote_result.group(1)

    return False

def wrap_quote(line, quote, link_id):
    return re.sub(quote, f"<a href=\"#linked-quote-{link_id}\">{quote}</a>", line)

def wrap_quoted_text(line, quote, link_id):
    if quote == None:
        return line
    if re.search(Q_SANS_P, line) == None and re.search(quote, line) != None:
        return re.sub(quote, f"<a id=\"linked-quote-{link_id}\"></a>{quote}", line)
    else:
        return line

found = 0
linked = 0

for filename in get_xhtml_filenames():
    quoted_text = []
    lines = []
    with open(filename) as file:
        for line in file.readlines():
            quote = extract_quote(line)
            if quote != False:
                quote_id = len(quoted_text)
                quoted_text.append(quote[1:len(quote) - 1])
                next_line = re.sub(Q_REGEX, r"\1\6", line)
                next_line = wrap_quote(next_line, quote, quote_id)
                lines.append(next_line)
            else:
                lines.append(line)
    if len(quoted_text) == 0:
        continue
    with open(filename, 'w') as file:
        file.writelines(lines)
    lines = []
    with open(filename) as file:
        for line in file.readlines():
            next_line = line
            for idx, quote in enumerate(quoted_text):
                wrapped = wrap_quoted_text(next_line, quote, idx)
                if wrapped != next_line:
                    quoted_text = quoted_text[0:idx] + [None] + quoted_text[idx + 1:len(quoted_text)]
                next_line = wrapped
            lines.append(next_line)
    with open(filename, 'w') as file:
        file.writelines(lines)

    found += len(quoted_text)
    linked += len([quote for quote in quoted_text if quote == None])
    print (f"{linked}/{found}", end="\r", flush=True)
