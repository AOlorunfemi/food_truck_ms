#imports 
import googlemaps 
import pandas as pd 
from math import radians, cos, sin, asin, sqrt
import numpy as np


#haversine_distance formula ti calculate this distance between two points
def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   
   return np.round(res, 2)


def mylocation(address,client): #using Google api to get input address's lattitude and Longitude
    geocode = client.geocode(address=address)
    new_geocode_df = pd.DataFrame(geocode) #turns the geocode results into a dataframe
    extraction = new_geocode_df["geometry"].apply(pd.Series) 
    extraction_location = extraction["location"].apply(pd.Series)  #extracting longitude and latitude to make tables
    new_geocode_df = new_geocode_df.join(extraction_location["lng"]) # adding those columns to the overall dataframe
    new_geocode_df = new_geocode_df.join(extraction_location["lat"])
    new_geocode_df=new_geocode_df.rename(columns ={'lng':'lon'}) 
    new_geocode_df = new_geocode_df.loc[:, ['formatted_address','lat','lon']] #want only the address and the lat,long in the table
    return new_geocode_df

def getfood_truck_locations(address,client):
    new_geocode_df = mylocation(address,client) #getting the address dataframe from previous function
    start_lat, start_lon = new_geocode_df['lat'], new_geocode_df['lon']
    food_truck= pd.read_csv("Mobile_Food_Facility_Permit.csv")
    food_truck = food_truck.loc[:, ['Latitude','Longitude','FacilityType','LocationDescription','Applicant']]
    food_truck = food_truck.rename(columns ={'Latitude':'lat', 'Longitude':'lon'})
    
    distances_km = []
    for row in food_truck.itertuples(index=False): #interating over the food truck latitude and longitude and then gicing us our dinstance from our "address"
        distances_km.append(haversine_distance(start_lat, start_lon, row.lat, row.lon) ) 
    
    food_truck['Distance'] = distances_km
    food_truck['Distance'] = food_truck['Distance'].astype('float64')
    
    food_truck = food_truck[(food_truck['Distance'] <= 2) & (food_truck['Distance'] !=0)]
    
    return food_truck.head() #returns first 5 


def main(): 
    
    API_KEY = ''
    client = googlemaps.Client(API_KEY)
    address = input("Enter Address: ")
    file_path = pd.read_csv("Mobile_Food_Facility_Permit.csv")

    print(mylocation(address,client)) 
    print(getfood_truck_locations(address,client))

if __name__ == "__main__":
    main()