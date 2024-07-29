import unittest
from io import StringIO

from inclusion.preprocessor import Preprocessor, PreprocessorError


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

        preprocessor = Preprocessor(libraries={"testlib": "(define-constant TEST u2)"})
        preprocessor.process_stream(infile, outfile)

        outfile.seek(0)
        result = outfile.read()
        self.assertEqual(
            result, ";; <testlib>\n(define-constant TEST u2)\n;; </testlib>\n"
        )

    def test_with_header(self):
        infile = StringIO()
        outfile = StringIO()
        infile.write(";; #include(testlib)\n")
        infile.seek(0)

        preprocessor = Preprocessor(
            ";; HEADER", {"testlib": "(define-constant TEST u2)"}
        )
        preprocessor.process_stream(infile, outfile)

        outfile.seek(0)
        result = outfile.read()
        self.assertEqual(
            result,
            ";; <testlib>\n;; HEADER\n(define-constant TEST u2)\n;; </testlib>\n",
        )

    def test_require(self):
        infile = StringIO()
        outfile = StringIO()
        infile.write(";; #require(testlib)[TEST]\n(define-data-var day uint u10)\n")
        infile.seek(0)

        preprocessor = Preprocessor(libraries={"testlib": "(define-constant TEST u2)\n(define-map balances principal uint)\n"})
        preprocessor.process_stream(infile, outfile)

        outfile.seek(0)
        result = outfile.read()
        self.assertEqual(
            result, ";; <testlib>\n(define-constant TEST u2)\n;; </testlib>\n(define-data-var day uint u10)\n"
        )

    def test_require_many(self):
        infile = StringIO()
        outfile = StringIO()
        infile.write(";; #require(testlib)[TEST,balances]\n(define-data-var day uint u10)\n")
        infile.seek(0)
        
        preprocessor = Preprocessor(libraries={"testlib": "(define-constant TEST u2)\n(define-map balances principal uint)\n"})
        preprocessor.process_stream(infile, outfile)

        outfile.seek(0)
        result = outfile.read()
        self.assertEqual(
            result, ";; <testlib>\n(define-constant TEST u2)\n(define-map balances principal uint)\n;; </testlib>\n(define-data-var day uint u10)\n"
        )

    def test_many_require(self):
        infile = StringIO()
        outfile = StringIO()
        infile.write(";; #require(testlib)[TEST]\n;; #require(testlib2)[balances]\n(define-data-var day uint u10)\n")
        infile.seek(0)
        
        preprocessor = Preprocessor(libraries={"testlib": "(define-constant TEST u2)\n", "testlib2": "(define-map balances principal uint)\n"})
        preprocessor.process_stream(infile, outfile)

        outfile.seek(0)
        result = outfile.read()
        self.assertEqual(
            result, ";; <testlib>\n(define-constant TEST u2)\n;; </testlib>\n;; <testlib2>\n(define-map balances principal uint)\n;; </testlib2>\n(define-data-var day uint u10)\n"
        )

    def test_require_with_dependencies(self):
        infile = StringIO()
        outfile = StringIO()
        infile.write(";; #require(testlib)[get-test]\n(define-data-var day uint u10)\n")
        infile.seek(0)
        
        preprocessor = Preprocessor(libraries={"testlib": "(define-data-var test uint u2)\n(define-read-only (get-test)\n\t(var-get test)\n)\n"})
        preprocessor.process_stream(infile, outfile)

        outfile.seek(0)
        result = outfile.read()
        self.assertEqual(
            result, ";; <testlib>\n(define-data-var test uint u2)\n(define-read-only (get-test)\n\t(var-get test)\n)\n;; </testlib>\n(define-data-var day uint u10)\n"
        )


if __name__ == "__main__":
    unittest.main()
