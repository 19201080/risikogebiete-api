#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
risikogebiete_analysis.pdf_analysis.pdf_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the analyse_pdf function, that parses the raw text from
the extracted pdf and returns a dict of countries and details about them.
"""

import re

from country_list import countries_for_language
from iso3166 import countries_by_alpha2

from risikogebiete_analysis.pdf_analysis.constants import \
    COUNTRY_SEPARATORS, INTRO_LINE, END_LINES, BULLETS, REGION_BULLET
from risikogebiete_analysis.pdf_analysis.mistyped_countries import \
    parse_mistyped_countries


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
                 for el in re.findall(sep, element)]
    if not separator:
        return False
    results = [match.start() for match in re.finditer(separator[0], element)
               if not separator_in_parenthesis(element, match.start())]
    return results


def remove_region_bullets(element):
    return '\n'.join(line for line in element.split('\n')
                     if not line.startswith(REGION_BULLET))


def no_date_in_parenthesis(element):
    return re.search(r'(\d+.\s?\w+)', element.replace('\n', '')) is None


def flatten_list(list_of_list):
    return [item for sublist in list_of_list for item in sublist]


def analyse_complex_country(element, separators, pattern):
    complex_matches = [element[separators[idx - 1] if idx else None:sep]
                       for idx, sep in enumerate(separators)]
    complex_matches = [element for group in complex_matches
                       for element in group.split('\n')
                       if not any(element.startswith(sep)
                                  for sep in COUNTRY_SEPARATORS)]
    complex_matches = [[element] if no_date_in_parenthesis(element)
                       else pattern.findall(element.replace('\n', ''))
                       for element in complex_matches
                       if element]
    return flatten_list(complex_matches)


def extract_country(element):
    pattern = re.compile(r'(.+)?\(.*\d+.\s?\w+\)?')

    element = remove_region_bullets(element)
    if separators := find_complex_case(element):
        return analyse_complex_country(element, separators, pattern)
    simple_case = [el for el in pattern.findall(element.replace('\n', ''))]
    if simple_case:
        return simple_case
    return [element]


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
    return text[min(found_indexes):] if reverse else text[:min(found_indexes)]


def extract_bullet_list(text):
    content = remove_special_characters(text)
    content = slice_from_line(content, INTRO_LINE, reverse=True)
    try:
        content, first_bullet = find_bullet_list(content, BULLETS)
    except ValueError as e:
        print(e)
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


def translate_countries(countries):
    country_codes = {name: code
                     for code, name in countries_for_language('de')}
    country_data = {al2: country_pattern(country.name, al2,
                                         country.alpha3, country.numeric)
                    for al2, country in countries_by_alpha2.items()}
    return [
        country_data.get(
            country_codes.get(
                country,
                parse_mistyped_countries(country, country_codes)),
            country_pattern(country))
        for country in countries]


def analyse_pdf(stream):
    bullet_list = extract_bullet_list(stream)
    country_list = flatten_list(extract_country(country)
                                for country in bullet_list)
    country_list = [country.strip() for country in country_list]
    country_list = translate_countries(country_list)
    return country_list
