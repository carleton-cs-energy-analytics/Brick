# A test Brick Schema for Boliou

from rdflib import RDF, RDFS, OWL, Namespace, Graph
import psycopg2
from psycopg2 import connect, sql
from datetime import datetime
import sys
import os
import urllib.parse

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

'''
g.add((BOLIOU[boliou_rooms[i]], RDF.type, BRICK.Room))
g.add((BOLIOU["Ground-Floor"], BRICK.hasPart, BOLIOU["RM021"]))
g.add((BOLIOU["RM021"], RDF.type, BRICK.Room))
g.add((BOLIOU["Ground-Floor"], BRICK.hasPart, BOLIOU["RM021"]))
g.add((BOLIOU["RM022"], RDF.type, BRICK.Room))
g.add((BOLIOU["Ground-Floor"], BRICK.hasPart, BOLIOU["RM022"]))
g.add((BOLIOU["RM155"], RDF.type, BRICK.Room))
g.add((BOLIOU["First-Floor"], BRICK.hasPart, BOLIOU["RM155"]))
g.add((BOLIOU["RM159"], RDF.type, BRICK.Room))
g.add((BOLIOU["First-Floor"], BRICK.hasPart, BOLIOU["RM159"]))
g.add((BOLIOU["021-Room_Temp_Setpoint"], RDF.type, BRICK.Room_Air_Temperature_Setpoint))
g.add((BOLIOU["RM021"], BRICK.hasPoint, BOLIOU["021-Room_Temp_Setpoint"]))
'''

for i in range(len(point_names)):
  if point_names[i][0] == "BO":
    for room in boliou_rooms:
      room_name = point_names[i][2].split(':')[0]
      if room == room_name:
        print("Added point " + points[i][1] + "to room " + room)
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
'''
g.add((EVANS["RM120"], RDF.type, BRICK.Room))
g.add((EVANS["First-Floor"], BRICK.hasPart, EVANS["RM120"]))
g.add((EVANS["120-Room_Temp_Setpoint"], RDF.type, BRICK.Room_Air_Temperature_Setpoint))
g.add((EVANS["RM120"], BRICK.hasPoint, EVANS["120-Room_Temp_Setpoint"]))
g.add((EVANS["120-Room_Temp"], RDF.type, BRICK.Room_Air_Temperature))
g.add((EVANS["RM120"], BRICK.hasPoint, EVANS["120-Room_Temp"]))


g.add((EVANS["RM122"], RDF.type, BRICK.Room))
g.add((EVANS["First-Floor"], BRICK.hasPart, EVANS["RM122"]))
g.add((EVANS["122-Room_Temp_Setpoint"], RDF.type, BRICK.Room_Air_Temperature_Setpoint))
g.add((EVANS["RM122"], BRICK.hasPoint, EVANS["122-Room_Temp_Setpoint"]))
g.add((EVANS["122-Room_Temp"], RDF.type, BRICK.Room_Air_Temperature))
g.add((EVANS["RM122"], BRICK.hasPoint, EVANS["122-Room_Temp"]))

g.add((EVANS["RMG05"], RDF.type, BRICK.Room))
g.add((EVANS["Ground-Floor"], BRICK.hasPart, EVANS["RMG05"]))
g.add((EVANS["RMG16"], RDF.type, BRICK.Room))
g.add((EVANS["Ground-Floor"], BRICK.hasPart, EVANS["RMG16"]))
'''

for i in range(len(point_names)):
  if point_names[i][0] == "EV":
    for room in evans_rooms:
      if room in points[i][1]:
        print("Added point " + points[i][1] + " to room " + room)
        point = urllib.parse.quote_plus(points[i][1])
        g.add((EVANS[point], RDF.type, BRICK.Value))
        g.add((EVANS[room], BRICK.hasPart, EVANS[point]))

with open("Carleton.ttl", "wb") as f:
    # the Turtle format strikes a balance beteween being compact and easy to read
    f.write(g.serialize(format="ttl"))
