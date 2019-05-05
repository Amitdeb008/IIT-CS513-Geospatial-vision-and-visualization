from math import sin, cos, log, pi
import cv2
import numpy as np
import urllib.request
import requests
import shutil

xrange=range

LATITUDE_RANGE = (-89.90876543, 89.90876543)
LONGITUDE_RANGE = (-180., 180.)
EARTH_RADIUS = 6378137

def cut(n, minMax):
    return min(max(n, minMax[0]), minMax[1])

def mSize(level):
    return 256 << level

def GrdRes(lat, level):
    lat = cut(lat, LATITUDE_RANGE)
    return cos(lat * pi / 180) * 2 * pi * EARTH_RADIUS / mSize(level)

def mScale(lat, level, dpi):
    return GrdRes(lat, level) * dpi / 0.0254

def GeoToPixel(geo, level):                     #Latitude and Longitude points are converted to pixel
    lat, lon = float(geo[0]), float(geo[1])
    lat = cut(lat, LATITUDE_RANGE)
    lon = cut(lon, LONGITUDE_RANGE)
    x = (lon + 180) / 360
    sin_lat = sin(lat * pi / 180)
    y = 0.5 - log((1 + sin_lat) / (1 - sin_lat)) / (4 * pi)
    mapSize = mSize(level)
    pixel_x = int(cut(x * mapSize + 0.5, (0, mapSize - 1)))
    pixel_y = int(cut(y * mapSize + 0.5, (0, mapSize - 1)))
    return pixel_x, pixel_y

def PixelToTile(pixel):            #Generating Tiles using Pixels
    return pixel[0] / 256, pixel[1] / 256

def TitleToQuadkey(tile, level):
    tile_1 = tile[0]
    tile_2 = tile[1]
    quadkey = ""
    for i in xrange(level):
        bit = level - i
        digit = ord('0')
        mask = 1 << (bit - 1)  # if (bit - 1) > 0 else 1 >> (bit - 1)
        if (tile_1 & mask) is not 0:
            digit += 1
        if (tile_2 & mask) is not 0:
            digit += 2
        quadkey += chr(digit)
    return quadkey

def fromGeo(geo, level):
    pixel = GeoToPixel(geo, level)
    tile = PixelToTile(pixel)
    return tile

def getImages(keys):
    ext = ".jpeg"
    urlA = 'http://h0.ortho.tiles.virtualearth.net/tiles/h'
    urlB = '.jpeg?g=131'
   
    
    for i in range(0,len(keys)):
        fname = str(i+1)+ext
        url = urlA + keys[i] + urlB
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(fname, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

def combineImage():
    img1 = cv2.imread('1.jpeg')
    img2 = cv2.imread('2.jpeg')
    img3 = cv2.imread('3.jpeg')
    img4 = cv2.imread('4.jpeg')
 
    img5 = cv2.imread('5.jpeg')
    img6 = cv2.imread('6.jpeg')
    img7 = cv2.imread('7.jpeg')
    img8 = cv2.imread('8.jpeg')
    
    img9 = cv2.imread('9.jpeg')
    img10 = cv2.imread('10.jpeg')
    img11 = cv2.imread('11.jpeg')
    img12 = cv2.imread('12.jpeg')
    
    
    i = [[img1,img2,img3,img4],[img5,img6,img7,img8],[img9,img10,img11,img12]]
    
    final = np.hstack((np.vstack(i[0]),np.vstack(i[1]),np.vstack(i[2])))
    
    cv2.imwrite('combined.jpeg',final)

def main():
   #The below Latitude & Longitude points are for displaying aerial image of IIT Chicago
    lat1 = 41.834734
    lon1 = -87.623386
    lat2 = 41.839363
    lon2 = -87.629659
    print("Tiles are being generated for the given 2 points...")
    x = fromGeo((lat1,lon1), 17)
    y = fromGeo((lat2,lon2), 17)
    print("Tiles are being generated for the given 2 points...")
    zipped = []
    if (x[0]>y[0]):
        t = y
        y = x
        x = t
    for i in range(int(x[0]),int(y[0]+1)):
        for j in range(int(x[1]),int(y[1]+1)):
            zipped.append((i,j))
    print("Number of tiles generated: %d" %len(zipped))
    print("Quadkeys are being generated for the generated tiles....")
    keys = []
    for i in range(0,len(zipped)):
        print(zipped[i])
        keys.append(TitleToQuadkey(zipped[i], 17))
    print("Finished generating Quadkeys ")
    print("Downloading images for generated the quadkeys....")
    getImages(keys)
    print("Combining images....")
    combineImage()
    print("Final image generated.")

if __name__ == '__main__':
    main()
