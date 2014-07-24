#!/usr/env/python

import xmltodict

with open ("ontology.xml", "r") as myfile:
    data=myfile.read()

#parsing the XML file
xml = xmltodict.parse(data)
root = 'beer'

#generating the classes
for beerClass in xml[root]:
	print "<owl:Class rdf:ID=\"" + beerClass + "\">"
	print "\t<rdfs:label xml:lang=\"en\">" + beerClass + "</rdfs:label>" 
	
	#generating the subclasses
	for subClass1 in xml[root][str(beerClass)]:
		print "\t<owl:Class rdf:ID=\"" + subClass1 + "\">"
		print "\t\t<rdfs:subClassOf rdf:resource=\"#" + beerClass + "\" />"
	
	#closing class
	print "</owl:Class>"

