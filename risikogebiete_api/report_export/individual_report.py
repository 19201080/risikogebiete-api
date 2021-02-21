#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

import aiofiles
import aiocsv


async def save_individual_reports(data, directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)
    for timestamp, filename, analysis in data:
        filename = filename.replace('.pdf', '')
        csv_file = f'{directory}{filename}.csv'
        async with aiofiles.open(csv_file, mode='w') as file:
            fieldnames = list(analysis[0].keys())
            csv_countries = [list(country.values()) for country in analysis]
            writer = aiocsv.AsyncWriter(file)
            await writer.writerow(fieldnames)
            await writer.writerows(csv_countries)

        json_file = f'{directory}{filename}.json'
        async with aiofiles.open(json_file, mode='w') as file:
            await file.write(json.dumps(analysis, indent=2))
