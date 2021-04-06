# A test Brick Schema for Boliou

from rdflib import RDF, RDFS, OWL, Namespace, Graph


g = Graph()

BOLIOU = Namespace("http://example.com/boliou#")
g.bind("boliou", BOLIOU)


BRICK = Namespace("https://brickschema.org/schema/Brick#")
g.bind("brick", BRICK)

g.add((BOLIOU["Room-021"], RDF.type, BRICK.Room))
g.add((BOLIOU["Room-022"], RDF.type, BRICK.Room))
g.add((BOLIOU["Room-055"], RDF.type, BRICK.Room))
g.add((BOLIOU["Room-059"], RDF.type, BRICK.Room))

g.add((BOLIOU["021-Room_Temp_Setpoint"], RDF.type, BRICK.Room_Air_Temperature_Setpoint))
g.add((BOLIOU["Room-021"], BRICK.hasPoint, BOLIOU["021-Room_Temp_Setpoint"]))




EVANS = Namespace("http://example.com/evans#")
g.bind("evans", EVANS)

g.add((EVANS["Room-120"], RDF.type, BRICK.Room))
g.add((EVANS["120-Room_Temp_Setpoint"], RDF.type, BRICK.Room_Air_Temperature_Setpoint))
g.add((EVANS["Room-120"], BRICK.hasPoint, EVANS["120-Room_Temp_Setpoint"]))
g.add((EVANS["120-Room_Temp"], RDF.type, BRICK.Room_Air_Temperature))
g.add((EVANS["Room-120"], BRICK.hasPoint, EVANS["120-Room_Temp"]))



g.add((EVANS["Room-122"], RDF.type, BRICK.Room))
g.add((EVANS["122-Room_Temp_Setpoint"], RDF.type, BRICK.Room_Air_Temperature_Setpoint))
g.add((EVANS["Room-122"], BRICK.hasPoint, EVANS["122-Room_Temp_Setpoint"]))
g.add((EVANS["122-Room_Temp"], RDF.type, BRICK.Room_Air_Temperature))
g.add((EVANS["Room-122"], BRICK.hasPoint, EVANS["122-Room_Temp"]))

g.add((EVANS["Room-G05"], RDF.type, BRICK.Room))
g.add((EVANS["Room-G16"], RDF.type, BRICK.Room))


with open("example.ttl", "wb") as f:
    # the Turtle format strikes a balance beteween being compact and easy to read
    f.write(g.serialize(format="ttl"))





