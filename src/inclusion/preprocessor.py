import re
import os

import requirements


class PreprocessorError(Exception):
    pass


def read_library(library_name: str) -> str:
    filename = os.path.join("clarity_libs", f"{library_name}.clar")
    try:
        with open(filename, "r") as file:
            content = file.read()
        return content.strip()
    except FileNotFoundError:
        raise PreprocessorError(f"Library file '{filename}' not found")


def process_file(input_filename: str, output_filename: str) -> None:
    included_libraries = set()
    libraries = {}

    with open(input_filename, "r") as infile, open(output_filename, "w") as outfile:
        for line in infile:
            if line.strip().startswith(";;"):
                # Check if this comment is a directive
                include_match = re.match(r";;\ *#include\(([-\w0-9]+)\)", line.strip())
                require_match = re.match(
                    r";;\ *#require\(([-\w0-9]+)\)\[([-\w0-9,\s_]*)\]", line.strip()
                )

                any_match = include_match or require_match
                if any_match is None:
                    outfile.write(line)  # Keep comments that are not directives
                    continue

                library_name = any_match.group(1)
                if library_name in included_libraries:
                    raise PreprocessorError(
                        f"Already included library '{library_name}'"
                    )
                if library_name not in libraries:
                    try:
                        libraries[library_name] = read_library(library_name)
                    except PreprocessorError as e:
                        raise PreprocessorError(
                            f"Error including library '{library_name}': {str(e)}"
                        )

                included_libraries.add(library_name)
                library_content = libraries[library_name]
                outfile.write(f";; <{library_name}>\n")

                if require_match:
                    requires = list(map(str.strip, require_match.group(2).split(",")))
                    nodes = requirements.get_definitions(requires, library_content)
                    for n in nodes:
                        outfile.write(str(n.text, "utf8"))
                if include_match:
                    outfile.write(library_content)

                outfile.write(f"\n;; </{library_name}>\n")
            else:
                outfile.write(line)
