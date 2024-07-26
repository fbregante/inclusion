import re
import sys
import os

import requirements

class PreprocessorError(Exception):
    pass

def read_library(library_name):
    filename = os.path.join("clarity_libs", f"{library_name}.clar")
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content.strip()
    except FileNotFoundError:
        raise PreprocessorError(f"Library file '{filename}' not found")

def process_file(input_filename, output_filename):
    included_libraries = set()
    libraries = {}

    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            if line.strip().startswith(';;'):
                # Check if this comment is a directive
                include_match = re.match(r';;\ *#include\(([-\w0-9]+)\)', line.strip())
                require_match = re.match(r';;\ *#require\(([-\w0-9]+)\)\[([-\w0-9,\s_]*)\]', line.strip())
                
                if require_match:
                    library_name = require_match.group(1)
                    requires = list(map(str.strip, require_match.group(2).split(",")))
                    if library_name in included_libraries:
                        raise PreprocessorError(f"Already included library '{library_name}': {str(e)}")
                        
                    if library_name not in libraries:
                        try:
                            libraries[library_name] = read_library(library_name)
                        except PreprocessorError as e:
                            raise PreprocessorError(f"Error including library '{library_name}': {str(e)}")
                    
                    included_libraries.add(library_name)
                    library_content = libraries[library_name]

                    nodes = requirements.get_definitions(requires, library_content)
                    
                    outfile.write(f";; <{library_name}>\n")
                    for n in nodes:
                        outfile.write(str(n.text, "utf8"))
                    outfile.write(f"\n;; </{library_name}>\n")
                elif include_match:
                    library_name = include_match.group(1)
                    if library_name in included_libraries:
                        raise PreprocessorError(f"Already included library '{library_name}': {str(e)}")
                        
                    if library_name not in libraries:
                        try:
                            libraries[library_name] = read_library(library_name)
                        except PreprocessorError as e:
                            raise PreprocessorError(f"Error including library '{library_name}': {str(e)}")
                    
                    included_libraries.add(library_name)
                    library_content = libraries[library_name]
                    outfile.write(f";; <{library_name}>\n")
                    outfile.write(library_content)
                    outfile.write(f"\n;; </{library_name}>\n")
                else:
                    outfile.write(line)  # Keep comments that are not directives
            else:
                outfile.write(line)

def main():
    if len(sys.argv) != 3:
        print("Usage: python preprocessor.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        process_file(input_file, output_file)
        print(f"Preprocessed {input_file} and saved to {output_file}")
    except PreprocessorError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
