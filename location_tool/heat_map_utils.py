import numpy as np
from datetime import datetime
import time
from functools import reduce
import googlemaps

import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

####### Calculates distance between two coordinates ##########
def CalculateDistance(coord1, coord2): # coord = {'lat' : latval, 'lng': longval}   
    Radius_miles = 3961
    
    lat1 = coord1['lat']
    lon1 = coord1['lng']
    
    lat2 = coord2['lat']
    lon2 = coord2['lng']
    
    lat1 = np.radians(lat1) 
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2*np.arctan2(a**(.5), (1-a)**(.5))
    dm = c*Radius_miles
    
    return dm*1609.34  #Returns distance in meters 

########### Turn a matrix of scores into javascript code #############

def javascriptwriter(scores, xvals, yvals, num_xsamples, num_ysamples, All_tags):
    output = ""
    for tag_group in All_tags:
        Best = np.amax(scores[tag_group])
        output += " var %s ={max: %f, data: [" % (tag_group, Best)
        for i in range(num_xsamples):
            for j in range(num_ysamples):
                output += "{lat: %.10f, lng: %.10f, count: %.10f}," %(yvals[j], xvals[i], scores[tag_group][i][j]) 

        output = output[:-1]
        output += "]}; "
        output += "\n"

    return (output)

######## Set up coordinate grid ###########################
def prepare_query(bounding_box):
    sampling_rate = 500      # Sample every 500 meters in both x and y directions
    coordinates = bounding_box.coordinates
    northeast_coord = coordinates['northEast']
    southwest_coord = coordinates['southWest']
    northwest_coord = {'lat': northeast_coord['lat'], 'lng': southwest_coord['lng']}
    southeast_coord = {'lat': southwest_coord['lat'], 'lng': northeast_coord['lng']}

    if northeast_coord['lat'] >= 0 and southeast_coord['lat'] >= 0:
        lat_diff = northeast_coord['lat'] - southeast_coord['lat']
    elif northeast_coord['lat'] < 0 and southeast_coord['lat'] < 0:
        lat_diff = southeast_coord['lat'] - northeast_coord['lat']
    else:
        lat_diff = abs(northeast_coord['lat']) + abs(southeast_coord['lat'])
    
    if northeast_coord['lng'] >= 0 and northwest_coord['lng'] >= 0:
        lng_diff = northeast_coord['lng'] - northwest_coord['lng']
    elif northeast_coord['lng'] < 0 and northwest_coord['lng'] < 0:
        lng_diff = northwest_coord['lng'] - northeast_coord['lng']
    else:
        lng_diff = abs(northeast_coord['lng']) + abs(southeast_coord['lng'])

    center_coord = {
        'lat': southeast_coord['lat'] + (lat_diff / 2),
        'lng': southwest_coord['lng'] + (lng_diff / 2)
    }
    xdist = CalculateDistance(southwest_coord, southeast_coord)
    ydist = CalculateDistance(northeast_coord, southeast_coord)
    num_xsamples = int(np.round(xdist/sampling_rate))
    num_ysamples = int(np.round(ydist/sampling_rate))
    xvals = np.linspace(southwest_coord['lng'], southeast_coord['lng'], num_xsamples)
    yvals = np.linspace(southeast_coord['lat'], northeast_coord['lat'], num_ysamples)

    return {
        'northeast_coord': northeast_coord,
        'southwest_coord': southwest_coord,
        'southeast_coord': southeast_coord,
        'center_coord': center_coord,
        'xdist': xdist,
        'ydist': ydist,
        'num_xsamples': num_xsamples,
        'num_ysamples': num_ysamples,
        'xvals': xvals,
        'yvals': yvals
    }

############ Get Data from Google ###########

def getGoogleData(xvals, yvals, num_xsamples, num_ysamples):
    gmaps = googlemaps.Client(key = os.environ.get('GOOGLE_API_KEY') )    
    community_tags = ['library', 'church', 'school', 'laundry', 'post_office', 'gas_station']
    tourist_tags = ['amusement_park', 'aquarium', 'art_gallery', 'bowling_alley', 'museum', 'night_club', 'park', 'university', 'stadium', 'zoo']      
    food_tags = ['restaurant']       
    big_shops_tags = ['department_store', 'shopping_mall', 'clothing_store', 'shoe_store']
    small_shops_tags = ['florist', 'hair_care', 'bakery', 'book_store', 'liquor_store' , 'beauty_salon']
    transit_tags = ['transit_station']
    All_tags = {'googletransitData': transit_tags, 'googlecommunityData': community_tags, 'googletouristData': tourist_tags, 'googlefoodData': food_tags, 'googlebigshopsData': big_shops_tags, \
       'googlesmallshopsData': small_shops_tags, 'googletransitData': transit_tags}
    scores = {}

    
    # Create a score array for all tag groups
    
    for tag_group in All_tags:
           scores[tag_group] = np.array([[0.0 for k in range(num_ysamples)] for k in range(num_xsamples)])
    

    for tag_group in All_tags:
        tag_list = All_tags[tag_group]

        for i in range(num_xsamples):
            for j in range(num_ysamples):
                coord = {'lat': yvals[j], 'lng': xvals[i]}

                for tag in tag_list:
                    curr_result = gmaps.places_nearby(location = coord, radius = 500, type = tag)
                    places = curr_result['results']
                    scores[tag_group][i][j] += len(places)


                    if 'next_page_token' in curr_result:
                        token = curr_result['next_page_token']
                        time.sleep(5)
                        curr_result = gmaps.places_nearby(location = coord, page_token = token)
                        places = curr_result['results']
                        scores[tag_group][i][j] += len(places)

                        if 'next_page_token' in curr_result:
                            token = curr_result['next_page_token']
                            time.sleep(5)
                            curr_result = gmaps.places_nearby(location = coord, page_token = token)
                            places = curr_result['results']
                            scores[tag_group][i][j] += len(places)

    for tag_group in All_tags:
        if (np.amax(scores[tag_group]) > 0):
            scores[tag_group]= scores[tag_group]*10/np.amax(scores[tag_group])

    return((scores, All_tags))
