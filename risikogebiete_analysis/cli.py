#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from datetime import datetime
import json
import os
import re
import sys

import aiocsv
import aiofiles

from risikogebiete_analysis.pdf_analysis.pdf_extractor import extract_pdf_data
from risikogebiete_analysis.pdf_analysis.pdf_parser import analyse_pdf
from risikogebiete_analysis.document_download.page_scraper \
    import get_page_content
from risikogebiete_analysis.document_download.document_comparator \
    import get_missing_files
from risikogebiete_analysis.document_download.file_downloader \
    import manage_downloads


async def get_reports():
    root_url = 'https://www.rki.de'
    url = (
        'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_'
        'Coronavirus/Transport/Archiv_Risikogebiete/DE-Tab.html'
    )
    results = get_page_content(url)
    missing_files = get_missing_files(results)
    await manage_downloads(missing_files, root_url)


def filename_to_datetime(filename):
    def date_format_2021(digits):
        return len(digits) == 3 and len(digits[0]) == 4

    def either(iterable, key, default):
        try:
            return iterable[key]
        except IndexError:
            return default

    digits = re.findall(r'\d+', filename)
    if date_format_2021(digits):
        params = digits
    else:
        params = (digits[0][4:], digits[0][2:4], digits[0][:2],
                  either(digits, 1, 0), either(digits, 2, 0))
    params = (int(el) for el in params)
    return datetime(*params).isoformat()


async def analyse_report(path):
    filename = path.split('/')[-1]
    analysis = analyse_pdf(extract_pdf_data(path), filename)
    analysis = sorted(analysis, key=lambda x: x['name'])
    timestamp = filename_to_datetime(filename)
    print(f'analysed report: {path.split("/")[-1]}')
    return timestamp, analysis


async def analyse_all_reports(directory):
    tasks = [analyse_report(f'{directory}/{file}')
             for file in os.listdir(directory)]
    return await asyncio.gather(*tasks)


async def write_to_file(data, filename):
    data = sorted(data, key=lambda el: el[0])
    async with aiofiles.open(filename, mode='w') as file:
        for item in data:
            await file.write(f'{item[0]}: {str(item[1])}\n')


async def write_to_csv(data, filename):
    data = sorted(data, key=lambda el: el[0])
    async with aiofiles.open(filename, mode='w') as file:
        fieldnames = ['timestamp', 'countries']
        writer = aiocsv.AsyncWriter(file)
        await writer.writerow(fieldnames)
        await writer.writerows([timestamp, ','.join(str(list(country.values()))
                                                    for country in countries)]
                               for timestamp, countries in data)


async def write_to_json(data, filename):
    data = sorted(data, key=lambda el: el[0])
    data = {timestamp: countries for timestamp, countries in data}
    async with aiofiles.open(filename, mode='w') as file:
        await file.write(json.dumps(data, indent=2))


async def extract_data():
    directory = '../files'
    analysis = await analyse_all_reports(directory)
    print(f'analysed {len(analysis)} report{"s" if len(analysis) else ""}')
    return await asyncio.gather(
        write_to_json(analysis, 'data.json'),
        write_to_csv(analysis, 'data.csv'))


def main():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_reports())
        loop.run_until_complete(extract_data())
        loop.close()
        return 0
    except KeyboardInterrupt:
        return 0
    except RuntimeError:
        return 1


if __name__ == "__main__":
    sys.exit(main())
