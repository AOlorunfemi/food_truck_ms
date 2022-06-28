import time
import googlemaps 
import pandas as pd 
import matplotlib.pyplot as plt 
import descartes 
import geopandas as gpd
from shapely.geometry import Point, Polygon


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
    
    response = client.places_nearby(
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
    
    API_KEY = ''
    client = googlemaps.Client(API_KEY)
    address = input("Enter Address: ")
    search_string = input("Enter place of interest: " )


    print(getFoodTruck(search_string, address,client)) 



if __name__ == "__main__":
    main()



