import sys
from inclusion.preprocessor import Preprocessor, PreprocessorError
from inclusion.libs import HEADER, LIBRARIES


def main():
    if len(sys.argv) != 3:
        print("Usage: python preprocessor.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        Preprocessor(HEADER, LIBRARIES).process_file(input_file, output_file)
        print(f"Preprocessed {input_file} and saved to {output_file}")
    except PreprocessorError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
