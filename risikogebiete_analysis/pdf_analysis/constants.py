#!/usr/bin/env python
# -*- coding: utf-8 -*-

HYPHEN_SEPARATOR = ('- ', ' - ', ' -')
EN_DASH_SEPARATOR = ('– ', ' – ', ' –')
COLON_SEPARATOR = (': ', ' : ', ' :')
COUNTRY_SEPARATORS = (*COLON_SEPARATOR, *HYPHEN_SEPARATOR, *EN_DASH_SEPARATOR)

INTRO_LINE = 'Unten aufgeführte Staaten werden aktuell als Gebiete'
END_LINES = [
    'Gebiete, die zu einem beliebigen Zeitpunkt in den vergangenen',
    'Die bestehenden Reise- und Sicherheitshinweise',
    'Die Einstufung als Risikogebiet']

BULLETS = ['•', '']
REGION_BULLET = 'o '
