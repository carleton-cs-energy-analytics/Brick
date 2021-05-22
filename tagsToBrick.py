# This mapping maps the tag_id's in the database to BRICK objects (as well as their tag name).
# To check if all tags in the database have been mapped to BRICK objects,
#   run this program and it will output an array of tags that need to be mapped, if there are any
# Output is in the form (tag_id, tag_name) as a tuple
# Silas Monahan 4/2021

from rdflib import RDF, RDFS, OWL, Namespace, Graph
import psycopg2
from psycopg2 import connect, sql
from datetime import datetime
import json
import sys
import os

g = Graph()
BRICK = Namespace("https://brickschema.org/schema/Brick#")
g.bind("brick", BRICK)

point_types = []

conn = psycopg2.connect(
    host="localhost",
    database="energy",
    user="energy",
    password="less!29carbon")
cur = conn.cursor()

id_mapping = {
    1: {'Tag': 'Academic', 'BrickObj': BRICK.Building},
    2: {'Tag': 'Damper Command', 'BrickObj': BRICK.Damper_Command},
    3: {'Tag': 'Room Temperature', 'BrickObj': BRICK.Air_Temperature_Sensor},
    4: {'Tag': 'Residential', 'BrickObj': BRICK.Building},
    5: {'Tag': 'Room Temperature Setpoint Dial', 'BrickObj': BRICK.Room_Air_Temperature_Setpoint},
    6: {'Tag': 'Valve', 'BrickObj': BRICK.Valve},
    7: {'Tag': 'Night Override', 'BrickObj': BRICK.Override_Command},
    8: {'Tag': 'Night Cooling Setpoint', 'BrickObj': BRICK.Cooling_Temperature_Setpoint},
    9: {'Tag': 'Aux Temperature', 'BrickObj': BRICK.Air_Temperature_Sensor},
    10: {'Tag': 'Virtual Room Temperature Setpoint', 'BrickObj': BRICK.Room_Air_Temperature_Setpoint},
    11: {'Tag': 'Day Cooling Setpoint', 'BrickObj': BRICK.Cooling_Temperature_Setpoint},
    12: {'Tag': 'Heating Loopout', 'BrickObj': BRICK.Point}, # NEED TO FIX
    13: {'Tag': 'Cabinet Unit Heater', 'BrickObj': BRICK.Point}, # need to fix
    14: {'Tag': 'Flow', 'BrickObj': BRICK.Flow_Sensor},
    15: {'Tag': 'Valve Two Position', 'BrickObj': BRICK.Valve_Position_Sensor},
    16: {'Tag': 'Valve Two Command', 'BrickObj': BRICK.Valve_Command},
    17: {'Tag': 'Damper Position', 'BrickObj': BRICK.Damper_Position_Sensor},
    18: {'Tag': 'Duct Area', 'BrickObj': BRICK.Point}, # need to fix
    19: {'Tag': 'Valve One Command', 'BrickObj': BRICK.Valve_Command},
    20: {'Tag': 'Day Heating Setpoint', 'BrickObj': BRICK.Heating_Temperature_Setpoint},
    21: {'Tag': 'Controller Minimum Flow', 'BrickObj': BRICK.Point},
    22: {'Tag': 'Flow Setpoint', 'BrickObj': BRICK.Flow_Setpoint},
    23: {'Tag': 'Day/Night', 'BrickObj': BRICK.Point},
    24: {'Tag': 'Fan Coil Unit', 'BrickObj': BRICK.Fan_Coil_Unit},
    25: {'Tag': 'Valve Count', 'BrickObj': BRICK.Point},
    26: {'Tag': 'Valve One Position', 'BrickObj': BRICK.Valve_Position_Sensor},
    27: {'Tag': 'Controller Temperature', 'BrickObj': BRICK.Point},
    29: {'Tag': 'Hot Water Pump', 'BrickObj': BRICK.Hot_Water_Pump},
    30: {'Tag': 'Night Heating Setpoint', 'BrickObj': BRICK.Heating_Temperature_Setpoint},
    31: {'Tag': 'Cooling Minimum Flow', 'BrickObj': BRICK.Point},
    32: {'Tag': 'Cooling Maximum Flow', 'BrickObj': BRICK.Point},
    33: {'Tag': 'Domestic Circulating Pump', 'BrickObj': BRICK.Water_Pump},
    34: {'Tag': 'Heating/Cooling', 'BrickObj': BRICK.Point},
    36: {'Tag': 'Meter Setup', 'BrickObj': BRICK.Point},
    37: {'Tag': 'Air Volume', 'BrickObj': BRICK.VAV},
    39: {'Tag': 'Hot Water Return Temp', 'BrickObj': BRICK.Hot_Water_Return_Temperature_Sensor},
    40: {'Tag': 'Flow Coefficient', 'BrickObj': BRICK.Point},
    41: {'Tag': 'Heat Recovery Ventilator', 'BrickObj': BRICK.Point},
    42: {'Tag': 'Controller Maximum Flow', 'BrickObj': BRICK.Point},
    43: {'Tag': 'Cooling Loopout', 'BrickObj': BRICK.Point}, # need to fix
    44: {'Tag': 'Floor Temperature', 'BrickObj': BRICK.Temperature_Sensor},
    45: {'Tag': 'Heat Exchanger', 'BrickObj': BRICK.Heat_Exchanger},
    46: {'Tag': 'Floor Temperature Disable', 'BrickObj': BRICK.Disable_Fixed_Temperature_Command},
    48: {'Tag': 'Hot Water Supply Temp', 'BrickObj': BRICK.Hot_Water_Supply_Temperature_Sensor},
    49: {'Tag': 'Exhaust Set', 'BrickObj': BRICK.Exhaust_Air_Flow_Setpoint},
    50: {'Tag': 'Exhaust Air Flow Sensor', 'BrickObj': BRICK.Exhaust_Air_Flow_Sensor},
    51: {'Tag': 'Exhaust Damper', 'BrickObj': BRICK.Exhaust_Damper},
    53: {'Tag': 'Differential Set', 'BrickObj': BRICK.Setpoint},
    54: {'Tag': 'Flow Differential', 'BrickObj': BRICK.Flow_Sensor},
    55: {'Tag': 'Fume Flow Sensor', 'BrickObj': BRICK.Flow_Sensor},
    56: {'Tag': 'Alarm', 'BrickObj': BRICK.Alarm},
    57: {'Tag': 'Other Supply', 'BrickObj': BRICK.Point},
    58: {'Tag': 'Blast Freeze Alarm', 'BrickObj': BRICK.Alarm},
    59: {'Tag': 'Total Supply', 'BrickObj': BRICK.Point},
    60: {'Tag': 'Occupied', 'BrickObj': BRICK.Occupancy_Status},
    61: {'Tag': 'Max Air Supply', 'BrickObj': BRICK.Point},
    62: {'Tag': 'Supply Damper', 'BrickObj': BRICK.Damper},
    63: {'Tag': 'Supply Set', 'BrickObj': BRICK.Setpoint},
    64: {'Tag': 'Supply Air Flow Sensor', 'BrickObj': BRICK.Supply_Air_Flow_Sensor},
    65: {'Tag': 'Vacancy', 'BrickObj': BRICK.Occupancy_Status},
    66: {'Tag': 'Radiator DI 2', 'BrickObj': BRICK.Radiator},
    67: {'Tag': 'Radiator DI 3', 'BrickObj': BRICK.Radiator},
    68: {'Tag': 'Fan', 'BrickObj': BRICK.Fan},
    69: {'Tag': 'Valve One Command', 'BrickObj': BRICK.Valve_Command},
    70: {'Tag': 'Valve Two Position', 'BrickObj': BRICK.Valve_Position_Sensor},
    71: {'Tag': 'Chilled Water', 'BrickObj': BRICK.Chilled_Water},
    72: {'Tag': 'Chilled Water Flow', 'BrickObj': BRICK.Water_Flow_Sensor},
    73: {'Tag': 'Domestic Water Return Temperature Sensor', 'BrickObj': BRICK.Domestic_Hot_Water_Return_Temperature_Sensor},
    74: {'Tag': 'Hot Water Flow', 'BrickObj': BRICK.Hot_Water_Flow_Sensor},
    75: {'Tag': 'Domestic Water', 'BrickObj': BRICK.Domestic_Water},
    76: {'Tag': 'Domestic Water Supply Temperature Sensor', 'BrickObj': BRICK.Domestic_Hot_Water_Supply_Temperature_Sensor},
    77: {'Tag': 'Electricity Use', 'BrickObj': BRICK.Building_Electrical_Meter},
    78: {'Tag': 'Electricity Demand', 'BrickObj': BRICK.Electrical_Power_Sensor},
    79: {'Tag': 'Electricity Meter Reading', 'BrickObj': BRICK.Electrical_Power_Sensor},
    80: {'Tag': 'Water Meter Reading', 'BrickObj': BRICK.Building_Water_Meter},
    81: {'Tag': 'Hot Water Alarm', 'BrickObj': BRICK.Supply_Water_Temperature_Alarm},
    82: {'Tag': 'Hot Water', 'BrickObj': BRICK.Hot_Water},
    83: {'Tag': 'Last Months Electricity Consumption', 'BrickObj': BRICK.Energy_Usage_Sensor},
    84: {'Tag': 'Last Months Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    85: {'Tag': 'Last Months Steam Consumption', 'BrickObj': BRICK.Steam_Usage_Sensor},
    86: {'Tag': 'Last Weeks Electricity Consumption', 'BrickObj': BRICK.Energy_Usage_Sensor},
    87: {'Tag': 'Last Weeks Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    88: {'Tag': 'Last Weeks Steam Consumption', 'BrickObj': BRICK.Steam_Usage_Sensor},
    89: {'Tag': 'This Months Electricity Consumption', 'BrickObj': BRICK.Energy_Usage_Sensor},
    90: {'Tag': 'This Months Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    91: {'Tag': 'This Months Steam Consumption', 'BrickObj': BRICK.Steam_Usage_Sensor},
    92: {'Tag': 'Steam Demand', 'BrickObj': BRICK.Steam_Usage_Sensor},
    93: {'Tag': 'Steam', 'BrickObj': BRICK.Steam},
    94: {'Tag': 'Todays Electricity Consumption', 'BrickObj': BRICK.Energy_Usage_Sensor},
    95: {'Tag': 'Todays Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    96: {'Tag': 'Todays Steam Consumption', 'BrickObj': BRICK.Steam_Usage_Sensor},
    97: {'Tag': 'Trench Alarm', 'BrickObj': BRICK.Alarm},
    98: {'Tag': 'Sump Pump', 'BrickObj': BRICK.Water_Pump},
    99: {'Tag': 'Water Demand', 'BrickObj': BRICK.Water_Meter},
    100: {'Tag': 'Water High Point', 'BrickObj': BRICK.Water_Level_Sensor},
    101: {'Tag': 'Water Highest Flow', 'BrickObj': BRICK.Water_Flow_Sensor},
    102: {'Tag': 'Water Low Point', 'BrickObj': BRICK.Water_Level_Sensor},
    103: {'Tag': 'Water Lowest Flow', 'BrickObj': BRICK.Water_Flow_Sensor},
    104: {'Tag': 'This Weeks Electricity Consumption', 'BrickObj': BRICK.Energy_Usage_Sensor},
    105: {'Tag': 'This Weeks Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    106: {'Tag': 'This Weeks Steam Consumption', 'BrickObj': BRICK.Steam_Usage_Sensor},
    107: {'Tag': 'Yesterdays Electricity Consumption', 'BrickObj': BRICK.Energy_Usage_Sensor},
    108: {'Tag': 'Yesterdays Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    109: {'Tag': 'Yesterdays Steam Consumption', 'BrickObj': BRICK.Steam_Usage_Sensor},
    110: {'Tag': 'Maximum Temperature Setpoint', 'BrickObj': BRICK.Max_Air_Temperature_Setpoint},
    111: {'Tag': 'Minimum Temperature Setpoint', 'BrickObj': BRICK.Min_Air_Temperature_Setpoint},
    112: {'Tag': 'Other', 'BrickObj': BRICK.Point},
    114: {'Tag': 'Setpoint', 'BrickObj': BRICK.Setpoint},
    115: {'Tag': 'Heating Valve', 'BrickObj': BRICK.Heating_Valve},
    119: {'Tag': 'Last Months Domestic Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    120: {'Tag': 'Last Weeks Domestic Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    121: {'Tag': 'Local Point', 'BrickObj': BRICK.Point},
    122: {'Tag': 'This Months Domestic Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    123: {'Tag': 'Todays Domestic Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    124: {'Tag': 'This Weeks Domestic Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    125: {'Tag': 'Yesterdays Domestic Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    127: {'Tag': 'Domestic Water Consumption', 'BrickObj': BRICK.Water_Usage_Sensor},
    128: {'Tag': 'CO2 Monitor', 'BrickObj': BRICK.CO2_Sensor},
    131: {'Tag': 'Hall Lights', 'BrickObj': BRICK.Lighting_Equipment},
    133: {'Tag': 'Hot Water Supply Temp Setpoint', 'BrickObj': BRICK.Supply_Hot_Water_Temperature_Setpoint},
    134: {'Tag': 'Heat Tape', 'BrickObj': BRICK.Trace_Heat_Sensor},
    138: {'Tag': 'Average Hot Water Supply Temp', 'BrickObj': BRICK.Hot_Water_Supply_Temperature_Sensor},
    139: {'Tag': 'Speed Output', 'BrickObj': BRICK.Speed_Status},
    141: {'Tag': 'Irrigation Meter', 'BrickObj': BRICK.Water_Meter},
    142: {'Tag': 'Consumption', 'BrickObj': BRICK.Usage_Sensor},
    143: {'Tag': 'DEM Consumption High', 'BrickObj': BRICK.Usage_Sensor},
    144: {'Tag': 'DEM Consumption Low', 'BrickObj': BRICK.Usage_Sensor},
    151: {'Tag': 'Drain Pan', 'BrickObj': BRICK.Point},
    152: {'Tag': 'Average Steam', 'BrickObj': BRICK.Steam_Usage_Sensor},
    163: {'Tag': 'Steam Valve', 'BrickObj': BRICK.Steam_Valve}
}

tag_query = '''SELECT tag_id, name FROM tags'''
cur.execute(tag_query)
tags = cur.fetchall()
cur.close()

no_mapping = []
wrong_name = []

for tag in tags:
    id = tag[0]
    name = tag[1]
    if id not in id_mapping.keys():
        no_mapping.append(tag)
    elif (name != id_mapping[id]['Tag']):
        wrong_name.append(name + ' (tag: ' + str(id) + ')')

if(len(no_mapping) > 0):
    print("These tags are in the database but are not in this mapping: ")
    print(no_mapping)
if(len(wrong_name) > 0):
    print("These tags are in the mapping but do not have the correct tag name: ")
    print(wrong_name)

if(len(wrong_name) == 0 and len(no_mapping) == 0):
    print("All tags in the database are mapped correctly")
