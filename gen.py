#!/usr/env/python

import xmltodict

with open ("ontology.xml", "r") as myfile:
    data=myfile.read()

xmlParsed = xmltodict.parse(data)
for beerClasses in xmlParsed['beer']:
	print beerClasses

