#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

import aiofiles
import aiocsv

from risikogebiete_api.utils import get_path_from_root


async def save_individual_reports(data, directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)
    for timestamp, analysis in data:
        csv_file_path = get_path_from_root(f'{timestamp}.csv', directory)
        async with aiofiles.open(csv_file_path, mode='w') as file:
            fieldnames = list(analysis[0].keys())
            csv_countries = [list(country.values()) for country in analysis]
            writer = aiocsv.AsyncWriter(file)
            await writer.writerow(fieldnames)
            await writer.writerows(csv_countries)

        json_file_path = get_path_from_root(f'{timestamp}.json', directory)
        async with aiofiles.open(json_file_path, mode='w') as file:
            await file.write(json.dumps(analysis, indent=2))
