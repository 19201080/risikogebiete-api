#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
risikogebiete_analysis.document_download.file_downloader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains a function to download a pdf to the files directory.
"""

import requests


def download_file(file, url):
    file_directory = '../files/'
    with requests.get(url, stream=True) as r:
        with open(f'{file_directory}{file}.pdf', 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
    f.close()
