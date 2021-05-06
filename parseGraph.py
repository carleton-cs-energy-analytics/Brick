filename = 'Carleton.ttl' 
import rdflib

g = rdflib.Graph()

result = g.parse(filename, format='ttl')
print(result)
query = '''SELECT ?Rm  WHERE { ?Rm rdf:type brick:Room .}'''

g.query(query)
for stmt in g:
    print(stmt)