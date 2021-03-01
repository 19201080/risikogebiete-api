#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
risikogebiete_api.pdf_analysis.pdf_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the analyse_pdf function, that parses the raw text from
the extracted pdf and returns a dict of countries and details about them.
"""

import logging
import re

from country_list import countries_for_language
from iso3166 import countries_by_alpha2

from risikogebiete_api.pdf_analysis.constants import \
    COUNTRY_SEPARATORS, INTRO_LINE, END_LINES, BULLETS
from risikogebiete_api.pdf_analysis.mistyped_countries import \
    parse_mistyped_countries

logger = logging.getLogger(__name__)


def separator_in_parenthesis(element, sep_index):
    previous_opening_paren = element.rfind('(', 0, sep_index)
    if previous_opening_paren == -1:
        return False
    previous_closing_paren = element.find(
        ')',
        previous_opening_paren,
        sep_index)
    if previous_closing_paren == -1:
        return True
    return False


def find_complex_case(element):
    separator = [el for sep in sorted(COUNTRY_SEPARATORS, key=len)[::-1]
                 for el in re.findall(str(sep), element)]
    if not separator:
        return False
    results = [match.start() for match in re.finditer(separator[0], element)
               if not separator_in_parenthesis(element, match.start())]
    return results


def extract_country(element):
    pattern = re.compile(r'(.+)?\(.*\d+.\s?\w+\)?')
    element = element.replace('\n', '')
    if found_country := pattern.findall(element):
        element = found_country[0].replace('gesamt', '')
    if separators := find_complex_case(element):
        first_separator = separators[0]
        return element[:first_separator].strip()
    return element.strip()


def find_bullet_list(text, bullets):
    bullet_list = {text.find('\n' + bullet): bullet for bullet in bullets
                   if text.find('\n' + bullet) >= 0}
    if len(bullet_list) == 0:
        raise ValueError('no bullet found')
    first_index = min(bullet_list.keys())
    first_bullet = bullet_list[first_index]
    return text[first_index + 2:], first_bullet


def remove_special_characters(text):
    return text.replace('\x0c', '').replace('\xa0', ' ')


def slice_from_line(text, *lines, reverse=False):
    found_indexes = [el for el in [text.find(line) for line in lines]
                     if el >= 0]
    if not found_indexes:
        return text
    first_index = min(found_indexes)
    if reverse:
        line_end = text.find('\n', first_index)
        return text[line_end:]
    line_beginning = text.rfind('\n', 0, first_index)
    return text[:line_beginning]


def extract_bullet_list(text):
    content = remove_special_characters(text)
    content = slice_from_line(content, INTRO_LINE, reverse=True)
    try:
        content, first_bullet = find_bullet_list(content, BULLETS)
    except ValueError as e:
        logger.error(e)
        return 1
    content = slice_from_line(content, *END_LINES)

    spaced_bullet = f'{first_bullet} '
    cleaned_content = content.split(spaced_bullet)
    cleaned_content = [item.strip() for item in cleaned_content
                       if any(char.isalnum() for char in item)]
    return cleaned_content


def country_pattern(name=None, alpha2=None, alpha3=None, numeric=None):
    return {'name': name,
            'alpha2': alpha2,
            'alpha3': alpha3,
            'numeric': numeric}


def translate_countries(countries, filename):
    country_codes = {name: code
                     for code, name in countries_for_language('de')}
    country_data = {al2: country_pattern(country.name, al2,
                                         country.alpha3, country.numeric)
                    for al2, country in countries_by_alpha2.items()}
    translated_countries = [country_codes.get(
        country, parse_mistyped_countries(country, country_codes))
        for country in countries]
    parsed_countries = [country_data.get(country, country_pattern(country))
                        for country in translated_countries]
    unrecognized_countries = [country for country in parsed_countries
                              if not country['alpha2']]
    for country in unrecognized_countries:
        logger.warning(f'unrecognized country in report '
                       f'{filename}: {country["name"]}')
    return parsed_countries


def analyse_pdf(stream, filename):
    bullet_list = extract_bullet_list(stream)
    country_list = [extract_country(country) for country in bullet_list]
    country_list = translate_countries(country_list, filename)
    return country_list
