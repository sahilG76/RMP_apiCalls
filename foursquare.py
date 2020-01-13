from contextlib import closing

import json, requests
from POI import POI
import csv


def foursquareSearch(lat, lng, errorDir):   ## could use search(lat, lng, dist) to set the searching radius as well right now, the nearest 50 (maximum) POI are returned
    CLIENT_ID = "IUVCNGA4OJNL00ZXVEGWZTSU1FUFC2PA3PY15YWY2C3M34AG"
    CLIENT_SECRET = "VZR0I3KGUHGGMEEGDII5MEVHEOOFFYXS01WAAYW1JZJDBZOT"

   
   ## This is basically the code you wrote to get the data (i.e., nearest 50 neighbors for your selected lat lng)
    url = 'https://api.foursquare.com/v2/venues/explore'
    
    # this is to convert the input parameters to the format of ll like '37.3875,-122.0575'
    ll_test=str(lat)+","+str(lng)
    
    params = dict(
      client_id=CLIENT_ID,
      client_secret=CLIENT_SECRET,
      v='20180323',
      ll=ll_test,
      limit=50,
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)


    ## Below is to get the data from the Json and save the data into a list named as venue_list
    venue_list = []

    try:

        for item in data['response']['groups'][0]["items"]:
            
            name=[]
            venueId=[]
            lat=[]
            lng=[]
            distance=[]
            category=[]

            venue = item['venue'] 
           # print venue
      
            try:
                name=venue['name']
            except NameError:
                name=None

            try:
                venueId=venue['id']
            except NameError:
                venueId=None
            
            try:
                lat=venue['location']['lat']
            except NameError:
                lat=None

            try:
                lng=venue['location']['lng']
            except NameError:
                lng=None

            try:
                distance=venue['location']['distance']
            except NameError:
                distance=None

            try:
                category=venue['categories'][0]['name']     
            except NameError:
                category=None
                                          
            
            destinationPOI=POI(str(name), str(venueId), lat, lng, distance, str(category))
            venue_list.append(destinationPOI)

    ## ignore this part for now. This is mainly to check if there is any error in the code. 
    except Exception as e:
        error="the list is not built for coordinate ({} , {}) \n".format(lat, lng )
        with open(errorDir, 'a') as textfile:
            textfile.write(error)
            textfile.close()

    return venue_list    

