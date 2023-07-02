#! /usr/bin/env python2
# coding: utf-8
from lxml import etree
from os import listdir, path
from sys import argv
data = []
#
# educationqualificationnamerod = {
#     "6.051004": u'бакалавра з оптотехніки',
#     "6.050502": u'бакалавра з інженерної механіки',
#     "6.051001": u'бакалавра з метрології та інформаційно-вимірювальних технологій',
#     "6.050503": u'бакалавра з машинобудування'
# }
#
# educationqualificationname = {
#     "6.051004": u'бакалавр з оптотехніки',
#     "6.050502": u'бакалавр з інженерної механіки',
#     "6.051001": u'бакалавр з метрології та інформаційно-вимірювальних технологій',
#     "6.050503": u'бакалавр з машинобудування'
# }


def to_normal(name):
    return '"%s"' % (name[0].upper() + name[1:].lower())

for fl_name in listdir(argv[1]):
    for action, elem in etree.iterparse(path.join(argv[1], fl_name), tag='document'):
        elem[0].attrib['specdirprofnameen'] = to_normal(elem[0].attrib['specdirprofnameen'])
        elem[0].attrib['specdirprofname'] = to_normal(elem[0].attrib['specdirprofname'])
        elem[0].attrib['bossen'] = u'Volodymyr Hrabko'
        elem[0].attrib['boss'] = u'В.В. Грабко'
        elem[0].attrib['dateendeducation'] = elem[0].attrib['dateendeducation'].replace('/', '.')
        elem[0].attrib['dategive'] = elem[0].attrib['dategive'].replace('/', '.')
        # if elem[0].attrib['specdirprofcode'] in educationqualificationname:
        #     print elem[0].attrib['specdirprofcode']
        #     elem[0].attrib['educationqualificationname'] = educationqualificationname[elem[0].attrib['specdirprofcode']]
        #
        # if elem[0].attrib['specdirprofcode'] in educationqualificationnamerod:
        #     print elem[0].attrib['specdirprofcode']
        #     elem[0].attrib['educationqualificationnamerod'] = educationqualificationnamerod[elem[0].attrib['specdirprofcode']]

        data.append(etree.tostring(elem, encoding='utf-8'))

with open('file.xml', 'w') as fl:
    fl.write('<?xml version="1.0" encoding="utf-8"?><documents>')
    for i in data:
        fl.writelines(i)
    fl.write('</documents>')
print len(data)
