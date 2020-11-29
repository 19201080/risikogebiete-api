#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
risikogebiete_analysis.pdf_analysis.pdf_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the analyse_pdf function, that parses the raw text from
the extracted pdf and returns a dict of countries and details about them.
"""

from risikogebiete_analysis.pdf_analysis.constants import COUNTRY_SEPARATORS


def country_only_parsing(element):
    sep = element.rfind(' (')
    country_name = element[:sep]
    details = element[sep:].strip()
    return {'name': country_name, 'case': 'simple', 'details': details}


def exceptions_parsing(country_name, details):
    return {'name': country_name, 'case': 'except', 'details': details}


def regions_parsing(country_name, details):
    return {'name': country_name, 'case': 'regions', 'details': details}


def country_with_regions_parsing(element, sep_index):
    first_region_bullet = ': o '
    exception_text = 'mit Ausnahme'

    smallest_country_sep = min(len(el) for el in COUNTRY_SEPARATORS)
    country_name = element[:sep_index]
    details = element[sep_index+smallest_country_sep:].strip()
    if details.find(first_region_bullet) != -1:
        return regions_parsing(country_name, details)
    if details.find(exception_text) != -1:
        return exceptions_parsing(country_name, details)
    return {'name': country_name, 'case': 'complex', 'details': details}


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
    results = [element.find(sep) for sep in COUNTRY_SEPARATORS]
    results = [sep for sep in results
               if not separator_in_parenthesis(element, sep) and sep != -1]
    return -1 if len(results) == 0 else min(results)


def analyse_country(element):
    complex_sep_position = find_complex_case(element)
    if complex_sep_position == -1:
        return country_only_parsing(element)
    return country_with_regions_parsing(element, complex_sep_position)


def analyse_pdf(stream, start_line, end_line):
    start_index = stream.find(start_line)
    end_index = stream.rfind(end_line)
    assert(start_index != -1), 'start_line not found'
    assert (end_index != -1), 'end_line not found'
    list_result = stream[start_index+len(start_line):end_index].split('•')
    list_result = [analyse_country(el.strip()) for el in list_result
                   if not el.isspace()]
    dict_result = {el['name']: {'case': el['case'], 'details': el['details']}
                   for el in list_result}

    return dict_result
