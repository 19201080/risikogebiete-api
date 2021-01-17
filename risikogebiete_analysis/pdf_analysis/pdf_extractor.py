#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
risikogebiete_analysis.pdf_analysis.pdf_extractor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Code taken from the docs of pdfminer.six.
https://pdfminersix.readthedocs.io/en/latest/tutorial/highlevel.html
https://pdfminersix.readthedocs.io/en/latest/tutorial/composable.html
"""

from io import StringIO

from pdfminer.high_level import extract_text_to_fp
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def extract_pdf_data(filename):
    output_string = StringIO()
    with open(filename, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams(char_margin=4.0)
        device = TextConverter(rsrcmgr, output_string, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()


def simple_extract(filename):
    output_string = StringIO()
    with open(filename, 'rb') as fin:
        extract_text_to_fp(fin, output_string)
    return output_string.getvalue().strip()
