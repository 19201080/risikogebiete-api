#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import csv
import json
import logging
import os

import aiocsv
import aiofiles

from risikogebiete_api.utils \
    import parse_data_for_csv, parse_data_for_json, get_path_from_root

logger = logging.getLogger(__name__)


async def save_complete_report(data, filename):
    return await asyncio.gather(save_complete_csv_report(data, filename),
                                save_complete_json_report(data, filename))


async def save_complete_csv_report(data, filename):
    analysed_dates = [el[0] for el in data]
    csv_file_path = get_path_from_root(f'{filename}.csv')
    if not os.path.exists(csv_file_path):
        logger.info(f'{csv_file_path} doesn\'t exist, creating new one')
        await write_to_csv(data, csv_file_path)
    else:
        async with aiofiles.open(csv_file_path, mode='r+') as f:
            content = await f.read()
            if not content.strip():
                logger.debug(f'{csv_file_path} is empty, writing from scratch')
                await write_to_csv(data, csv_file_path)
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
    json_file_path = get_path_from_root(f'{filename}.json')
    if not os.path.exists(json_file_path):
        logger.info(f'{json_file_path} doesn\'t exist, creating new one')
        await write_to_json(data, json_file_path)
    else:
        async with aiofiles.open(json_file_path, mode='r+') as f:
            content = await f.read()
            if not content.strip():
                logger.debug(f'{json_file_path} is empty, '
                             f'writing from scratch')
                await write_to_json(data, json_file_path)
            else:
                saved_data = {k: v for k, v in json.loads(content).items()
                              if k not in analysed_dates}
                complete_data = {**saved_data, **parse_data_for_json(data)}
                await f.seek(0)
                await f.truncate()
                await f.write(json.dumps(complete_data,
                                         sort_keys=True, indent=2))


async def write_to_csv(data, file_path):
    data = sorted(data, key=lambda el: el[0])
    async with aiofiles.open(file_path, mode='w') as file:
        fieldnames = ['timestamp',
                      '\t'.join(['country', 'alpha2', 'alpha3', 'numeric'])]
        writer = aiocsv.AsyncWriter(file)
        await writer.writerow(fieldnames)
        await writer.writerows(parse_data_for_csv(data))


async def write_to_json(data, file_path):
    data = sorted(data, key=lambda el: el[0])
    data = {timestamp: countries for timestamp, countries in data}
    async with aiofiles.open(file_path, mode='w') as file:
        await file.write(json.dumps(data, sort_keys=True, indent=2))
