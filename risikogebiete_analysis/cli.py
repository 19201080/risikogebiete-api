#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from risikogebiete_analysis.pdf_analysis.pdf_extractor import simple_extract
from risikogebiete_analysis.pdf_analysis.pdf_parser import analyse_pdf


def main():
    file = '../files/Risikogebiete_27112020.pdf'
    start_line = 'Folgende Staaten/Regionen gelten aktuell als Risikogebiete:'
    end_line = 'Gebiete, die zu einem beliebigen Zeitpunkt in den vergangenen'
    raw_text = simple_extract(file)
    result = analyse_pdf(raw_text, start_line, end_line)

    for i, (key, val) in enumerate(result.items()):
        print(f'{val["case"]:<10}{key:<60}{val["details"]}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
