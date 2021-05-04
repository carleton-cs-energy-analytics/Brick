from rdflib import RDF, RDFS, OWL, Namespace, Graph
import json
import psycopg2

from tagsToBrick import id_mapping

conn = psycopg2.connect(
    host="localhost",
    database="energy",
    user="energy",
    password="less!29carbon")
cur = conn.cursor()

def addEdge(graph,u,v):
    graph[u].append(v)

def brickifyBuilding(building_name, BRICK_BUILDING):
    building_name = building_name.replace(" ", "*")
    building_name_spaces = building_name.replace("*", " ")
    # Brick Graph
    g.add((BRICK_BUILDING[building_name], RDF.type, BRICK.Building))
    # Python graph 
    graph[building_name] = []

    building_query = '''SELECT building_id FROM buildings WHERE name = '{0}' '''.format(building_name_spaces)
    cur.execute(building_query)
    building_id = cur.fetchone()
    
    # Tests if the inputted building matches a building in the database
    if(building_id != None):
        building_id = building_id[0]
    else:
        print("ERROR: " + building_name + " is not a building in the database. Make sure you inputted spelled the name correctly")
        return
    
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
        0: "Ground-Floor",
        1: "First-Floor",
        2: "Second-Floor",
        3: "Third-Floor",
        4: "Fourth-Floor",
        5: "Fifth-Floor",
        None: "No-Floor"
    }
    
    # Creates all brick floors that are in the database for this building
    for floor in floors:
        floor_name = floor_map[floor]
        # Brick graph
        g.add((BRICK_BUILDING[floor_name], RDF.type, BRICK.Floor))
        g.add((BRICK_BUILDING[building_name], BRICK.hasPart, BRICK_BUILDING[floor_name]))
        # Python graph
        graph[floor_name] = []
        addEdge(graph, building_name, floor_map[floor])

    # Creates all brick rooms that are in the database for this building
    for room in rooms:
        if room[0:6] == "UnID'd":
            room_name = "No-Room"
            # Brick graph
            g.add((BRICK_BUILDING[room_name], RDF.type, BRICK.Room))
            g.add((BRICK_BUILDING["No-Floor"], BRICK.hasPart, BRICK_BUILDING[room_name]))
            # Python graph
            graph[room_name] = []
            addEdge(graph, floor_map[floor], room_name)
            continue
        room_name_spaces = room
        room_name = room.replace(" ", "*")
        cur.execute('''SELECT floor FROM rooms WHERE name = '{0}' '''.format(room_name_spaces))
        floor = cur.fetchone()[0]
        # Brick graph 
        g.add((BRICK_BUILDING[room_name], RDF.type, BRICK.Room))
        g.add((BRICK_BUILDING[floor_map[floor]], BRICK.hasPart, BRICK_BUILDING[room_name]))
        # Python Graph
        graph[room_name] = []
        addEdge(graph, floor_map[floor], room_name)
        

    # Creates all brick points that are in the database for this building
    for point in points:
        point_name = point[0].replace(" ", "*")
        tag_id = point[2]
        room_name = point[4].replace(" ", "*")
        if len(room_name) > 4:
            if room_name[0:4] == "UnID":
                room_name = "No-Room"
        tag = id_mapping[tag_id]['Tag']
        brick_obj = id_mapping[tag_id]['BrickObj']
        # Brick Graph
        g.add((BRICK_BUILDING[point_name], RDF.type, brick_obj))
        g.add((BRICK_BUILDING[room_name], BRICK.hasPoint, BRICK_BUILDING[point_name]))
        # Python Graph
        pointObj = [tag, point_name]
        addEdge(graph, room_name, pointObj)

# Creates graph
graph = {} # python graph
g = Graph() # Brick graph
BRICK = Namespace("https://brickschema.org/schema/Brick#")
g.bind("brick", BRICK)

# Adds Boliou to the brick schema
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

# Adds Townhouses to the brick schema
TOWNHOUSES = Namespace("http://example.com/townhouses#")
g.bind("townhouses", TOWNHOUSES)
brickifyBuilding("Townhouses", TOWNHOUSES)

# Adds Weitz to the brick schema
WEITZ = Namespace("http://example.com/weitz#")
g.bind("weitz", WEITZ)
brickifyBuilding("Weitz", WEITZ)

# Adds Cassat to the brick schema
CASSAT = Namespace("http://example.com/cassat#")
g.bind("cassat", CASSAT)
brickifyBuilding("Cassat", CASSAT)

# Doesnt like the unid'd buldings
'''
UNID = Namespace("http://example.com/unid'd#")
g.bind("UnID'd", UNID)
brickifyBuilding("UnID''d Building", UNID)
'''

# output brick schema to Carleton2.ttl
with open("Carleton2.ttl", "wb") as f:
    # the Turtle format strikes a balance beteween being compact and easy to read
    f.write(g.serialize(format="ttl"))

# Create json file for python graph
json = json.dumps(graph)
f = open("pythonGraph.json","w")
f.write(json)
f.close()

