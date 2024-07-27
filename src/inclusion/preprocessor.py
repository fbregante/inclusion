import re
import os

from requirements import SyntaxTreeSearcher


class PreprocessorError(Exception):
    pass


class Preprocessor:
    def __init__(self, libraries):
        self.libraries = libraries
        self.included_libraries = []

    def process_file(self, input_filename: str, output_filename: str) -> None:
        with open(input_filename, "r") as infile, open(output_filename, "w") as outfile:
            for line in infile:
                # If not a directive, just write it
                if not re.match(r";;\ *#", line.strip()):
                    outfile.write(line)
                    continue

                # Check if this comment matches a known directive
                include_match = re.match(r";;\ *#include\(([-\w0-9]+)\)", line.strip())
                require_match = re.match(
                    r";;\ *#require\(([-\w0-9]+)\)\[([-\w0-9,\s_]*)\]", line.strip()
                )

                # If it is a directive, fetch the library
                library_name = (include_match or require_match).group(1)
                library_content = self.fetch_library(library_name)

                # Write opening tag
                outfile.write(f";; <{library_name}>\n")
                # Determine which directive is and process it
                if include_match:
                    outfile.write(library_content)
                else:
                    definitions_required = list(
                        map(str.strip, require_match.group(2).split(","))
                    )
                    nodes = SyntaxTreeSearcher().get_definitions_and_dependencies(
                        definitions_required, library_content
                    )
                    for n in nodes:
                        outfile.write(str(n.text, "utf8"))
                # Write closing tag
                outfile.write(f"\n;; </{library_name}>\n")

    def fetch_library(self, library_name):
        if library_name in self.included_libraries:
            raise PreprocessorError(f"Already included library '{library_name}'")
        if library_name not in self.libraries:
            try:
                self.libraries[library_name] = self.read_library(library_name)
            except PreprocessorError as e:
                raise PreprocessorError(
                    f"Error including library '{library_name}': {str(e)}"
                )
        return self.libraries[library_name]

    def read_library(self, library_name: str) -> str:
        filename = os.path.join("clarity_libs", f"{library_name}.clar")
        try:
            with open(filename, "r") as file:
                content = file.read()
            return content.strip()
        except FileNotFoundError:
            raise PreprocessorError(f"Library file '{filename}' not found")
