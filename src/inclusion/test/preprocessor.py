import unittest
from io import StringIO

from preprocessor import Preprocessor, PreprocessorError


class TestPreprocessor(unittest.TestCase):
    def test_no_library(self):
        preprocessor = Preprocessor("HEADER")
        self.assertRaises(
            PreprocessorError,
            preprocessor.fetch_library,
            "testlib",
        )

    def test_no_header(self):
        infile = StringIO()
        outfile = StringIO()
        infile.write(";; #include(testlib)\n")
        infile.seek(0)

        preprocessor = Preprocessor(libraries= {"testlib": "(define-constant TEST u2)"})
        preprocessor.process_stream(infile, outfile)

        outfile.seek(0)
        result = outfile.read()
        self.assertEqual(
            result,
            ";; <testlib>\n(define-constant TEST u2)\n;; </testlib>\n"
        )

    def test_with_header(self):
        infile = StringIO()
        outfile = StringIO()
        infile.write(";; #include(testlib)\n")
        infile.seek(0)

        preprocessor = Preprocessor(";; HEADER", {"testlib": "(define-constant TEST u2)"})
        preprocessor.process_stream(infile, outfile)

        outfile.seek(0)
        result = outfile.read()
        self.assertEqual(
            result,
            ";; <testlib>\n;; HEADER\n(define-constant TEST u2)\n;; </testlib>\n"
        )

    def test_require(self):
        infile = StringIO()
        outfile = StringIO()
        infile.write(";; #require(testlib)[TEST]\n")
        infile.seek(0)

        preprocessor = Preprocessor(libraries= {"testlib": "(define-constant TEST u2)"})
        preprocessor.process_stream(infile, outfile)

        outfile.seek(0)
        result = outfile.read()
        self.assertEqual(
            result,
            ";; <testlib>\n(define-constant TEST u2)\n;; </testlib>\n"
        )



if __name__ == "__main__":
    unittest.main()
