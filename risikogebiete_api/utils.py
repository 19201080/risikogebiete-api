#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_path_from_root(tail, root=ROOT_DIRECTORY):
    return os.path.join(root, tail)


if __name__ == '__main__':
    print('->', get_path_from_root('downloads'))
