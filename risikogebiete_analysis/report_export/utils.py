#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse_data_for_csv(data):
    return [[timestamp, ','.join(str(list(country.values()))
                                 for country in countries)]
            for timestamp, filename, countries in data]


def parse_data_for_json(data):
    return {timestamp: countries for timestamp, filename, countries in data}
