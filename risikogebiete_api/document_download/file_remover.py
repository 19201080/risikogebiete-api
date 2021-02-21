#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

DOWNLOAD_FOLDER = '../files/'


def remove_downloaded_files(folder=DOWNLOAD_FOLDER):
    if not os.path.exists(folder):
        return
    for file in os.listdir(folder):
        os.remove(folder + file)
    os.rmdir(folder)
