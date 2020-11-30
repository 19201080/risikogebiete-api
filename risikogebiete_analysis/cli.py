#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import sys

from risikogebiete_analysis.pdf_analysis.pdf_extractor import simple_extract
from risikogebiete_analysis.pdf_analysis.pdf_parser import analyse_pdf
from risikogebiete_analysis.document_download.page_scraper \
    import get_page_content
from risikogebiete_analysis.document_download.document_comparator \
    import get_missing_files
from risikogebiete_analysis.document_download.file_downloader \
    import manage_downloads


def get_reports():
    root_url = 'https://www.rki.de'
    url = (
        'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_'
        'Coronavirus/Transport/Archiv_Risikogebiete/DE-Tab.html'
    )
    results = get_page_content(url)
    missing_files = get_missing_files(results)
    asyncio.run(manage_downloads(missing_files, root_url))


def main():
    get_reports()
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
