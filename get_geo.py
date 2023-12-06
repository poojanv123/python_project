import certifi
import ssl
import pandas as pd
import geopy.distance
import geopy.geocoders
from geopy.geocoders import Nominatim
import os

#read data
os.chdir('/Users/pooja/final-project-poojanv123')
tourist_cities = pd.read_excel('tourist_cities.xlsx',sheet_name="Sheet1")

# Initialize Nominatim API
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim(user_agent="MyApp")

#Get location data
tourist_cities['location'] = tourist_cities['City'].map(geolocator.geocode)
tourist_cities.dropna(subset=['location'],inplace=True)
tourist_cities['Latitude'] = tourist_cities['location'].apply(lambda x: x.latitude)
tourist_cities['Longitude'] = tourist_cities['location'].apply(lambda x: x.longitude)
tourist_cities.to_excel('tourist_cities_latlong.xlsx', index=False,sheet_name="Sheet1")

