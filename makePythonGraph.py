import json
import psycopg2

from tagsToBrick import id_mapping

conn = psycopg2.connect(
    host="localhost",
    database="energy",
    user="energy",
    password="less!29carbon")
cur = conn.cursor()

def addBuilding(building_name):
    building_name = building_name.replace(" ", "*")
    building_name_spaces = building_name.replace("*", " ")
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
        graph[floor_name] = []
        addEdge(graph, building_name, floor_map[floor])
    
    # Creates all brick rooms that are in the database for this building
    for room in rooms:
        if room[0:6] == "UnID'd":
            room_name = "No-Room"
            graph[room_name] = []
            graph["No-Floor"].append(room_name)
            continue
        room_name_spaces = room
        room_name = room.replace(" ", "*")
        graph[room_name] = []
        cur.execute('''SELECT floor FROM rooms WHERE name = '{0}' '''.format(room_name_spaces))
        floor = cur.fetchone()[0]
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
        pointObj = [tag, point_name]
        addEdge(graph, room_name, pointObj)
        
        

def addEdge(graph,u,v):
    graph[u].append(v)

# Creates graph

graph = {}

# Adds Boliou to the graph
addBuilding("Boliou")

print(graph)
'''
# Adds Evans to the graph
addBuilding("Evans")

# Adds Hulings to the graph
addBuilding("Hulings")

# Adds Townhouses to the graph
addBuilding("Townhouses")

# Adds Weitz to the graph
addBuilding("Weitz")

# Adds Cassat to the graph
addBuilding("Cassat")
'''

# Doesnt like the unid'd buldings
'''
addBuilding("UnID''d Building")
'''

json = json.dumps(graph)
f = open("pythonGraph.json","w")
f.write(json)
f.close()

