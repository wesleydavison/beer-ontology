#!/usr/env/python
# coding: utf-8
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
    data = myfile.read()
ontFile = open('./ontology.owl', 'w+')
sintaFile = open("./expert-sinta-input.txt", 'w+')

#pseudo-initialization of output strings
outOntFile = ""
outSintaFile = ""


#parsing the XML file
xml = xmltodict.parse(data)

#Here we go!

#append header
outOntFile = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + \
			ident(0) + "<rdf:RDF\n" + \
				ident(1) + "xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n" + \
				ident(1) + "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\"\n" + \
   				ident(1) + "xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n" + \
   			 	ident(1) + "xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n" + \
    			ident(1) +  "xmlns:vcard=\"http://www.w3.org/2001/vcard-rdf/3.0#\">\n"


#generating the rules
root = 'beer'
for beerClass in xml[root]:

	outOntFile += ident(1) + "<owl:Class rdf:about=\"#" + beerClass.encode('utf-8') + "\"/>" + '\n\n'

	#generating the first level of subclass
	for subClass1 in xml[root][str(beerClass)]:
		outOntFile += ident(1) + "<owl:Class rdf:about=\"#" + subClass1.encode('utf-8') + "\">" + '\n'
		outOntFile += ident(2) + "<rdfs:subClassOf rdf:resource=\"#" + beerClass.encode('utf-8') + "\"/>" + '\n'
		outOntFile += ident(1) + "</owl:Class>" + '\n'

		outSintaFile +=  "Regra " + subClass1.encode('utf-8') + "\n"
		firstTime = True
		#generating second level of subclass (individuals)
		for subClass2 in xml[root][str(beerClass)][subClass1]:
			if subClass2 == 'Appearance' \
			   or subClass2 == 'Aroma-and-taste' \
			   or subClass2 == 'Mouth-feel':
				for subClass3 in xml[root][str(beerClass)][subClass1][subClass2]:
					
					condition = "SE " if firstTime else "E "
					outSintaFile += ident(1) + condition + \
									subClass3.encode('utf-8') + " = " + \
									xml[root][str(beerClass)][subClass1][subClass2][subClass3] + '\n'
					firstTime = False	
			if subClass2 == 'Samples':
				#no more conditions. Time to close Sinta rule 
				outSintaFile += ident(1) + u"ENTÃO sub-classe de cerveja = " + subClass1.encode('utf-8')

				for subClass3 in xml[root][str(beerClass)][subClass1][subClass2]:

					outOntFile += ident(1) + "<owl:NamedIndividual rdf:about=\"#" + subClass3.encode('utf-8') + "\">" + '\n'
					outOntFile += ident(2) + "<rdf:type rdf:resource=\"#" + subClass1.encode('utf-8') + "\"/>" + '\n'
					outOntFile += ident(2) + "<rdf:type rdf:resource=\"#" + beerClass.encode('utf-8') + "\"/>" + '\n'
					outOntFile += ident(1) + "</owl:NamedIndividual>" + '\n'

		
		outOntFile += '\n'
#closing rdf root tag
outOntFile +=  "</rdf:RDF>"

#writing in file
ontFile.write(outOntFile)
sintaFile.write(outSintaFile.encode('utf-8'))
