import time
import googlemaps 
import pandas as pd 
import matplotlib.pyplot as plt 
import descartes 
import geopandas as gpd
from shapely.geometry import Point, Polygon


API_KEY = ''
map_client = googlemaps.Client(API_KEY)
street_map = gpd.read_file('/Users/abayomiolorunfemi/Downloads/kx-city-of-san-francisco-california-streets-SHP (1)')

def miles_to_meters(miles):
    try:
        return miles * 1_609.344
    except:
        return 0
    

def getFoodTruck(search_string, address, client):
    food_trucks = []
    distance = miles_to_meters(2)
    geocode = client.geocode(address=address)
    (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))
    
    response = map_client.places_nearby(
    location=(lat, lng),
    keyword=search_string,
    radius=distance
    )   
    food_trucks.extend(response.get('results'))
    df = pd.DataFrame(food_trucks)
    food_truck = df.loc[:,['name','vicinity','rating','opening_hours','geometry']]
    food_truck_df = food_truck[0:5]
    
    return food_truck_df

def main(): 
    
    API_KEY = 'AIzaSyAfj6kAIRfKwli1Uhm-XIxCWsu6YoSx74s'
    client = googlemaps.Client(API_KEY)
    street_map = gpd.read_file('/Users/abayomiolorunfemi/Downloads/kx-city-of-san-francisco-california-streets-SHP (1)')

    address = input("Enter Address: ")
    search_string = input("Enter place of interest: " )


    print(getFoodTruck(search_string, address,client))
    print(mapping(search_string, address, client,street_map))



if __name__ == "__main__":
    main()



