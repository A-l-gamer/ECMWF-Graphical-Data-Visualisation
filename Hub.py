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

#LaunchAll()

############### ############### UI ############### ###############

class CustomUIPanel(bpy.types.Panel):
    
    bl_label = "This is the UI area for the automatic commands"
    bl_idname = "AutomaticPlottingUI"
    
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    
    def draw(self, context):
        
        layout = self.layout
        
        row1 = layout.row()
        
        row2 = layout.row()
        row3 = layout.row()
        
        row4 = layout.row()
        row5 = layout.row()
        row6 = layout.row()
        
        row1.label(text = "Automatic Weather Data Plotting")
        
        row2.operator("mesh.launchalloperator")
        row3.operator("mesh.resetalloperator")
        
        obj = context.object               
        row5.prop(obj, "number_of_pages")
        
        layout.prop(context.window_manager, "number")
        
        row4.label(text = "Json file: ")
        jsonFile = bpy.props.StringProperty("Enter name of .json file to read") 
        row6.label(text = "default is: " + fileName)
        
class LaunchAllOperator(bpy.types.Operator):
    
    bl_idname = "mesh.launchalloperator"
    bl_label = "Plot"
    
    def execute(self, context):
        
        LaunchAll()
        
        return {"FINISHED"}

class ResetAllOperator(bpy.types.Operator):
    
    bl_idname = "mesh.resetalloperator"
    bl_label = "Clear"
    
    def execute(self, context):
        
        ResetAll()
        
        return {"FINISHED"}
        
bpy.utils.register_class(CustomUIPanel)
bpy.utils.register_class(LaunchAllOperator)
bpy.utils.register_class(ResetAllOperator)