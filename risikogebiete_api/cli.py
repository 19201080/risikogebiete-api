#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import sys

import click

from risikogebiete_api.pdf_analysis.pdf_extractor import extract_pdf_data
from risikogebiete_api.pdf_analysis.pdf_parser import analyse_pdf
from risikogebiete_api.document_download.page_scraper \
    import get_page_content
from risikogebiete_api.document_download.document_comparator \
    import get_missing_reports
from risikogebiete_api.document_download.file_downloader \
    import manage_downloads
from risikogebiete_api.document_download.file_remover \
    import remove_downloaded_files
from risikogebiete_api.report_export.individual_report \
    import save_individual_reports
from risikogebiete_api.report_export.complete_report \
    import save_complete_report
from risikogebiete_api.utils import get_path_from_root

logger = logging.getLogger(__name__)
LOG_FORMAT = ('%(asctime)-15s [%(levelname)-7s]: '
              '%(message)s (%(filename)s:%(lineno)s)')


async def get_reports():
    root_url = 'https://www.rki.de'
    url = (
        'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_'
        'Coronavirus/Transport/Archiv_Risikogebiete/DE-Tab.html'
    )
    results = get_page_content(url)
    missing_reports = get_missing_reports(results)
    await manage_downloads(missing_reports, root_url)


async def analyse_report(path):
    filename = os.path.basename(path)
    analysis = analyse_pdf(extract_pdf_data(path), filename)
    analysis = sorted(analysis, key=lambda x: x['name'])
    timestamp = filename.replace('.pdf', '')
    logger.debug(f'analysed report: {filename}')
    return timestamp, analysis


async def analyse_all_reports(directory):
    tasks = [analyse_report(get_path_from_root(file, directory))
             for file in os.listdir(directory)]
    return await asyncio.gather(*tasks)


async def extract_data():
    download_directory_path = get_path_from_root('files')
    report_directory_path = get_path_from_root('individual_reports')
    complete_report_name = 'data'

    if not os.path.exists(download_directory_path):
        return

    analysis = await analyse_all_reports(download_directory_path)
    logger.info(f'analysed {len(analysis)} '
                f'report{"s" if len(analysis) else ""}')
    return await asyncio.gather(
        save_individual_reports(analysis, report_directory_path),
        save_complete_report(analysis, complete_report_name))


@click.command()
@click.option('--debug/--no-debug', '-d', default=False)
def main(debug):
    logging.getLogger('pdfminer').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.basicConfig(
        format=LOG_FORMAT,
        level=logging.DEBUG if debug else logging.INFO)
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_reports())
        loop.run_until_complete(extract_data())
        loop.close()
        remove_downloaded_files()
        return 0
    except KeyboardInterrupt:
        return 0
    except RuntimeError:
        return 1


if __name__ == "__main__":
    sys.exit(main())