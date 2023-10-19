#!/usr/bin/python3
"""
Python script that converts Markdown to HTML.

Usage: ./markdown2html.py input_file output_file
"""

import sys
import re
from os.path import exists
from hashlib import md5

def h(line):
    # Create heading HTML element
    line = line.strip()
    parse_space = line.split(" ")
    level = min(len(parse_space[0]), 6)
    content = " ".join(parse_space[1:])
    return f"<h{level}>{content}</h{level}>"

def li(line):
    # Create a list item HTML element
    line = line.strip()
    content = " ".join(line.split(" ")[1:])
    return f"<li>{content}</li>"

def clean_line(line):
    # Styling tags with the use of Regular expressions.
    # Replace ** for <b> tags
    line = re.sub(r"\*\*(\S+)", r"<b>\1</b>", line)
    # Replace __ for <em> tags
    line = re.sub(r"\_\_(\S+)", r"<em>\1</em>", line)
    # Replace [[<content>]] for md5 hash of content.
    line = re.sub(r"\[\[(.*?)\]\]", lambda match: md5(match.group(1).encode()).hexdigest(), line)
    # Replace ((<content>)) for no C characters on content.
    line = re.sub(r"\(\((.*?)\)\)", lambda match: match.group(1).replace('C', ''), line)
    return line

def mark2html(input_file, output_file):
    with open(input_file, "r") as f:
        markdown = f.readlines()

    html = []

    index = 0
    while index < len(markdown):
        line = clean_line(markdown[index])

        if line.startswith("#"):
            html.append(h(line))
        elif line.startswith(("-", "*")):
            list_type = {"-": "ul", "*": "ol"}
            current_index = index
            ul_string = f"<{list_type[line[0]]}>\n"
            while current_index < len(markdown) and markdown[current_index].startswith(("-", "*")):
                ul_string += li(markdown[current_index])
                current_index += 1
            index = current_index - 1
            ul_string += f"</{list_type[line[0]}>"
            html.append(ul_string)
        elif not line:
            line = ""
        else:
            paragraph = "<p>\n"
            new_index = index

            while new_index < len(markdown):
                line = clean_line(markdown[new_index])
                next_line = markdown[new_index + 1] if new_index + 1 < len(markdown) else "\n"
                paragraph += line.strip() + "\n"
                if next_line.startswith(("-", "*", "#", "\n")):
                    index = new_index
                    break
                if not next_line.startswith(("-", "*", "#", "\n")):
                    paragraph += "        <br />\n"
                new_index += 1

            paragraph += "</p>"
            html.append(paragraph)
        index += 1

    text = "\n".join(html)

    with open(output_file, "w") as f:
        f.write(text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py input_file output_file\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not exists(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    mark2html(input_file, output_file)
