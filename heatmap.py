#%%
import geopandas as gpd
import fiona
from fiona.drvsupport import supported_drivers
import numpy as np
import statistics
import pandas as pd
import os
import time
from selenium import webdriver
import folium
from folium.plugins import HeatMap
from geopy.extra.rate_limiter import RateLimiter
import geopy
# ------------------------------
#       DATA TREATMENT
# ------------------------------

# READ KML file to a geopandas dataframe
#supported_drivers['LIBKML'] = 'rw'
#gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
#geo_df = gpd.read_file('doc.kml',driver='KML')
# Create Pandas Dataframe from GeoPandas
#df= pd.DataFrame(geo_df)
# Extract latitude and longitude from the KML geometry column
#df['latitud'] = df.geometry.apply(lambda p: p.y)
#df['longitud'] = df.geometry.apply(lambda p: p.x)
# Extract latitude and longitude from the KML geometry column
#df['latitud'] = df.geometry.apply(lambda p: p.y)
#df['longitud'] = df.geometry.apply(lambda p: p.x)

#Read personalized Excel file
df=pd.read_excel('Historial.xlsx')
df.rename(columns={'x':'longitud','y':'latitud'},inplace=True)
dfCoords=df.loc[:,['latitud','longitud']]

# leer el archivo excel que contiene los datos de localización
data = dfCoords.copy()
data['metric']=1 #Constante para sumar frecuencias

# fusionar el país, la ciudad y la calle en una sola cadena de direcciones
#data["addresses"] = data["country"] + ", " + data["city"] + ", " + data["street "]

# crear un objeto de servicio
#service = geopy.Nominatim(user_agent = "myGeocoder")

#data["coordinates"] = data["addresses"].apply(RateLimiter(service.geocode,min_delay_seconds=1)) # geocodificar cada dirección, utilizando el método .apply() para pandas DataFrame

#data.head() # mostrar un vistazo a la tabla de pandas DataFrame geocodificada

# extrayendo los valores de longitud y latitud a listas separadas
longs = list(data['longitud'])
lats = list(data['latitud'])
# calcular los valores medios de longitud y latitud para centrar las coordenadas en el mapa (Opcional para primer aproximación geografica)
#meanLong = statistics.mean(longs)
#meanLat = statistics.mean(lats)

########## Creación de mapa ##########
# crear un objeto mapa base usando Map()
centerCoordsMty=[25.68311113135739, -100.31776690411596] #Coordenadas centrales de la ciudad
mapObj = folium.Map(location=centerCoordsMty, zoom_start = 11)

heatmap = HeatMap( list(zip(lats, longs, data["metric"])),
                   min_opacity=0.2,
                   radius=50, blur=50,
                   max_zoom=1) # crear capa de mapa de calor

heatmap.add_to(mapObj) # añadir capa de mapa de calor al mapa base
#folium.raster_layers.TileLayer(tiles='Stamen Toner').add_to(mapObj) #añadir capa para vista en blanco y negro
#folium.LayerControl().add_to(mapObj) #Agregar toggle para seleccionar capa a observar de fondo
#%%
#delay=10
fn='testmap.html'
#tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
mapObj.save(fn)

