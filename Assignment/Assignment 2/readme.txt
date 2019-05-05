How to Run:

Imstasll Python.

Save Partition6467ProbePoints.csv, Partition6467LinkData.csv, Assignment_2.py files in the same folder.

Run Assignment_2.py 

It will generate the following files
1. EvaluationData
2. SlopeData
3. MatchedPoints

MatchedPoints Record Format:

	sampleID, dateTime, sourceCode, latitude, longitude, altitude, speed, heading, linkPVID, direction, distFromRef, distFromLink

		sampleID	is a unique identifier for the set of probe points that were collected from a particular phone.
		dateTime	is the date and time that the probe point was collected.
		sourceCode	is a unique identifier for the data supplier (13 = Nokia).
		latitude	is the latitude in decimal degrees.
		longitude	is the longitude in decimal degrees.
		altitude	is the altitude in meters.
		speed		is the speed in KPH.
		heading		is the heading in degrees.
		linkPVID	is the published versioned identifier for the link.
		direction	is the direction the vehicle was travelling on thelink (F = from ref node, T = towards ref node).
		distFromRef	is the distance from the reference node to the map-matched probe point location on the link in decimal meters.
		distFromLink	is the perpendicular distance from the map-matched probe point location on the link to the probe point in decimal meters.


 