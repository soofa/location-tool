
Before you can use the python script, you will need to import the following python modules:

- yelp (https://github.com/Yelp/yelp-python)
- googlemaps (https://github.com/googlemaps/google-maps-services-python)

If you have python3 on your computer, you can install them using pip.

## Api Keys:

Google Maps Webservice API: ' Your API Key '
Google Maps Javascript API: ' Your API Key '


Yelp ConsumerKey =  ' Your API Key '
Yelp ConsumerSecret = ' Your API Key '
Yelp Token = ' Your API Key '
Yelp TokenSecret = ' Your API Key '

Walk Score API: ' Your API Key '

## How to Create Heatmaps:

From your terminal, go to the directory that CreateHeatMaps.py is located and enter:

python3 CreateHeatMaps.py

Then, the following prompt will open: 

Enter location in city, state format (NewHaven, CT): 

Enter the city that you wish to create heatmaps for. Note that depending on the size of the city, this may take 
anywhere from 15 minutes to multiple hours. Also, due to restrictions on the above apis, it is only possible to create heatmaps for 2-3 
cities every day.


## How to Visualize Heatmaps:

After CreateHeatMaps.py finishes, a file called 'SoofaDataYOURCITY.js' will be created in the current folder. Now open
HeatMap.html and go to line 56. There, you will need to add the following code to see the heatmaps for your city:

```` HTML
 <option value="Cityname">Cityname, State</option>
 ````

 Then, open HeatMap.html with Google Chrome. You will see a menu called 'Cities.' Click on this menu and then click on your city. This will update the map view and you will be able to see the heatmaps for your city. 

## How to use HeatMap.html:

You can select from a list of preloaded cities using the 'Cities' dropdown menu. The default city is Cambridge, MA. You can select which layers you want to see on the upper right corner of the map view. You should only be clicking on one layer! If you want to visualize multiple layers together, go to the upper right corner of the map view and click 'Multiple Layers.' You can then go to the 'Add to Multiple Layers' drop down menu and select the layers that you wish to visualize. 

You can also click on the map itself. This will create a draggable marker that you can move around. Dragging this marker will display the various scores for the marker location on the right side of the webpage.

## How Scores are Calculated:

Each score ranges from 0 to 10. The google scores count the number of locations of that type that are in a 500 meter radius of the marker. The yelp scores use the formula ratings^2 * # of ratings to give a score for each location. The walkscores are pulled from the walkscore API. 

## Other Information:

The heatmaps are created using the Heatmap.js library. The map view is created using the leaflet.js library.
