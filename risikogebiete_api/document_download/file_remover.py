#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from risikogebiete_api.utils import get_path_from_root

DOWNLOAD_FOLDER = get_path_from_root('files')


def remove_downloaded_files(folder=DOWNLOAD_FOLDER):
    if not os.path.exists(folder):
        return
    for file in os.listdir(folder):
        os.remove(get_path_from_root(file, folder))
    os.rmdir(folder)
