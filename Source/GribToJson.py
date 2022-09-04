############### ##### LIBRARIES ##### ###############
 
# Data manipulation libraries 
import numpy as np
import pandas as pd
import xarray as xr

# To check if file exists
import os

# Data storage libraries
import json

# To measure time and performance
import time

############### ##### MENU ##### ###############

def UploadFileMode():

    global fileNameToBe
    
    print("(Only accepts files stored within the same folder as this python script)")
    fileNameToBe = input("Enter file name: ")

    if(os.path.exists(fileNameToBe) == False):
        print("Not such file found...")
        print("(Please try again) \n")
        IntroMenu()
        
    allowedRegions.append(Whole)

def SampleFileMode():
    print("This instance will convert the file: " + fileToConvert)
    print(" ")

    possibleRegions = ["Uk", "De", "It", "Equator", "EuropeLikeSlice"]
    possibleRegionsAsClassInstances = [UK, DE, IT, Equator, EuropeLikeSlice]
    print("Input the regions you want to visualise")
    print("E.g. Input 0,2 to visualise the UK and Italy only")

    global fileNameToBe

    for i in range(len(possibleRegions)):
        region = possibleRegions[i]
        
        print(" ", i, " - " + region)
    print(" ")
    
    choice = input("Chosen Regions: ")
    print(" ")

    choices = choice.split(",")
    
    for s in range(len(choices)):

        try:
            
            choice = choices[s]
            
            allowedRegions.append(possibleRegionsAsClassInstances[int(choice)])
            
            fileNameToBe = fileNameToBe +  possibleRegions[int(choice)]
            
        except:
            print("Index ", choices[s], " does not transate to any region!")

    print("The Json will include points from ", len(allowedRegions), " regions.")

def IntroMenu():

    print("Welcome to the .grib to json converter.")
    print("This allows you to convert the publicly available .grib files from the ECMRWF to .json files,")
    print("which is a necessary step to visualise the data from Blender")
    print(" ")

    print("Would you like to: ")
    print("1 - Use the sample .grib file")
    print("2 - Upload .grib file from disk")
    print("3 - quit")
    print(" ")
    choice = input("Choosen mode: ")

    if(choice == "1"):
        SampleFileMode()
        
    elif(choice == "2"):
        UploadFileMode()
        
    elif(choice == "3"):
        quit()
        
    else:
        print("Not such mode found...")
        print("(Please try again) \n")
        IntroMenu()
        

############### ##### GRIB -> XARRAY -> JSON CONVERSION SUBROUTINES ##### ###############

def gribToXarray(fileToConvert):
    # Converts .grib to an xarray
    ds = xr.open_dataset(fileToConvert + ".grib", engine = "cfgrib")

    return ds

# The function that adds point to the array toConvert
#  which will eventually be transformed into jsonFormat
def addPoint(value, lat, lon):
        tempDictionary = {
                "Value" : float(value),
                "Lat" : float(lat),
                "Lon" : float(lon)
        }
        # This is the array of dictionaries that will eventually become the JSON file
        toConvert.append(tempDictionary)

# Converts the toConvert array into a json file
# And stores it in the memory
def convertToJson(toConvert):

    # Time
    conversion = time.time()
    
    # Logging
    print("Converting...")

    # Opens JSON file
    with open(fileNameToBe + "_" + fileToConvert + ".json", 'w', encoding = 'utf-8') as outfile:
        json.dump(toConvert, outfile, ensure_ascii = False, indent = 4)

        
    # Time
    end = time.time()

    # Final Logging
    print("Converted")
    print("The conversion took ", round(end - conversion, 1), " seconds.")
    print(" ")
    print("The whole process took ", round(end - start, 1), " seconds.")
    print("The bounds inculde only ", numberInBounds, " points.")# Logging

############### ##### REGION CROPPING ##### ###############

# Boudary limits - to cut down the number of points
# Class which stores all boundary groups for a region
class Boundary:
    
    minLat = 0
    maxLat = 0
    minLon = 0
    maxLon = 0
    
    def __init__(self, minLat, maxLat, minLon, maxLon ):
        
        self.minLat = minLat
        self.maxLat = maxLat
        self.minLon = minLon
        self.maxLon = maxLon
        
# Each region is addedd by creating a new boundary object
UK = Boundary(50, 59, -10, 2)
DE = Boundary(47, 54, 5, 14)
IT = Boundary(35, 47, 6, 18)
EuropeLikeSlice = Boundary(-90, 90, -12, 25)
Equator = Boundary(-10, 10, -180, 180)
Whole = Boundary(-90, 90, -180, 180)

allowedRegions = []

def boundaryCheck(latExamined, lonExamined):

     for region in allowedRegions :
            if ( latExamined >= region.minLat and latExamined <= region.maxLat ):
                if ( lonExamined >= region.minLon and lonExamined <= region.maxLon ):
                    return True
                
############### ##### MISCELANOUS SETUP ##### ###############

# Default input file to convert
fileToConvert = "sample"
fileNameToBe = "AreasOf"

IntroMenu()
print(" ")

# Logging
print("Start!")
print(" ")
start = time.time()

# Making new empty array to append to
toConvert= []

# Feeds it into the conversion function
data = gribToXarray(fileToConvert)

# Gets the 1st time, which will be the only one to be considered.
timeChoosen = data.time[0]
# Preps the array to only consider tempertature
arrayChosen = data.sel(time=timeChoosen).t2m

# Counting to report later
numberInBounds = 0

# Prepping to count and loop through the data
lonPos = 0
latPos = 0

# Time
setUp = time.time()
# Logging
print("Set-up done in ", round(setUp - start, 1), " seconds. Ready to loop!")

############### ##### LOOP THROUGH POINTS ##### ###############

# Logging
print("Looping...")
print(" ")

# The big loop through longitude (480 times)
for longitude in arrayChosen.longitude:
    
    # The small loop through latitude (241 times, for a total of 115,680)
    for latitude in arrayChosen.latitude:

        # Simplifies the values expression for the current point
        latExamined = arrayChosen.latitude.values[latPos]
        lonExamined = arrayChosen.longitude.values[lonPos]

        # Adapts the current point
        # To be in the -180 180 format for longitude
        if(lonExamined > 180):
            lonExamined = lonExamined - 360

        # Checks if within the boundary of any interesting region
        if(boundaryCheck(latExamined, lonExamined)):

            # Stores point and its interesting values in the dictionaries array
            addPoint(arrayChosen.values[latPos][lonPos], latExamined, lonExamined)

            # Used for logging the number of points to plot later
            numberInBounds += 1

        # Counting
        latPos += 1
    # Counting
    lonPos += 1
    
    # Resetting the count of the small loop
    latPos = 0
# Resetting the count of the big loop
lonPos = 0

# Time
looping = time.time()

# Logging
print("Loop done in ", round (looping - setUp, 1), " seconds. Ready to convert!")
print(" ")

convertToJson(toConvert)
