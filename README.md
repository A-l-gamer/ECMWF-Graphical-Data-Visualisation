# ECMWF-Graphical-Data-Visualisation

## Grib to Json conversion
To get started with the tool, you will need a .json file for Blender to read off. The .json file needs to be an array of dictionaries, where each dictionary is one recording.

A suitable .json will look like this:
<img width="1920" alt="Screenshot 2022-07-05 at 13 36 04" src="https://user-images.githubusercontent.com/79207038/177328972-2433ee45-9318-426b-a8f1-88742d3256e1.png">

To get a suitable .json file, the easiest way is by converting a .grib file from the ECMRWF to .json using the GribToJson python converter inculded. As just stated, the converter will need a .grib file, which can be sourced in two prominent ways:
* Dowloading a .grib file from the ECMRWF as explained (by them) here: https://github.com/ecmwf-projects/polytope-client;
* Using the sample.grib file included in this repository.

The tool should guide you in converting the .grib file into a .json file, which will be stored in the same file as the GribToJson python converter.

NB: Because both the converter and blender later expect files to be in the same directory as them, please keep all of the files inculded and produced by this tool in the same folder.
