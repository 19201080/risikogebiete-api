#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse_data_for_csv(data):
    return [[timestamp,
             *['\t'.join(str(val) for val in country.values())
               for country in countries]]
            for timestamp, countries in data]


def parse_data_for_json(data):
    return {timestamp: countries for timestamp, countries in data}
