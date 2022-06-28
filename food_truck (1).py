#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time
import googlemaps 
import pandas as pd 
import matplotlib.pyplot as plt 
import descartes 
import geopandas as gpd
from shapely.geometry import Point, Polygon

get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


API_KEY = 'AIzaSyAfj6kAIRfKwli1Uhm-XIxCWsu6YoSx74s' #initialize API KEY TO PASS INTO CLIENT
map_client = googlemaps.Client(API_KEY)


# In[4]:


def miles_to_meters(miles): # need to convert miles to meters 
    try:
        return miles * 1_609.344 #
    except:
        return 0


# In[5]:


search_string = input("Enter keyword to search(Food Truck):") #google API takes a search string 
distance = miles_to_meters(2) # want to do in a 2 mile radius so we convert the miles to meters from the helper function
food_trucks = [] # empty list, we are going to put our list of food trucks in this list
address = input("Enter address:")


# In[6]:


geocode = map_client.geocode(address=address) #using geo code to extract the long, and lat from the address 
(lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))


# In[7]:


response = map_client.places_nearby(
    location=(lat, lng),
    keyword=search_string,
    radius=distance
)   

food_trucks.extend(response.get('results'))

df = pd.DataFrame(food_trucks)


# In[8]:


food_trucks_2= df.loc[:,['name','vicinity','rating','opening_hours','geometry']]


# In[10]:


food_trucks_2[0:5] #displays top 5 closest food trucks 


# In[12]:


food_trucks_2=food_trucks_2[0:5]


# In[14]:


lat_long_extraction=food_trucks_2["geometry"].apply(pd.Series) # 
new_2=lat_long_extraction.loc[:,['location']] #Isolate
new_3 = new_2['location'].apply(pd.Series)


# In[18]:


street_map = gpd.read_file('/Users/abayomiolorunfemi/Downloads/kx-city-of-san-francisco-california-streets-SHP (1)')


# In[19]:


fig,ax = plt.subplots(figsize=(15,15)) 
street_map.plot(ax = ax)


# In[20]:


geometry = [Point(xy) for xy in zip (new_3["lng"], new_3["lat"])]
geometry[:3]


# In[21]:


new_geocode_df = pd.DataFrame(geocode)
extraction = new_geocode_df["geometry"].apply(pd.Series)
extraction_location = extraction["location"].apply(pd.Series)
geometry_2 = [Point(xy) for xy in zip (extraction_location["lng"], extraction_location["lat"])]
geometry_2 


# In[22]:


geo_df = gpd.GeoDataFrame(food_trucks_2,
                         geometry = geometry)
geo_df_2 = gpd.GeoDataFrame(new_geocode_df,
                         geometry = geometry_2)


# In[23]:


geo_df_2


# In[24]:


geo_df


# In[25]:


fig,ax = plt.subplots(figsize = (8,8))
street_map.plot(ax =ax, alpha =0.4, color="grey")
geo_df.plot(ax=ax, marker='o', color='red', markersize=15, label="Food Trucks")
geo_df_2.plot(ax=ax, marker='o', color='blue', markersize=15, label= "Your Position")
plt.legend(prop={'size': 15})


# In[ ]:




