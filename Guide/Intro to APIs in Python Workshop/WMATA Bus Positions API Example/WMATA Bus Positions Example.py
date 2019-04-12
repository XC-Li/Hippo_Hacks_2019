
# coding: utf-8

# ## WMATA Bus Positions Example

# Import pandas library for data analysis and requests library for API requests

# In[1]:


import pandas as pd
import requests


# Add header for WMATA API key

# In[2]:


headers = {'api_key': '5d7494bbde0c411981d3832703734b09'}


# API request for bus positions

# In[3]:


bus_positions = requests.get('https://api.wmata.com/Bus.svc/json/jBusPositions', headers=headers)


# Status code for bus position request

# In[4]:


bus_positions.status_code


# Decode bus positions JSON

# In[5]:


bus_positions_json = bus_positions.json()


# Parse through bus positions JSON and convert it to a pandas dataframe

# In[6]:


BlockNumber = []
DateTime = []
Deviation = []
DirectionNum = []
DirectionText = []
Lat = []
Lon = []
RouteID = [] 
TripEndTime = [] 
TripHeadsign = []
TripID = []
TripStartTime = []
VehicleID = []

for i in bus_positions_json['BusPositions']:
    BlockNumber.append(i['BlockNumber'])
    DateTime.append(i['DateTime'])
    Deviation.append(i['Deviation'])
    DirectionNum.append(i['DirectionNum'])
    DirectionText.append(i['DirectionText'])
    Lat.append(i['Lat'])
    Lon.append(i['Lon'])
    RouteID.append(i['RouteID'])
    TripEndTime.append(i['TripEndTime']) 
    TripHeadsign.append(i['TripHeadsign'])
    TripID.append(i['TripID'])
    TripStartTime.append(i['TripStartTime'])
    VehicleID.append(i['VehicleID'])
    
bus_positions_df = pd.DataFrame(list(zip(BlockNumber, DateTime, Deviation, DirectionNum, DirectionText, Lat, Lon, RouteID, 
    TripEndTime, TripHeadsign, TripID, TripStartTime, VehicleID)), 
    columns=['BlockNumber','DateTime', 'Deviation', 'DirectionNum', 'DirectionText', 'Lat', 'Lon', 'RouteID',
            'TripEndTime', 'TripHeadsign', 'TripID', 'TripStartTime', 'VehicleID'])


# Preview of bus positions dataframe

# In[7]:


bus_positions_df.head()


# Export bus positions to a CSV file

# In[8]:


bus_positions_df.to_csv('bus_positions.csv', encoding = 'utf-8')

