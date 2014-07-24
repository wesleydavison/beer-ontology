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

	output += "<owl:Class rdf:ID=\"" + beerClass.encode('utf-8') + "\">" + '\n'
	output += "\t<rdfs:label xml:lang=\"en\">" + beerClass.encode('utf-8') + "</rdfs:label>" + '\n'
	
	#generating the first level of subclass
	for subClass1 in xml[root][str(beerClass)]:
		output += "\t<owl:Class rdf:ID=\"" + subClass1.encode('utf-8') + "\">" + '\n'
		output += "\t\t<rdfs:label xml:lang=\"en\">" + subClass1.encode('utf-8') + "</rdfs:label>" + '\n'
		output += "\t\t<rdfs:subClassOf rdf:resource=\"#" + beerClass.encode('utf-8') + "\" />" + '\n'
		output += "\t</owl:Class>" + '\n'

		#generating second level of subclass
		for subClass2 in xml[root][str(beerClass)][subClass1]:
			output += "\t<owl:Class rdf:ID=\"" + subClass2.encode('utf-8') + "\">" + '\n'
			output += "\t\t<rdfs:label xml:lang=\"en\">" + subClass2.encode('utf-8') + "</rdfs:label>" + '\n'
			output += "\t\t<rdfs:subClassOf rdf:resource=\"#" + subClass1.encode('utf-8') + "\" />" + '\n'
			output += "\t</owl:Class>" + '\n'

	
	#closing class
	output += "</owl:Class>" + '\n'

#writing in file
outFile.write(output)
