#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_path_from_root(tail, root=ROOT_DIRECTORY):
    return os.path.join(root, tail)


def parse_data_for_csv(data):
    return [[timestamp,
             *['\t'.join(str(val) for val in country.values())
               for country in countries]]
            for timestamp, countries in data]


def parse_data_for_json(data):
    return {timestamp: countries for timestamp, countries in data}


if __name__ == '__main__':
    print('->', get_path_from_root('downloads'))
