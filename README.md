# European Center for Medium-range Weather Forecast (ECMWF) Graphical Data Visualisation
This is a week-long, personal project for learning how to use python with blender. 

The tool allows to visualise publicly available data from the ECMWF as little coloured squares on the surface of the earth, where the colour indicates the extent of the recorded value. E.g. if the value is the temperature at 2 meters off the ground, a red square will indicate a hotter reading than a green square.

A possible end result, displaying temperature at two meters off the ground in areas around the Uk and Italy is shown below:
![RENDER_AreasOfUkIt_sample](https://user-images.githubusercontent.com/79207038/177328890-3472513f-a284-4396-a0a4-74023e823b37.png)

## Grib to Json conversion
To get started with the tool, you will need a .json file for Blender to read off. The .json file needs to be an array of dictionaries, where each dictionary is one recording.

A suitable .json will look like this:
<img width="1920" alt="Screenshot 2022-07-05 at 13 36 04" src="https://user-images.githubusercontent.com/79207038/177328972-2433ee45-9318-426b-a8f1-88742d3256e1.png">

To get a suitable .json file, the easiest way is by converting a .grib file from the ECMRWF to .json using the GribToJson python converter inculded. As just stated, the converter will need a .grib file, which can be sourced in two prominent ways:
* Dowloading a .grib file from the ECMRWF as explained (by them) here: https://github.com/ecmwf-projects/polytope-client;
* Using the sample.grib file included in this repository.

The tool should guide you in converting the .grib file into a .json file, which will be stored in the same file as the GribToJson python converter.

NB: Because both the converter and blender later expect files to be in the same directory as them, please keep all of the files inculded and produced by this tool in the same folder.

## Using Json to Display the Data
Once a suitable .json file is sourced, you can now open blender to display the data from the json file.

NB: For each point plotted, a new object and a new material are formed. Thus, please be mindful that the process may take a while, especially if the nuumber of points is in the thousands.

When blender is opened, there is a chance of the earth not recocnising the texture and looking something like this:
<img width="1024" alt="Screenshot 2022-07-05 at 14 00 16" src="https://user-images.githubusercontent.com/79207038/177334346-6733b56b-7462-4f4c-8a88-dfa12037c13c.png">

If that is the case, the fix is to re-assign the texture. This can be done by: 
> Going to the Shading Tab;
> Selecting the earth through the Scene Collection;
> Clicking the folder icon in the Image Texture node;
> Going to the BlendersTextures folder in the ECMWF Blender Grib Visualisation folder;
> Selecting either image. Both images are the same, one was just colour adjusted.

<img width="1920" alt="Screenshot 2022-07-05 at 14 11 00" src="https://user-images.githubusercontent.com/79207038/177340059-4802cff0-3ff0-4a65-a0c2-8d39df07baf2.png">

Once the center sphere is looking like the earth, you can plot the points over it. Firstly, you need to change to the Scripting tab and select the Hub.py script from the dropdown:
<img width="1761" alt="Screenshot 2022-07-05 at 14 03 05" src="https://user-images.githubusercontent.com/79207038/177334370-a064ae91-46c1-4444-9e48-da70ce264d52.png">

The Hub code is like the "headquarters of the blender operation": from here, you can call any function from the other scripts and the Hub script itself. 

For now, all you need to do is to plot the points, which requires only the LaunchAll() function, which the Hub script calls by default. Thus, you do not need to change anything. If you now run the script using the arrow button, it will plot the points that represent the temperature around the uk, as stated in the sample .json file included.

To run the script, just press the arrow button:
<img width="1762" alt="Screenshot 2022-07-05 at 14 31 22" src="https://user-images.githubusercontent.com/79207038/177340099-30f63757-e83d-48bd-bd89-e1e3420fe809.png">

To use your own custom .json files displaying the specific data you need, you have to specify the name of the .json file by hardcoding it in the fileName variable:
<img width="1747" alt="Screenshot 2022-07-05 at 14 01 09" src="https://user-images.githubusercontent.com/79207038/177334365-8c9c58ea-fa51-4bce-9edf-581dc884ec34.png">

NB: As stated earlier, blender will assume that the .json file is stored in the same folder as the blender, and will yield an error otherwise.

Once the program is run, blender will execute it, and no visual changes occours until every step is executed. The render will therfore be located in the Render folder within the ECMWF Blender Grib Visualisation folder.

If you want to run it again, as long as you use the LaunchAll() function, all generated materials and objects will be deleted. Thus, there is no need for manual clean-up.
