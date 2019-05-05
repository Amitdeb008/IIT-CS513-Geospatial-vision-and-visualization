import math
from collections import defaultdict


#Global variables used for the code (collection defaultdict is used to handle error in list)
pointDataList = defaultdict(list)
linkDataList = defaultdict(list)

#Finding the latitude and longitude of fiven points
class findLatLong():
    def __init__(self, shapeInfo):
        self.ID = shapeInfo
        shape_attributes = shapeInfo.split("/")
        self.longitude, self.latitude = map(float, (shape_attributes[0], shape_attributes[1]))

#Packing LinkData.csv into a package object        
class PackageLinkID():
    #Pass start and end data points to class constructor which packages it into the object
    def __init__(self, ID, start, end):
        self.id = ID
        self.point1, self.point2 = findLatLong(start), findLatLong(end)
        self.longitude_vector, self.latitude_vector = self.point2.longitude - self.point1.longitude, self.point2.latitude - self.point1.latitude
        self.length = math.sqrt(self.longitude_vector ** 2 + self.latitude_vector ** 2)
        if self.latitude_vector != 0:
            self.radian = math.atan(self.longitude_vector / self.latitude_vector)
        elif self.longitude_vector > 0:
            self.radian = math.pi / 2
        else:
            self.radian = math.pi * 3 / 2
            
    #Calculating the distance between a packed linkData and a new probe-point
    def Distance(self, point):
        target_longitude, target_latitude = point.longitude - self.point1.longitude, point.latitude - self.point1.latitude
        dist_point_refnode = (target_longitude ** 2) + (target_latitude ** 2)
        projection = (target_longitude * self.longitude_vector + target_latitude * self.latitude_vector) / self.length
        if projection < 0:
            return dist_point_refnode
        if projection ** 2 > self.length ** 2:
            return (point.longitude - self.point2.longitude) ** 2 + (point.latitude - self.point2.latitude) ** 2
        return (target_longitude**2 + target_latitude**2) - projection**2

   #Calculating the distance between two links using link data.	
    def DistanceFromLink(self, point):
        target_longitude, target_latitude = point.longitude - self.point1.longitude, point.latitude - self.point1.latitude
        return math.sqrt(target_longitude**2 + target_latitude**2)

#Class used to package the sample ID data set into an object    
class PackageSampleID(object):
    def __init__(self, line):
        self.sampleID,self.dateTime,self.sourceCode,self.latitude,self.longitude,self.altitude,self.speed,self.heading = line.strip().split(',')
        self.direction = ""
        self.linkID = None
        self.distanceFromReference = None
        self.distanceFromLink = None
        self.slope = None

    # finding the direction 
    def getDirection(self, A, B):
        self.direction = "F" if ((math.cos(A) * math.cos(B) + math.sin(A) * math.sin(B)) > 0) else "T"

    #Converting object to string of required format
    def toString(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}, {}, {} ,{}, {}\n' \
            .format(self.sampleID, self.dateTime,self.sourceCode,self.latitude,self.longitude,self.altitude,self.speed,self.heading,
                    self.linkID,self.direction,self.distanceFromReference,self.distanceFromLink)

#packaging the sample ID data set into an object with scope object appended to the return list
class PackageProbeSlope(object):
	def __init__(self, line):
		self.sampleID, self.dateTime, self.sourceCode, self.latitude, self.longitude, self.altitude, self.speed, self.heading, \
        self.linkID, self.direction	, self.distanceFromReference, self.distanceFromLink = line.split(',')        
		self.elevation = None
		self.slope = None

   #converting data into comma seperated string
	def toString(self):       
		return '{}, {}, {}, {}, {}, {}, {}, {}, {}, {} , {}, {}\n' \
			.format(self.sampleID,self.dateTime,self.sourceCode,self.latitude,self.longitude,self.altitude,	self.speed,	self.heading,
					self.linkID, self.direction,self.distanceFromReference,#self.distanceFromLink,
					self.slope)

#packing the linkData
class PackageLink(object):
	def __init__(self, line):
		self.linkID,self.refNodeID,self.nrefNodeID,self.length,self.functionalClass,self.directionOfTravel,self.speedCategory,self.fromRefSpeedLimit,\
		self.toRefSpeedLimit,self.fromRefNumLanes,self.toRefNumLanes,self.multiDigitized,self.urban,self.timeZone,self.shapeInfo,self.curvatureInfo,\
		self.slopeInfo= line.strip().split(',')
		self.ReferenceNodeLat,self.ReferenceNodeLong,_  = self.shapeInfo.split('|')[0].split('/')
		self.ReferenceNode = map(float, (self.ReferenceNodeLat,self.ReferenceNodeLong))
		self.ProbePoints   = []
        
#Read the linkData from the csv and create linkDataList/pointDataList           
def readLinkData():
    print("Reading LinkData")
    for line in open("Partition6467LinkData.csv").readlines():
        columns = line.strip().split(",")
        shapeInfo = columns[14].split("|")
        for i in range(len(shapeInfo)-1):
            tempShape = PackageLinkID(columns[0], shapeInfo[i], shapeInfo[i+1])
            linkDataList[columns[0]].append(tempShape)
            pointDataList[shapeInfo[i]].append(tempShape)
            pointDataList[shapeInfo[i + 1]].append(tempShape)

