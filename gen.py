#!/usr/env/python

import xmltodict

with open ("ontology.xml", "r") as myfile:
    data=myfile.read()

#parsing the XML file
xml = xmltodict.parse(data)
root = 'beer'

#generating the classes
for beerClass in xml[root]:
	print "<owl:Class rdf:ID=\"" + beerClass + "\" />"
	
	#generating the subclasses
	for subClass1 in xml[root][str(beerClass)]:
		print "\t<owl:Class rdf:ID=\"" + subClass1 + "\">"
		print "\t<rdfs:subClassOf rdf:resource=\"#" + beerClass + "\" />"
	print "</owl:Class>"

