import folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

#a function for json data extraction 
def load_file(fileloc):
    data = []
    
    # read file line by line and strip white space
    with open(fileloc) as f:
        for line in f:            
            data.append(json.loads(line.rstrip()))
    return data

#load data file
data=load_file('yelp_academic_dataset_business.json')
bus_df=pd.DataFrame.from_dict(data)
bus_df['city'].value_counts()

#select businesses for Las Vegas 
vegas=bus_df[bus_df['city']=='Las Vegas']
vegas.shape
bus_df.shape
vegas1=vegas

#divide businesses per category 
cat_df=vegas['categories'].str.join(sep=',').str.get_dummies(sep=',')
cats=cat_df.columns.values
vegas=pd.merge(vegas,cat_df,left_index=True,right_index=True)
vegas['categories'].value_counts()

#keep the ones with high ratings
top_bus=vegas[vegas.stars>4.4]
top_bus

#extract Restaurants type and fashion type businesses 
top_bus['Restaurants'].value_counts()
top_bus.shape
top_bus.columns

top_res=top_bus[top_bus.Restaurants==1]
top_res.shape
top_fas=top_bus[top_bus.Fashion==1]
top_fas.shape

#only keep relevent columns
top_fash1=top_fas.loc[:,['city','postal_code','stars','state','neighborhood','latitude','longitude','is_open','business_id','name']]
top_res1=top_res.loc[:,['city','postal_code','stars','state','neighborhood','latitude','longitude','is_open','business_id','name']]

#display the fashion businesses in Las Vegas
map2=folium.Map(location=[36.1699, -115.1398],zoom_start=13)
for index,row in top_fash1.iterrows():
  folium.Marker(location=[row['longitude'],row['latitude']],popup=row['name']).add_to(map2)

map2.save('test.html')

#Read zip codes and its Longitude Latitude 
zip_cord=pd.read_csv('US Zip Codes from 2013 Government Data',skiprows=1)
zip_cord.columns

#extract zip,long,lat for las vegas 
vg_zips=zip_cord[(zip_cord['ZIP']>89100) & (zip_cord['ZIP']<89200)
]
vg_zips.columns

#read income data from us census 
income=pd.read_csv('vegas_income.csv',skiprows=[1])
income=income.rename(index=str,columns={"name":"ZIP","B19013001":"income","B19013001,":""})
vg_zips.columns

#megre income data with zip data based on zip code 
j1=pd.merge(income,vg_zips,on='ZIP')

#plot the income level in map along with fashion business distribution 
map3=folium.Map(location=[36.1699, -115.1398],zoom_start=13)

for index,row in top_fash1.iterrows():
  folium.Marker(location=[row['latitude'],row['longitude']],popup=row['name']).add_to(map3)

for index,row in j1.iterrows():
    folium.CircleMarker(location=[row['LAT'],row['LNG']],radius=row['income']/100,color='#e2d814',fill_color='#e2d814').add_to(map3)

map3.save('final.html')