#Matching the linkDataList with the probe data, find the shortest distance and create output file MatchedPoints.csv
def matchPoints():
    matchedPoints = open("MatchedPoints.csv", "w+")
    previousID = None
    matchingArray = []
    print("Writing matched points into MatchedPoints.csv.....please wait ");
    records=0;
    for line in open("Partition6467ProbePoints.csv").readlines():
        if records < 5500:
            records=records+1;
            probePoints = PackageSampleID(line)
            latitude_longitude = findLatLong(probePoints.latitude + "/" + probePoints.longitude)
            #Check if the previous value is repeated
            if probePoints.sampleID != previousID:
                previousID = probePoints.sampleID
                for key in linkDataList.keys():
                    for link in linkDataList[key]:
                        distance = link.Distance(latitude_longitude)
                        #If the probe point is empty or less than the distance find the direction b/w the point and the linkdata
                        if not probePoints.distanceFromReference or distance < probePoints.distanceFromReference:
                            probePoints.distanceFromReference, probePoints.linkID = distance, link.id
                            probePoints.distanceFromLink = linkDataList[probePoints.linkID][0].DistanceFromLink(latitude_longitude)
                            probePoints.getDirection(float(probePoints.heading), link.radian)
                            matchingArray = [link.point1, link.point2]
           
            else:
                #Looping through the array of match data when the repeation occurs
                for candidate_point in matchingArray:
                    for link in pointDataList[candidate_point.ID]:
                        distance = link.Distance(latitude_longitude)
                        if not probePoints.distanceFromReference or distance < probePoints.distanceFromReference:
                            probePoints.distanceFromReference, probePoints.linkID = distance, link.id
                            probePoints.distanceFromLink = linkDataList[probePoints.linkID][0].DistanceFromLink(latitude_longitude)
                            probePoints.getDirection(float(probePoints.heading), link.radian)
        else:
            break;     
        #Finding the distance from the reference 
        probePoints.distanceFromReference = math.sqrt(probePoints.distanceFromReference) * (math.pi / 180 * 6371000)
        #Finding the distance from the link
        probePoints.distanceFromLink = probePoints.distanceFromLink * (math.pi / 180 * 6371000)
        matchedPoints.write(probePoints.toString())

    matchedPoints.close()
    print("mapmatching is completed");

#Finding distance between two data points (latitude and longitude) with respect to earth avg rad
def distance(longitude_startpoint, latitude_startpoint, longitude_endpoint, latitude_endpoint):
    longitude_startpoint, latitude_startpoint, longitude_endpoint, latitude_endpoint = list(map(math.radians, [longitude_startpoint, latitude_startpoint, longitude_endpoint, latitude_endpoint]))
    distance_longitude, distance_latitude = longitude_endpoint - longitude_startpoint , latitude_endpoint - latitude_startpoint
    #Calculating the distance
    distance = math.sin(distance_latitude/2)**2 + math.cos(latitude_startpoint) * math.cos(latitude_endpoint) * math.sin(distance_longitude/2)**2
    #Converting in Km w.r.t earth radius
    distance = 6371 * 2 * math.asin(math.sqrt(distance))
    return distance

#Finding the slope of the road link
def calculateSlopeData():
    slopeArray = []
    records=0;
    slope_file = open("SlopeData.csv", 'w')
    previousProbe = None
    print("Computing slope of road")
    for line in open("Partition6467LinkData.csv").readlines():
        slopeArray.append(PackageLink(line)) 
    with open("MatchedPoints.csv") as each_data:
        for line in each_data:
            if records < 5000:
                records=records+1;
                current_probe = PackageProbeSlope(line)
                #checking previous value for repetation
                if not previousProbe or current_probe.linkID != previousProbe.linkID:
                    current_probe.slope = ''
                else:
                    try:
                        start, end = list(map(float, [current_probe.longitude, current_probe.latitude])), list(map(float, [previousProbe.longitude, previousProbe.latitude]))
                        hypotenuse_angle = distance(start[0], start[1], end[0], end[1]) / 1000
                        opposite_angle = float(current_probe.altitude) - float(previousProbe.altitude)
                        current_probe.slope = (2 * math.pi * math.atan(opposite_angle / hypotenuse_angle)) / 360                
                    except ZeroDivisionError:
                        current_probe.slope = 0.0
                    for link in slopeArray:
                        if current_probe.linkID.strip() == link.linkID.strip() and link.slopeInfo != '':
                           link.ProbePoints.append(current_probe)
                           break
                #Writing to the slope csv
                slope_file.write(current_probe.toString())
                previousProbe = current_probe
            else:
                break;    
        slope_file.close()
    print("Computing SlopeData is done ")    
    return slopeArray

#Evaluating the derived road slope with the surveyed road slope in the link data file
def slope_evaluation(slope_data):
    print("Evaluating slope data")
    evaluation_file = open("EvaluationData.csv", 'w')
    for node in slope_data:
        # checking for matched point in the node
        if len(node.ProbePoints) > 0:     
            sum = 0.0
            slopeArray = node.slopeInfo.strip().split('|')
            for currentSlope in slopeArray:
                sum += float(currentSlope.strip().split('/')[1])
            slope = sum / len(slopeArray)
            sum_final, probe_count = 0.0, 0
            for eachProbe in node.ProbePoints:
                if eachProbe.direction == "T":
                    eachProbe.slope = -eachProbe.slope
                if eachProbe.slope != '' and eachProbe.slope != 0:
                    sum_final += eachProbe.slope
                    probe_count += 1
            evaluatedSlope = sum_final / probe_count if probe_count != 0 else 0
            evaluation_file.write('{}, {}, {}\n'
                                  .format(node.linkID,
                                          slope,
                                          evaluatedSlope))
    print("Evaluation of slope is completed")        
    evaluation_file.close()

if __name__ == '__main__':
    #Function to create linkdata array
    readLinkData()
    #Function to create the MatchedPoints csv
    matchPoints()
    #Function to calculate the slope
    SlopeData = calculateSlopeData()
    #Function to evaluate slope data
    slope_evaluation(SlopeData)
