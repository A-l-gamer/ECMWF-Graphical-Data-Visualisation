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
   
############### ############### RENDERING ############### ###############   

def Render(outputName = "RENDER_"):
    
    RenderPath = os.path.dirname(bpy.data.filepath) + "/Render"
    
    fileName = Hub.getFileName().split(".")[0]
    outputName = outputName + fileName
    outputName + ".jpeg"
    
    bpy.context.scene.render.filepath = os.path.join(RenderPath, outputName)
    
    bpy.ops.render.render(write_still = True)
    
############### ############### GENERAL SET-UP ############### ###############

def LibSetUp():
    blend_dir = os.path.dirname(bpy.data.filepath)
    if blend_dir not in sys.path:
       sys.path.append(blend_dir)
       
    importlib.reload(Hub)

def SetUp():
    
    LibSetUp()

def Start():
    
    SetUp()
    
    Render()