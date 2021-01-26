#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
risikogebiete_analysis.document_download.document_comparator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the get_missing_reports function that compares results
from the RKI Risikogebiete archive to the files already downloaded.
"""

import os


def get_missing_reports(scraped_results):
    local_directory = '../individual_reports/'
    if not os.path.isdir(local_directory):
        return scraped_results
    local_files = {item.split('.')[0] for item in os.listdir(local_directory)}
    missing_reports = {key: val for key, val in scraped_results.items()
                       if key not in local_files}
    return missing_reports
