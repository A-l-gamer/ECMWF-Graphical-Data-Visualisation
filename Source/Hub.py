# The Hub:
# This is the core of the blender program
# Where all the shared variables are stored
# And from where the UI will eventually launch the different programs

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

blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

# The other scripts to launch
import SpheresSpawner
import CameraPositioner
import Renderer

############### ############### SHARED VARIABLES ############### ###############

fileName = "AreasOfUkIt_sample.json"

def getFileName():
    return fileName

############### ############### CLEARING ############### ###############

def ClearMaterials():
    print("Materials Deleted")
    
    for m in bpy.data.materials:
        if(m.name != "PlaceHolder Earh Base Material"):
            bpy.data.materials.remove(m)
            
def ClearScene(): 
    print("Scene Cleared")
    
    for ob in bpy.data.objects:
        if(ob.name != "Earth" and ob.name != "Camera" and ob.name != "Camera Rotator" and ob.name != "Light"):
            bpy.data.objects[ob.name].select_set(True)
            bpy.ops.object.delete()
            
def ResetCamera():
    print("Camera Reset")
    
    camera = bpy.data.objects['Camera Rotator']

    camera.rotation_euler.x = 0
    camera.rotation_euler.z = 0
    
def ResetAll():
    
    ClearMaterials()
    ClearScene()
    ResetCamera()

############### ############### FUNCTIONS FROM "MODULES" ############### ###############

def SummonShapes():

    SpheresSpawner.Start()

def PositionCamera():

    CameraPositioner.Start()

def Render():

    Renderer.Start()

############### ############### GENERAL SET-UP ############### ###############

def LibSetUp():
    
    blend_dir = os.path.dirname(bpy.data.filepath)
    if blend_dir not in sys.path:
       sys.path.append(blend_dir)
       
    importlib.reload(SpheresSpawner)
    importlib.reload(CameraPositioner)
    importlib.reload(Renderer)

def SetUp():

    LibSetUp()

    ResetAll()
    
############### ############### CORE ALGORITHM ############### ###############

def LaunchAll():

    SetUp()

    SummonShapes()
    PositionCamera()
    Render()

LaunchAll()