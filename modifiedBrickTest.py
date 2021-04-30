from rdflib import RDF, RDFS, OWL, Namespace, Graph
import psycopg2
from psycopg2 import connect, sql
from datetime import datetime
import sys
import os

from tagsToBrick import id_mapping

conn = psycopg2.connect(
    host="localhost",
    database="energy",
    user="energy",
    password="less!29carbon")
cur = conn.cursor()

def brickifyBuilding(building_name, BRICK_BUILDING):
    g.add((BRICK_BUILDING[building_name], RDF.type, BRICK.Building))
    building_query = '''SELECT building_id FROM buildings WHERE name = '{0}' '''.format(building_name)
    cur.execute(building_query)
    building_id = cur.fetchone()
    
    # Tests if the inputted building matches a building in the database
    if(building_id != None):
        building_id = building_id[0]
    else:
        print("ERROR: " + building_name + " is not a building in the database. Make sure you inputted spelled the name correctly")
        return
    print(building_id)

    #(point_name, point_id, tag_id, room_id, room_name, floor)
    all_point_info_query = '''SELECT P.name, P.point_id, T.tag_id, R.room_id, R.name, R.floor FROM ((points as P JOIN points_tags as T ON P.point_id = T.point_id) JOIN devices AS D ON P.device_id=D.device_id) JOIN rooms as R ON R.room_id = D.room_id WHERE building_id = {0}'''.format(building_id)
    cur.execute(all_point_info_query)
    points = cur.fetchall()

    floors = []
    rooms = []
    # Loops through points and gets all unique rooms and points in the set
    for point in points:
        floor = point[5]
        if floor not in floors:
            floors.append(floor)
        room = point[4]
        if room not in rooms:
            rooms.append(room)

    # Maps floor numbers to their name
    floor_map = {
        -1: "Basement",
        0: "Ground",
        1: "First",
        2: "Second",
        3: "Third",
        4: "Fourth",
        5: "Fifth"
    }

    # Creates all brick floors that are in the database for this building
    for floor in floors:
        if floor == None:
            floor_name = "No-Floor"
        elif floor == -1:
            floor_name = "Basement"
        else:
            floor_name = floor_map[floor] + "-Floor"
        g.add((BRICK_BUILDING[floor_name], RDF.type, BRICK.Floor))
        g.add((BRICK_BUILDING[building_name], BRICK.hasPart, BRICK_BUILDING[floor_name]))

    # Creates all brick rooms that are in the database for this building
    for room in rooms:
        if room[0:6] == "UnID'd":
            room_name = 'Unidentified'
            g.add((BRICK_BUILDING[room_name], RDF.type, BRICK.Room))
            g.add((BRICK_BUILDING["No-Floor"], BRICK.hasPart, BRICK_BUILDING[room_name]))
            continue
        else:
            room_name = room
        g.add((BRICK_BUILDING[room_name], RDF.type, BRICK.Room))
        cur.execute('''SELECT floor FROM rooms WHERE name = '{0}' '''.format(room_name))
        floor = int(cur.fetchall()[0][0])
        if(floor == -1):
            g.add((BRICK_BUILDING["Basement"], BRICK.hasPart, BRICK_BUILDING[room_name]))
        else:
            g.add((BRICK_BUILDING[floor_map[floor] + "-Floor"], BRICK.hasPart, BRICK_BUILDING[room_name]))

    # Creates all brick points that are in the database for this building
    for point in points:
        point_name = point[0].replace(" ", "_")
        tag_id = point[2]
        room_name = point[4]
        if len(room_name) > 4:
            if room_name[0:4] == "UnID":
                room_name = "No-Floor"
        brick_obj = id_mapping[tag_id]['BrickObj']
        g.add((BRICK_BUILDING[point_name], RDF.type, brick_obj))
        g.add((BRICK_BUILDING[room_name], BRICK.hasPoint, BRICK_BUILDING[point_name]))

# Creates graph
g = Graph()
BRICK = Namespace("https://brickschema.org/schema/Brick#")
g.bind("brick", BRICK)

# Adds hulings to the brick schema
BOLIOU = Namespace("http://example.com/boliou#")
g.bind("boliou", BOLIOU)
brickifyBuilding("Boliou", BOLIOU)

# Adds Evans to the brick schema
EVANS = Namespace("http://example.com/evans#")
g.bind("evans", EVANS)
brickifyBuilding("Evans", EVANS)

# Adds Hulings to the brick schema
HULINGS = Namespace("http://example.com/hulings#")
g.bind("hulings", HULINGS)
brickifyBuilding("Hulings", HULINGS)

with open("Carleton2.ttl", "wb") as f:
    # the Turtle format strikes a balance beteween being compact and easy to read
    f.write(g.serialize(format="ttl"))

