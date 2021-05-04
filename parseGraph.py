filename = 'Carleton2.ttl' 
import rdflib

g = rdflib.Graph()

result = g.parse(filename, format='ttl')
print(result)
query = '''SELECT ?Rm  WHERE { ?Rm rdf:type brick:Room .}'''

g.query(query)
for stmt in g:
    print(stmt)

'''
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON

g = Graph()

result = g.parse('Carleton2.ttl', format="turtle")
sparql = SPARQLWrapper("http://example.com/boliou#")





sparql.setQuery(queryString)

ret = sparql.query()

print(ret)

#print(result.query(queryString).get_value()) #WHERE {?sensor rdf:type/rdfs:subClassOf* brick:Zone_Temperature_Sensor}))
'''
#queryString = '''SELECT ?Rm  WHERE { ?Rm rdf:type brick:Room .}'''

