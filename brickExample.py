file1 = open('Carleton.ttl', 'r')

boliou_rooms = []
evans_rooms = []
for line in file1:
    line.replace("*", " ")
    if "brick:Room" in line:
        if "boliou" in line:
            boliou_rooms.append(line.split(" ")[0].split(":")[1])
        elif "evans" in line:
            evans_rooms.append(line.split(" ")[0].split(":")[1])

file1.close()

print("\n Rooms in Boliou: \n")
print(boliou_rooms)
print("\n Rooms in Evans: \n")
print(evans_rooms)

print("\n Pulling points from arbitrary room in Evans example: \n")

file2 = open('Carleton.ttl', 'r')

found = False
room_points = []
for line in file2:
    if evans_rooms[5] in line and "hasPart" in line:
        found = True
        room_points.append(line[8:].split(" ")[1].split(",")[0])
    elif found == True:
        if "," in line:
            room_points.append(line[8:].split(",")[0])  
        elif line == "\n":
            found = False
        else:
            found = False
            room_points.append(line[8:].split(" ")[0])
room_points = set(room_points)
room_points = list(room_points)
print("\n Points found in " + evans_rooms[5] + ": \n")
print(room_points)

file2.close()
