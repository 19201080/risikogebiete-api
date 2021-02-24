#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
risikogebiete_api.document_download.file_downloader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains a function to manage the download of missing files.
"""

import asyncio
import logging
import os

import aiohttp
import aiofiles

logger = logging.getLogger(__name__)


async def download_file(filename, url, session: aiohttp.ClientSession):
    file_directory = '../files/'
    path = f'{file_directory}{filename}.pdf'

    if not os.path.exists(file_directory):
        os.mkdir(file_directory)

    async with session.get(url) as response:
        async with aiofiles.open(path, mode='wb') as file:
            async for data, _ in response.content.iter_chunks():
                await file.write(data)
    logger.debug(f'saved new report: {filename}')


async def manage_downloads(files, root_url):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for value in files.values():
            tasks.append(download_file(value['date'],
                                       root_url + value['url'],
                                       session))
        logger.info(f'downloading {len(tasks)} file'
                    f'{"s" if len(tasks) > 1 else ""}')
        await asyncio.gather(*tasks)
