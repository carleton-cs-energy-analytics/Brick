# Brick
Respository for managing the Brick Schema for Carleton's Campus. 

Docs pages for Brick Schema located here: https://brickschema.org/

The brickTest.py script currently generates a brick schema in 'Carleton.ttl' which graphs all of the points in Boliou and Evans with their respective dependencies. Each point is associated with its corresponding room, each room with its respective floor, floor with building, etc. To see a visualization of this graph upload the '.ttl' file here: https://brickschema.github.io/brick-studio/. An example script which shows how someone might read from the '.ttl' file is included as 'brickExample.py.' An advantage to this approach to getting point names, is that someone does not need to look through the database and manually find all point names associated with a room. Instead, they can iterate over the dependencies here. Unfortunately, due to the messiness of the point names this requires a bit of work to figure out how to best parse the '.ttl' file. One thing of note is that '.ttl' files do not accept the character " ", so any " " characters in point names are replaced with "*". To input any point name into the database as a query, you will have to replace all "*" with " ".

TODO: Add more buildings to the schema as they are added to the database.
TODO: This isn't in this repository, but making it so that all point names in the database don't contain the character " " would help a lot with the organization here. Similarly, point name formats really vary building to building and even within buildings. Simplifications of that on the database end will very much simplify the addition of new buildings to the Brick as well as retrieving of point names.
