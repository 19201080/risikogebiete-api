#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import csv
import json
import logging
import os

import aiocsv
import aiofiles

from risikogebiete_api.utils import parse_data_for_csv, parse_data_for_json

logger = logging.getLogger(__name__)


async def save_complete_report(data, filename):
    return await asyncio.gather(save_complete_csv_report(data, filename),
                                save_complete_json_report(data, filename))


async def save_complete_csv_report(data, filename):
    analysed_dates = [el[0] for el in data]
    csv_filename = f'{filename}.csv'
    if not os.path.exists(csv_filename):
        logger.info(f'{csv_filename} doesn\'t exist, creating new one')
        await write_to_csv(data, csv_filename)
    else:
        async with aiofiles.open(csv_filename, mode='r+') as f:
            content = await f.read()
            if not content.strip():
                logger.debug(f'{csv_filename} is empty, writing from scratch')
                await write_to_csv(data, csv_filename)
            else:
                fieldnames, *saved_data = [
                    line for line in csv.reader(content.splitlines())
                    if line and line[0] not in analysed_dates]
                complete_data = [*saved_data, *parse_data_for_csv(data)]
                complete_data = sorted(complete_data, key=lambda el: el[0])
                await f.seek(0)
                await f.truncate()
                writer = aiocsv.AsyncWriter(f)
                await writer.writerow(fieldnames)
                await writer.writerows(complete_data)


async def save_complete_json_report(data, filename):
    analysed_dates = [el[0] for el in data]
    json_filename = f'{filename}.json'
    if not os.path.exists(json_filename):
        logger.info(f'{json_filename} doesn\'t exist, creating new one')
        await write_to_json(data, json_filename)
    else:
        async with aiofiles.open(json_filename, mode='r+') as f:
            content = await f.read()
            if not content.strip():
                logger.debug(f'{json_filename} is empty, writing from scratch')
                await write_to_json(data, json_filename)
            else:
                saved_data = {k: v for k, v in json.loads(content).items()
                              if k not in analysed_dates}
                complete_data = {**saved_data, **parse_data_for_json(data)}
                await f.seek(0)
                await f.truncate()
                await f.write(json.dumps(complete_data,
                                         sort_keys=True, indent=2))


async def write_to_csv(data, filename):
    data = sorted(data, key=lambda el: el[0])
    async with aiofiles.open(filename, mode='w') as file:
        fieldnames = ['timestamp',
                      '\t'.join(['country', 'alpha2', 'alpha3', 'numeric'])]
        writer = aiocsv.AsyncWriter(file)
        await writer.writerow(fieldnames)
        await writer.writerows(parse_data_for_csv(data))


async def write_to_json(data, filename):
    data = sorted(data, key=lambda el: el[0])
    data = {timestamp: countries for timestamp, countries in data}
    async with aiofiles.open(filename, mode='w') as file:
        await file.write(json.dumps(data, sort_keys=True, indent=2))
