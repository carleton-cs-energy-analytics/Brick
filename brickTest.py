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
for i in range(len(points)):
  point_names.append(points[i][1].split('.'))

g = Graph()
BRICK = Namespace("https://brickschema.org/schema/Brick#")
g.bind("brick", BRICK)
BOLIOU = Namespace("http://example.com/boliou#")
g.bind("boliou", BOLIOU)
g.add((BOLIOU["Boliou"], RDF.type, BRICK.Building))
boliou_rooms = []

for i in range(len(point_names)):
  if point_names[i][0] == "BO":
    try:
      point_name = point_names[i][2].split(':')
      boliou_rooms.append(point_name[0])
    except Exception as e:
      print(e)

boliou_rooms = set(boliou_rooms)
boliou_rooms = list(boliou_rooms)

g.add((BOLIOU["Ground-Floor"], RDF.type, BRICK.Floor))
g.add((BOLIOU["Boliou"], BRICK.hasPart, BOLIOU["Ground-Floor"]))
g.add((BOLIOU["First-Floor"], RDF.type, BRICK.Floor))
g.add((BOLIOU["Boliou"], BRICK.hasPart, BOLIOU["First-Floor"]))
for i in range(len(boliou_rooms)):
  if boliou_rooms[i][2] == '0':
    g.add((BOLIOU[boliou_rooms[i]], RDF.type, BRICK.Room))
    g.add((BOLIOU["Ground-Floor"], BRICK.hasPart, BOLIOU[boliou_rooms[i]]))
  if boliou_rooms[i][2] == '1':
    g.add((BOLIOU[boliou_rooms[i]], RDF.type, BRICK.Room))
    g.add((BOLIOU["First-Floor"], BRICK.hasPart, BOLIOU[boliou_rooms[i]]))    

for i in range(len(point_names)):
  if point_names[i][0] == "BO":
    for room in boliou_rooms:
      if room == point_names[i][2][0:5]:
        print("Added point " + point_names[i][2] + " to room " + room)
        g.add((BOLIOU[points[i][1].replace(" ", "*")], RDF.type, BRICK.Value))
        g.add((BOLIOU[room], BRICK.hasPart, BOLIOU[points[i][1].replace(" ", "*")]))


EVANS = Namespace("http://example.com/evans#")
g.bind("evans", EVANS)
g.add((EVANS["Evans"], RDF.type, BRICK.Building))
evans_rooms = []
for i in range(len(point_names)):
  if point_names[i][0] == "EV":
    try:
      room_name = point_names[i][1]
      if room_name not in evans_rooms:
        if room_name[0:2] == 'RM':
          evans_rooms.append(room_name)
    except Exception as e:
      print(e)

g.add((EVANS["Ground-Floor"], RDF.type, BRICK.Floor))
g.add((EVANS["Evans"], BRICK.hasPart, EVANS["Ground-Floor"]))
g.add((EVANS["First-Floor"], RDF.type, BRICK.Floor))
g.add((EVANS["Evans"], BRICK.hasPart, EVANS["First-Floor"]))
g.add((EVANS["Second-Floor"], RDF.type, BRICK.Floor))
g.add((EVANS["Evans"], BRICK.hasPart, EVANS["Second-Floor"]))
g.add((EVANS["Third-Floor"], RDF.type, BRICK.Floor))
g.add((EVANS["Evans"], BRICK.hasPart, EVANS["Third-Floor"]))
g.add((EVANS["Fourth-Floor"], RDF.type, BRICK.Floor))
g.add((EVANS["Evans"], BRICK.hasPart, EVANS["Fourth-Floor"]))

for i in range(len(evans_rooms)):
  try:
    if evans_rooms[i][2] == 'G':
      g.add((BOLIOU[evans_rooms[i].replace(" ", "*")], RDF.type, BRICK.Room))
      g.add((EVANS["Ground-Floor"], BRICK.hasPart, EVANS[evans_rooms[i].replace(" ", "*")]))
    if evans_rooms[i][2] == '1':
      g.add((EVANS[evans_rooms[i].replace(" ", "*")], RDF.type, BRICK.Room))
      g.add((EVANS["First-Floor"], BRICK.hasPart, EVANS[evans_rooms[i].replace(" ", "*")]))
    if evans_rooms[i][2] == '2':
      g.add((EVANS[evans_rooms[i].replace(" ", "*")], RDF.type, BRICK.Room))
      g.add((EVANS["Second-Floor"], BRICK.hasPart, EVANS[evans_rooms[i].replace(" ", "*")]))  
    if evans_rooms[i][2] == '3':
      g.add((EVANS[evans_rooms[i].replace(" ", "*")], RDF.type, BRICK.Room))
      g.add((EVANS["Third-Floor"], BRICK.hasPart, EVANS[evans_rooms[i].replace(" ", "*")]))  
    if evans_rooms[i][2] == '4':
      g.add((EVANS[evans_rooms[i].replace(" ", "*")], RDF.type, BRICK.Room))
      g.add((EVANS["Fourth-Floor"], BRICK.hasPart, EVANS[evans_rooms[i].replace(" ", "*")]))  
  except Exception as e:
    print(e)

for i in range(len(point_names)):
  if point_names[i][0] == "EV":
    for room in evans_rooms:
      if room == point_names[i][1]:
        print("Added point " + points[i][1] + " to room " + room)
        g.add((EVANS[points[i][1].replace(" ", "*")], RDF.type, BRICK.Value))
        g.add((EVANS[room], BRICK.hasPart, EVANS[points[i][1].replace(" ", "*")]))

with open("Carleton.ttl", "wb") as f:
    # the Turtle format strikes a balance beteween being compact and easy to read
    f.write(g.serialize(format="ttl"))
