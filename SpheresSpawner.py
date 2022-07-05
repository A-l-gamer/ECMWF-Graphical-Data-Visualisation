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

# Sets-up the core variables
# (Actually not necessary in python3, just neat)
locationX = 0
locationY = 0
locationZ = 0

latAngles = []
lonAngles = []

# The size of the spawned shapes
# Just for aesthetic purposes
size = 0.005

colourMultiplier = 1
colourMidpoint = 0

############### ############### COLOUR MANAGMENT ############### ###############

def newShader(object, tem):
    
    materialName = "mtValue" + str(tem)
    
    alreadyExistingMaterial = False
    
    # Loops through materials
    for mat in bpy.data.materials:
        # Checks if already there
        if materialName == mat.name:   
            object.active_material = mat
            alreadyExistingMaterial = True
            break
    
    # If material does not exist yet
    if(alreadyExistingMaterial != True):
        
        # Sets colour in the three components
        if(tem >= colourMidpoint):
            r = math.sin(math.radians(tem)  * colourMultiplier)
            g = math.cos(math.radians(tem) * colourMultiplier)
            b = 0       
        else:
            r = 0
            g = math.sin(math.radians(tem) * colourMultiplier)
            b = math.cos(math.radians(tem) * colourMultiplier)
            
        # Creates a new material which has the object's name
        mat = bpy.data.materials.new(materialName)

        # Sets up to use nodes
        mat.use_nodes = True

        # Clears any existing nodes and links
        if mat.node_tree:
            mat.node_tree.links.clear()
            mat.node_tree.nodes.clear()
      
        # Used to call the nodes and links of material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Adds output node
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        # Adds diffuse node
        shader = nodes.new(type='ShaderNodeBsdfDiffuse')
        # Sets values of diffuse node equal to the parameters passed
        nodes["Diffuse BSDF"].inputs[0].default_value = (r, g, b, 1)
        
        #Links diffuse and output
        links.new(shader.outputs[0], output.inputs[0])
        
        object.active_material = mat

############### ############### CORE ALGORITHM ############### ###############

def ShapesSummoner(information):
    # Loops through every dictionary
    # to append the values to the arrays

    for dict in information:

        lat = dict.get("Lat")
        lon = dict.get("Lon")
        
        # Gets temperature in Kelvin from file
        tem = dict.get("Value")
        # Converts to Celsius
        tem = tem -273.15
        
        # Calculates how far up the point is
        # Based on its latitude
        locationZ = math.sin(math.radians(lat))

        # Calculates the extent that the latitude will have on the other coordinates
        # to ensure the final shape is a sphere, and not a cylinder
        offset = 1 - math.cos(math.radians(lat))
        
        # Calculates the horizontal (X and Y) coordinates of the point
        locationY = math.cos(math.radians(lon)) * math.cos(math.radians(lat))
        locationX = math.sin(math.radians(lon)) * math.cos(math.radians(lat))
        
        locationX *= -1
        
        # Spawns the sphere at the correct location
        bpy.ops.mesh.primitive_plane_add(size = size, calc_uvs = False)
        newCircle = bpy.context.object
        
        #newCircle.scale.x = squareSize
        #newCircle.scale.y = size
            
        newCircle.location.x = locationX
        newCircle.location.y = locationY
        newCircle.location.z = locationZ
        
        rotationX = lat + 90
        rotationZ = lon
        
        newCircle.rotation_euler.x = math.radians(rotationX)
        newCircle.rotation_euler.z = math.radians(rotationZ)
        
        newShader(newCircle, tem)
        
############### ############### GENERAL SET-UP ############### ###############

def TemperatureRange(information):

    minTem = 90
    maxTem = -90

    temRange = 1
    
    global colourMultiplier
    global colourMidpoint

    for dict in information:
    
        # Gets temperature in Kelvin from file
        tem = dict.get("Value")
        
        # Converts to Celsius
        tem = tem -273.15
      
        if(minTem > tem):
            minTem = tem
        elif(maxTem < tem):
            maxTem = tem
            
    temRange = abs(minTem) + abs(maxTem)
    colourMidpoint = minTem + (temRange/2)

    colourMultiplier = 180 / temRange

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
    
    TemperatureRange(information)
    ShapesSummoner(information)
    
def Start():
     
    SetUp()