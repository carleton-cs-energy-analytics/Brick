# A test Brick Schema for Boliou

from rdflib import RDF, RDFS, OWL, Namespace, Graph
import psycopg2
from psycopg2 import connect, sql
from datetime import datetime
import sys
import os

conn = psycopg2.connect(
    host="localhost",
    database="energy",
    user="energy",
    password="less!29carbon")
cur = conn.cursor()
points_query = '''SELECT * FROM points'''
cur.execute(points_query)
points = cur.fetchall()
point_names = []
for line in points:
  point_names.append(line[1].split('.'))
print(point_names[0])



g = Graph()

BOLIOU = Namespace("http://example.com/boliou#")
g.bind("boliou", BOLIOU)


BRICK = Namespace("https://brickschema.org/schema/Brick#")
g.bind("brick", BRICK)


g.add((BOLIOU["Boliou"], RDF.type, BRICK.Building))

g.add((BOLIOU["Ground-Floor"], RDF.type, BRICK.Floor))
g.add((BOLIOU["Boliou"], BRICK.hasPart, BOLIOU["Ground-Floor"]))
g.add((BOLIOU["First-Floor"], RDF.type, BRICK.Floor))
g.add((BOLIOU["Boliou"], BRICK.hasPart, BOLIOU["First-Floor"]))

g.add((BOLIOU["Room-021"], RDF.type, BRICK.Room))
g.add((BOLIOU["Ground-Floor"], BRICK.hasPart, BOLIOU["Room-021"]))
g.add((BOLIOU["Room-022"], RDF.type, BRICK.Room))
g.add((BOLIOU["Ground-Floor"], BRICK.hasPart, BOLIOU["Room-022"]))
g.add((BOLIOU["Room-155"], RDF.type, BRICK.Room))
g.add((BOLIOU["First-Floor"], BRICK.hasPart, BOLIOU["Room-155"]))
g.add((BOLIOU["Room-159"], RDF.type, BRICK.Room))
g.add((BOLIOU["First-Floor"], BRICK.hasPart, BOLIOU["Room-159"]))

g.add((BOLIOU["021-Room_Temp_Setpoint"], RDF.type, BRICK.Room_Air_Temperature_Setpoint))
g.add((BOLIOU["Room-021"], BRICK.hasPoint, BOLIOU["021-Room_Temp_Setpoint"]))

for i in range(len(point_names)):
  if point_names[i][0] == "BO":
    if "RM155" in point_names[i][2]:
      print(point_names[i][2])
      g.add((BOLIOU[point_names[i][2].replace(" ", "_")], RDF.type, BRICK.Location))
      g.add((BOLIOU["Room-155"], BRICK.hasPart, BOLIOU[point_names[i][2].replace(" ", "_")]))


EVANS = Namespace("http://example.com/evans#")
g.bind("evans", EVANS)

g.add((EVANS["Evans"], RDF.type, BRICK.Building))

g.add((EVANS["Ground-Floor"], RDF.type, BRICK.Floor))
g.add((EVANS["Evans"], BRICK.hasPart, EVANS["Ground-Floor"]))
g.add((EVANS["First-Floor"], RDF.type, BRICK.Floor))
g.add((EVANS["Evans"], BRICK.hasPart, EVANS["First-Floor"]))

g.add((EVANS["Room-120"], RDF.type, BRICK.Room))
g.add((EVANS["First-Floor"], BRICK.hasPart, EVANS["Room-120"]))
g.add((EVANS["120-Room_Temp_Setpoint"], RDF.type, BRICK.Room_Air_Temperature_Setpoint))
g.add((EVANS["Room-120"], BRICK.hasPoint, EVANS["120-Room_Temp_Setpoint"]))
g.add((EVANS["120-Room_Temp"], RDF.type, BRICK.Room_Air_Temperature))
g.add((EVANS["Room-120"], BRICK.hasPoint, EVANS["120-Room_Temp"]))


g.add((EVANS["Room-122"], RDF.type, BRICK.Room))
g.add((EVANS["First-Floor"], BRICK.hasPart, EVANS["Room-122"]))
g.add((EVANS["122-Room_Temp_Setpoint"], RDF.type, BRICK.Room_Air_Temperature_Setpoint))
g.add((EVANS["Room-122"], BRICK.hasPoint, EVANS["122-Room_Temp_Setpoint"]))
g.add((EVANS["122-Room_Temp"], RDF.type, BRICK.Room_Air_Temperature))
g.add((EVANS["Room-122"], BRICK.hasPoint, EVANS["122-Room_Temp"]))

g.add((EVANS["Room-G05"], RDF.type, BRICK.Room))
g.add((EVANS["Ground-Floor"], BRICK.hasPart, EVANS["Room-G05"]))
g.add((EVANS["Room-G16"], RDF.type, BRICK.Room))
g.add((EVANS["Ground-Floor"], BRICK.hasPart, EVANS["Room-G16"]))


with open("example.ttl", "wb") as f:
    # the Turtle format strikes a balance beteween being compact and easy to read
    f.write(g.serialize(format="ttl"))
