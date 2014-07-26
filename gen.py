#!/usr/env/python
'''
Rule Generator to Expert SINTA engine

by: Wesley Melo and Thiago Lima
'''
import xmltodict

#auxiliar function to help identation
def ident(level):
	ret = ""
	for i in range(level):
		ret += "\t"
	return ret

#opening input and output files
with open ("ontology.xml", "r") as myfile:
    data=myfile.read()
outFile=open('./ontology.owl', 'w+')

#parsing the XML file
xml = xmltodict.parse(data)

#Here we go!

#append header
output = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + \
			ident(0) + "<rdf:RDF\n" + \
				ident(1) + "xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n" + \
				ident(1) + "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\"\n" + \
   				ident(1) + "xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n" + \
   			 	ident(1) + "xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n" + \
    			ident(1) +  "xmlns:vcard=\"http://www.w3.org/2001/vcard-rdf/3.0#\">\n"


#generating the rules
root = 'beer'
for beerClass in xml[root]:

	output += ident(1) + "<owl:Class rdf:about=\"#" + beerClass.encode('utf-8') + "\"/>" + '\n'
	
	output += '\n'

	#generating the first level of subclass
	for subClass1 in xml[root][str(beerClass)]:
		output += ident(1) + "<owl:Class rdf:about=\"#" + subClass1.encode('utf-8') + "\">" + '\n'
		output += ident(2) + "<rdfs:subClassOf rdf:resource=\"#" + beerClass.encode('utf-8') + "\"/>" + '\n'
		output += ident(1) + "</owl:Class>" + '\n'

		#generating second level of subclass (individuals)
		for subClass2 in xml[root][str(beerClass)][subClass1]:
			#if subClass2 == 'Appearance' \
			#   or subClass2 == 'Aroma-and-taste' \
			#   or subClass2 == 'Mouth-feel':
			#	for subClass3 in xml[root][str(beerClass)][subClass1][subClass2]:
			#		output += ident(2) + "<owl:onProperty>" + "\n"
			#		output += ident(3) + "<owl:DatatypeProperty " + \
			#							  "rdf:ID=\"" + subClass3.encode('utf-8') + "\"/>" + '\n'
			#		output += ident(2) + "</owl:onProperty>" + "\n"
			if subClass2 == 'Samples':
				for subClass3 in xml[root][str(beerClass)][subClass1][subClass2]:

					output += ident(1) + "<owl:NamedIndividual rdf:about=\"#" + subClass3.encode('utf-8') + "\">" + '\n'
					output += ident(2) + "<rdf:type rdf:resource=\"#" + subClass1.encode('utf-8') + "\"/>" + '\n'
					output += ident(2) + "<rdf:type rdf:resource=\"#" + beerClass.encode('utf-8') + "\"/>" + '\n'
					output += ident(1) + "</owl:NamedIndividual>" + '\n'

		
		output += '\n'
#closing rdf root tag
output +=  "</rdf:RDF>"

#writing in file
outFile.write(output)
