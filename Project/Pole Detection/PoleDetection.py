import pcl
import numpy as np
import math
from geo2cart import geo2cart

def filterOutliers(pointCloud, mean, stdDev):
    outFilter = pointCloud.make_voxel_grid_filter()

    outFilter.set_leaf_size(1, 1, 1)

    outFilter = outFilter.filter()

    outFilter = pointCloud.make_statistical_outlier_filter()

    outFilter.set_mean_k(mean)

    outFilter.set_std_dev_mul_thresh(stdDev)

    outFilter.set_negative(False)

    negativeOutliers = outFilter.filter()
    file = open('Filter', 'w')
    for point in negativeOutliers:
        file.write(str(point[0]) + " " + str(point[1]) + " " + str(point[2]) + '\n')
    file.close()

    return negativeOutliers

def removeObjects(negativeOutliers, index, thresh):
    remainingElements = negativeOutliers.make_kdtree_flann()
    kIndices, kSqrDistances = remainingElements.nearest_k_search_for_cloud(negativeOutliers, index)
    dist = np.sum(kSqrDistances, axis=1)
    val = 1500000
    blocks = []
    for i in range(np.shape(dist)[0]):
        blocks.extend(kIndices[i]) if dist[i] < float(thresh) else val
    indices = list(set(blocks))
    negativeOutliers = negativeOutliers.extract(indices, negative = True)
    refined = open('Refined', 'w')
    for point in negativeOutliers:
        refined.write(str(point[0]) + " " + str(point[1]) + " " + str(point[2]) + '\n')
    refined.close()
    return negativeOutliers

def segmentation(negativeOutliers, model, iter):
    segSet = negativeOutliers.make_segmenter_normals(ksearch = 50)
    segSet.set_optimize_coefficients(True)
    segSet.set_normal_distance_weight(0.1)
    segSet.set_method_type(pcl.SAC_RANSAC)
    segSet.set_max_iterations(iter)

    if model == pcl.SACMODEL_CYLINDER:
        segSet.set_model_type(model)
        segSet.set_distance_threshold(20)
        segSet.set_radius_limits(0, 10)
        segIndices, model = segSet.segment()
        cylindricalSeg = negativeOutliers.extract(segIndices, negative = False)
        print("Generated Cylindrical segments")
        final = open('Cylinder', 'w')
        for point in cylindricalSeg:
            line = final.write(str(point[0]) + " " + str(point[1]) + " " + str(point[2]) + '\n')
        final.close()
        return cylindricalSeg

    else:
        segSet.set_model_type(model)
        segSet.set_distance_threshold(85)
        segIndices, model = segSet.segment()
        cloud = negativeOutliers.extract(segIndices, negative = True)
        filter = cloud.make_passthrough_filter()
        filter.set_filter_field_name("x")
        filter.set_filter_limits(0, max(lat))
        cloud = filter.filter()
        return cloud

file = open('final_project_point_cloud.fuse', 'r')

print("Detection started")
lat = []
long = []
alt = []
intensity = []

joinedPoints = []

index = 1000
thresh = 5000
for line in file:
    temp = []
    k = line.split()
    lat.append(float(k[0]))
    long.append(float(k[1]))
    alt.append(float(k[2]))
    intensity.append(float(k[3]))

    coord = geo2cart.cartesian(float(k[0]), float(k[1]), float(k[2]))
    joinedPoints.append([coord[0], coord[1], coord[2]])


joinedPoints = np.array(joinedPoints, dtype = np.float32)
pntCloud = pcl.PointCloud()
pntCloud.from_array(joinedPoints)

negativeOutliers = filterOutliers(pntCloud, mean = 50, stdDev = 5)
negativeOutliers = removeObjects(negativeOutliers, index, thresh)

cylindricalSeg = segmentation(negativeOutliers, model = pcl.SACMODEL_CYLINDER, iter = 1000)
cloud = segmentation(cylindricalSeg, model = pcl.SACMODEL_CYLINDER, iter = 100)
final = open('Detected_Poles.txt', 'w')
for point in cloud:
    final.write(str(point[0]) + " " + str(point[1]) + " "+ str(point[2]) + '\n')

Print("Detection Completed")

