#!/usr/bin/env python

from pathlib import Path

import mkdocs_gen_files


def build_sidebar(data, indentation=0):
    lines = []
    for key in sorted(data):
        value = data[key]
        if isinstance(value, dict):
            lines.append(f"{indentation * ' '}* {key}")
            lines.extend(build_sidebar(value, indentation + 4))
        else:
            lines.append(f"{indentation * ' '}* [{key}.py]({value})")
    return lines


sidebar_data = {
    "mkdocstrings": {},
    "mkdocs_autorefs": {
        "references": "autorefs/references.md",
        "plugin": "autorefs/plugin.md",
    },
}

for path in Path("src", "mkdocstrings").glob("**/*.py"):
    module_path = path.relative_to("src", "mkdocstrings").with_suffix(".md")
    current_dict = sidebar_data["mkdocstrings"]
    for part in module_path.parts:
        if part.endswith(".md"):
            key = part[:-3]
            value = str(module_path)
        else:
            key = part
            value = {}
        if key not in current_dict:
            current_dict[key] = value
        if isinstance(current_dict[key], dict):
            current_dict = current_dict[key]

    doc_path = Path("reference", module_path)
    with mkdocs_gen_files.open(doc_path, "w") as f:
        ident = ".".join(path.relative_to("src").with_suffix("").parts)
        print("::: " + ident, file=f)

    mkdocs_gen_files.set_edit_path(doc_path, Path("..", path))

with mkdocs_gen_files.open("reference/sidebar.md", "w") as sidebar_file:
    sidebar_contents = "\n".join(build_sidebar(sidebar_data))
    print(sidebar_contents, file=sidebar_file)
