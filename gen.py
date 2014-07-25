#!/usr/env/python
'''
Rule Generator to Expert SINTA engine

by: Wesley Melo and Thiago Lima
'''
import xmltodict

#opening input and output files
with open ("ontology.xml", "r") as myfile:
    data=myfile.read()
outFile=open('./ontology.owl', 'w+')

#parsing the XML file
xml = xmltodict.parse(data)
root = 'beer'
output = "<?xml version=\"1.0\"?>\n \
			<rdf:RDF \n \
			 xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n \
			 xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\"\n \
   			 xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n \
   			 xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n \
    		xmlns:vcard=\"http://www.w3.org/2001/vcard-rdf/3.0#\">\n "

#append header

#generating the rules
for beerClass in xml[root]:

	output += "<owl:Class rdf:ID=\"" + beerClass.encode('utf-8') + "\">" + '\n'
	output += "\t<rdfs:label xml:lang=\"en\">" + beerClass.encode('utf-8') + "</rdfs:label>" + '\n'
	
	#generating the first level of subclass
	for subClass1 in xml[root][str(beerClass)]:
		output += "\t<owl:Class rdf:ID=\"" + subClass1.encode('utf-8') + "\">" + '\n'
		#output += "\t\t<rdfs:label xml:lang=\"en\">" + subClass1.encode('utf-8') + "</rdfs:label>" + '\n'
		output += "\t\t<rdfs:subClassOf>\n" 
		output += "\t\t\t <owl:Class rdf:about=\"#" + beerClass.encode('utf-8') + "\"/>" + '\n'
		output += "\t\t</rdfs:subClassOf>\n" 
		output += "\t</owl:Class>" + '\n'

		#generating second level of subclass
		for subClass2 in xml[root][str(beerClass)][subClass1]:
			output += "\t<owl:Class rdf:ID=\"" + subClass2.encode('utf-8') + "\">" + '\n'
			#output += "\t\t<rdfs:label xml:lang=\"en\">" + subClass2.encode('utf-8') + "</rdfs:label>" + '\n'
			#output += "\t\t<rdfs:subClassOf rdf:resource=\"#" + subClass1.encode('utf-8') + "\" />" + '\n'
			output += "\t</owl:Class>" + '\n'

	
	#closing class
	output += "</owl:Class>" + '\n'

#closing rdf root tag
output +=  "</rdf:RDF>"

#writing in file
outFile.write(output)
