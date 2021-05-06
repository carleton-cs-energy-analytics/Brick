# Brick
Respository for managing the Brick Schema for Carleton's Campus. 

Docs pages for Brick Schema located here: https://brickschema.org/

## Brick Graph Constructor
The **makeBrick.py** script generates an RDF Graph of Brick objects in *Carleton2.ttl* which puts all of the points in all buildings in the database with their respective dependencies into a Graph. Each point is associated with its corresponding room, each room with its corresponding floor, floor with building, etc. Each point is also categorized as a specific Brick object instead of just the generic Point object. To see a visualization of this graph upload the '.ttl' file here: https://brickschema.github.io/brick-studio/.

This script also generates a python graph (dictionary format) and outputs it into *pythonGraph.json*, a json file that stores the python graph.

**parseGraph.py** parses *Carleton2.ttl* (right now it just finds all the rooms), but does not have any analysis associated with it. You must parse the .ttl file with SPARQL, which we have not looked into much but some documentation is here: https://www.w3.org/TR/rdf-sparql-query/#basicpatterns.

**tagsToBrick.py** maps tag_id's to both their tag names and their associated Brick objects. You can run this file to test if all tags in the database have been mapped to Brick objects, but this also automatically happens whenever you run *makeBrick.py*.

An advantage to this approach to getting point names is that someone does not need to look through the database and manually find all point names associated with a building, floor or room. Instead, they can iterate over the dependencies here. One thing of note is that the RDF format does not accept the character " ", so any " " characters in point names are replaced with "\*". Therefore of you want to go backwards and input any point name from this graph into the database as a query, you will have to replace all "\*" with " ".

TODO: This isn't in any repository, but making it so that all point names in the database don't contain the character " " would help a lot with the organization here. Similarly, point name formats really vary building to building and even within buildings. Simplifications of that on the database end will very much simplify the addition of new buildings to the Brick as well as retrieving of point names.

TODO: Use the brick schema to perform analysis. We have only created this schema, not used it in many useful ways.