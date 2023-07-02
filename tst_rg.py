__author__ = 'alexandr'
# coding: utf-8
from re import match

rg = ur'^[А-Я]+$'

if match(rg, u'ААААа'):
    print (True)
else:
    print (False)