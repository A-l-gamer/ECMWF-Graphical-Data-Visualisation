############### ############### LIBRARIES ############### ###############

# Necessary to make other libraries work
import importlib
import sys
# Necessary to interact with the blender scene
import bpy
# Necessary for all trig calculations
import math
# Necessary to read json files off
import json
import os
# Necessary to have UI
import Hub

############### ############### OTHER ############### ###############       

class ExtremePoint:
        
    xPos = 0
    yPos = 0
    
    def __init__(self, x, y):
        
        self.xPos = x
        self.yPos = y        
        
############### ############### CORE ALGORITHM ############### ###############

def PositionCamera(horLon, verLat):

    locationZ = math.sin(math.radians(verLat))
    locationY = math.cos(math.radians(horLon)) * math.cos(math.radians(verLat))
    locationX = math.sin(math.radians(horLon)) * math.cos(math.radians(verLat)) * -1

    camera = bpy.data.objects['Camera Rotator']

    camera.rotation_euler.x = math.radians(verLat)
    camera.rotation_euler.z = math.radians(horLon)   

    
def FindMidPoint(information):
    
    minLat = 90
    maxLat = -90
    minLon = 360
    maxLon = 0

    topRight = ExtremePoint(maxLon, maxLat)
    bottomRight = ExtremePoint(maxLon, minLat)
    topLeft = ExtremePoint(minLon, maxLat)
    bottomLeft = ExtremePoint(minLon, minLat)

    # Loops through file
    # To find min/max points
    for dict in information:
        
        # Shortening the expression of current coordinates
        lat = dict.get("Lat")
        lon = dict.get("Lon")
        
        # Checks if current latitude is either extreme
        if(lat < minLat):
            minLat = lat
        elif(lat > maxLat):
            maxLat = lat
            
        # Checks if current longitude is either extreme
        if(lon < minLon):
            minLon = lon
        elif(lon > maxLon):
            maxLon = lon
            
    # Now uses the min/max points to form a rectangle
    topRight = ExtremePoint(maxLon, maxLat)
    bottomRight = ExtremePoint(maxLon, minLat)
    topLeft = ExtremePoint(minLon, maxLat)
    bottomLeft = ExtremePoint(minLon, minLat) 

    horLon = (bottomRight.xPos + bottomLeft.xPos) / 2
    verLat = (topRight.yPos + bottomLeft.yPos) / 2

    print("The midpoint is: (", horLon, ", ", verLat, ")")
    PositionCamera(horLon, verLat)


############### ############### GENERAL SET-UP ############### ###############

def LibSetUp():
    blend_dir = os.path.dirname(bpy.data.filepath)
    if blend_dir not in sys.path:
       sys.path.append(blend_dir)
       
    importlib.reload(Hub)

def SetUp():
    
    LibSetUp()
    
    jsonFile = Hub.getFileName()

    f = open(os.path.join(os.path.dirname(bpy.data.filepath), jsonFile))
    information = json.load(f)
 
    FindMidPoint(information)

def Start():
    
    SetUp()