#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
risikogebiete_api.document_download.document_comparator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the get_missing_reports function that compares results
from the RKI Risikogebiete archive to the files already downloaded.
"""

import os

from risikogebiete_api.utils import get_path_from_root
from risikogebiete_api.constants import INDIVIDUAL_REPORTS


def get_missing_reports(scraped_results):
    local_directory = get_path_from_root(INDIVIDUAL_REPORTS)
    if not os.path.isdir(local_directory):
        return scraped_results
    local_files = {item.split('.')[0] for item in os.listdir(local_directory)}
    missing_reports = {key: val for key, val in scraped_results.items()
                       if val['date'] not in local_files}
    return missing_reports
