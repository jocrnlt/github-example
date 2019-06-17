#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

get_ipython().system("conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab")
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

get_ipython().system("conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab")
import folium # map rendering library

print('Libraries imported.')


# In[15]:


#Get the coordinates while specifying column names
filename = 'https://cocl.us/Geospatial_data'
Lat_long_coord_df = pd.read_csv(filename)
Lat_long_coord_df.columns = ["Postal_Code","Latitude","Longitude"]


# In[11]:


#create Toronto data file from part 1 
from bs4 import BeautifulSoup
page = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M')
# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')
# Create a data frame from BeautifulSoup object soup
table = soup.find_all('table')[0] 
df = pd.read_html(str(table))[0]
Toronto_df=df

# Drop whole row with 'Not assigned' in "Borough" column
Toronto_df1=Toronto_df[Toronto_df.Borough != 'Not assigned']

# reset index, because we droped two rows
Toronto_df1.reset_index(drop=True, inplace=True)

#Replace Not assigned value with Borough for Neighbourhood
Toronto_df1.Neighbourhood.replace("Not assigned",Toronto_df1.Borough,inplace=True)

#More than one neighborhood can exist in one postal code area. 
#For example, in the table on the Wikipedia page, 
#you will notice that M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. 
#These two rows will be combined into one row with the neighborhoods separated with a comma

Toronto_df2 = Toronto_df1.groupby(by=['Postcode','Borough']).agg(lambda x: ','.join(x))
#Reset index to Postcode and Borough
Toronto_df2.reset_index(level=['Postcode','Borough'], inplace=True)

#rename columns 
Toronto_df2.rename(columns={'Postcode': 'PostalCode', 'Neighbourhood': 'Neighborhood'}, inplace=True)


# In[12]:


Toronto_df2.head()


# In[13]:


Lat_long_coord_df.head()


# In[16]:


Toronto_merged = Toronto_df2

# merge Toronto_merged with Lat_long_coord_df to add latitude/longitude for each postal code
Toronto_merged = Toronto_merged.join(Lat_long_coord_df.set_index('Postal_Code'), on='PostalCode')

Toronto_merged.head() # check all columns


# In[ ]:




