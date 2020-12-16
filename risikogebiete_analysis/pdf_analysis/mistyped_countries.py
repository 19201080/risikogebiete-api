#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def parse_mistyped_countries(country, country_codes):
    if re.match(r'Bosni(a|en) [au]nd Herzego[vw]ina', country):
        return country_codes['Bosnien und Herzegowina']
    if re.match(r'Brunei', country):
        return country_codes['Brunei Darussalam']
    if re.match(r'Côte d\'Ivoire', country):
        return country_codes['Côte d’Ivoire']
    if re.match(r'Guinea.Bissau', country):
        return country_codes['Guinea-Bissau']
    if re.match(r'Kap Verde', country):
        return country_codes['Cabo Verde']
    if re.match(r'Kongo DR', country):
        return country_codes['Kongo-Kinshasa']
    if re.match(r'Kongo Rep', country):
        return country_codes['Kongo-Brazzaville']
    if re.match(r'Korea \(.+\)', country):
        return country_codes['Nordkorea']
    if re.match(r'Kosovo', country):
        return 'XK'
    if re.match(r'Palästinensische\s+(Autonomieg|G)ebiete', country):
        return country_codes['Palästinensische Autonomiegebiete']
    if re.match(r'Papua‐Neuguinea', country):
        return country_codes['Papua-Neuguinea']
    if re.match(r'Puerto Rico.*', country):
        return country_codes['Puerto Rico']
    if re.match(r'Russische Föderation', country):
        return country_codes['Russland']
    if re.match(r'Saint Kitts und Nevis', country):
        return country_codes['St. Kitts und Nevis']
    if re.match(r'Saint Lucia', country):
        return country_codes['St. Lucia']
    if re.match(r'(Saint Vincent [au]nd (die|the) Grenadine[ns])', country):
        return country_codes['St. Vincent und die Grenadinen']
    if re.match(r'Sankt Kitts und Nevis', country):
        return country_codes['St. Kitts und Nevis']
    if re.match(r'Saudi Arabien', country):
        return country_codes['Saudi-Arabien']
    if re.match(r'Süd(-S|s)udan', country):
        return country_codes['Südsudan']
    if re.match(r'Surinam', country):
        return country_codes['Suriname']
    if re.match(r'Syrische Arabische Republik', country):
        return country_codes['Syrien']
    if re.match(r'Timor Leste \(Osttimor\)', country):
        return country_codes['Timor-Leste']
    if re.match(r'Trinidad Tobago', country):
        return country_codes['Trinidad und Tobago']
    if re.match(r'USA', country):
        return country_codes['Vereinigte Staaten']
    if re.match(r'Vereinigtes Königreich von Großbritannien.*', country):
        return country_codes['Vereinigtes Königreich']
    if re.match(r'Weißrussland', country):
        return country_codes['Belarus']
    return country
