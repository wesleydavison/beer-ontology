#!/usr/env/python

import xmltodict

#opening input and output files
with open ("ontology.xml", "r") as myfile:
    data=myfile.read()
outFile=open('./ontology.owl', 'w+')


#parsing the XML file
xml = xmltodict.parse(data)
root = 'beer'
output = ""

#generating the classes
for beerClass in xml[root]:
	output += "<owl:Class rdf:ID=\"" + beerClass + "\">" + '\n'
	output += "\t<rdfs:label xml:lang=\"en\">" + beerClass + "</rdfs:label>" + '\n'
	
	#generating the subclasses
	for subClass1 in xml[root][str(beerClass)]:
		output += "\t<owl:Class rdf:ID=\"" + subClass1 + "\">" + '\n'
		output += "\t\t<rdfs:subClassOf rdf:resource=\"#" + beerClass + "\" />" + '\n'
		output += "\t</owl:Class>" + '\n'
	
	#closing class
	output += "</owl:Class>" + '\n'

#writing in file
outFile.write(output)
