import requests
import datetime
import json
#Weather station at the PDX Airport
latitude = '45.5958'
longitude = '-122.6093'
office = 'PQR'
gridX = '115'
gridY = '106'

# URL and query elements for the NOAA Web site
base_url = 'https://api.weather.gov/gridpoints/'
full_url = base_url + office + '/' + gridX + ',' + gridY + '/forecast'



def get_noaa_data():
    # GET the response from the NWS server
    response = requests.get(full_url)
    
    # Format the response object as JSON
    data = response.json()
    data = data["properties"]["periods"][0]
    
    temp = data["temperature"]
    prec = data["probabilityOfPrecipitation"]["value"]
    
    # parse forcast
    forcast = data["detailedForecast"].lower()
    sun = "sun" in forcast
    cloud =  "cloud" in forcast
    rain = "rain" in forcast
    
    sunpct = 0
    if sun and not cloud:
         sunpct = 100
    elif sun and cloud:
        sunpct = 50
    elif not rain and cloud:
        sunpct = 25
    elif rain and cloud:
        sunpct = 0
        
    # Farenheit,  % 0-100,  % 0-100
    return  temp, prec, sunpct, 
    
    
