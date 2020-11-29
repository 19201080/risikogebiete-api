#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
risikogebiete_analysis.document_download.page_scraper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the get_page_content function, to scrape the web page of
the RKI containing the archives of Risikogebiete documents. It extracts the
URLs of the available PDFs and the associated date.
"""

from datetime import datetime

import requests
from bs4 import BeautifulSoup


def get_date_time(string):
    input_date = [int(el) for el in string.split()[0].split('.')][::-1]
    input_time = [int(el) for el in string.split()[2].split(':')]
    date = datetime(
        *input_date,
        hour=input_time[0],
        minute=input_time[1] if len(input_time) > 1 else 0)
    return date.isoformat()


def get_filename(url):
    filename = url.split('.pdf')[0].split('/')[-1]
    return filename


def get_page_content(url):
    keyword = 'Archiv_Risikogebiete'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    parent = soup.select_one('ul[class="links"]')
    links = parent.select(f'a[href*={keyword}]')
    return {
        get_filename(link['href']): {
            'date': get_date_time(link.string),
            'url': link['href']
        } for link in links}
