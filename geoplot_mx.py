# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 15:16:14 2018

@author: davil
"""
import os
import pandas as pd
import geopandas as gpd
import sys
local_path = os.path.join(__file__)
local_path = local_path[:local_path.rfind('/')]
local_path = local_path[:local_path.rfind('/')] +'/plotly.py'
sys.path.insert(0,local_path )
import plotly
import plotly.plotly as py

#mx_df1 = pd.read_csv(os.path.join('resources','MEX_adm0.csv'))
#mx_df2 = pd.read_csv(os.path.join('resources','MEX_adm1.csv'))
#mx_df3 = pd.read_csv(os.path.join('resources','MEX_adm2.csv'))

mx_gdf1 = gpd.read_file(os.path.join('resources','gadm','MEX_adm0.shp'))
#Mexico's state info
mx_gdf2 = gpd.read_file(os.path.join('resources','gadm','MEX_adm1.shp'))
#Mexico's electoral districts info
mx_gdf3 = gpd.read_file(os.path.join('resources','gadm','MEX_adm2.shp'))

#very big!!!
#mx_secciones = gpd.read_file(os.path.join('resources','oliveraherbert','SECCION.shp'))
#mx_secciones.plot()

import random

random_numbers = [random.randint(0,50) for _ in range(32)]
mx_gdf2['rnd'] = random_numbers
mx_gdf2.plot(column='rnd', cmap='OrRd')
#from shapely.geometry import mapping
#mx_gdf2['geometry'] = mx_gdf2['geometry'].apply(mapping)
print('GEOPANDAS plot succeeded now onto ploting with plotly')


from plotly.graph_objs import Scatter, Figure, Layout
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

#crime_df = pd.read_csv(os.path.join('resources','crimes.csv'))
#
#plotly.tools.set_credentials_file(username='alandavila', api_key='PLKr3xS5w3So5LOafw3h')
#
#scl = [[0.0, 'rgb(585,580,587)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
#            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(65,39,123)']]
#
#data = [ dict(
#        type='choropleth',
#        colorscale = scl,
#        autocolorscale = False,
#        locations = crime_df['State'],
#        z = crime_df['2016'].astype(float),
#        locationmode = 'USA-states',
#        text = crime_df['2016'],
#        marker = dict(
#            line = dict (
#                color = 'rgb(255,255,255)',
#                width = 2
#            ) ),
#        colorbar = dict(
#            title = "Crime per 100k habitants")
#        ) ]
#
#layout = dict(
#        title = 'Crime rate per State (2016)',
#        geo = dict(
#            scope='usa',
#            projection=dict( type='albers usa' ),
#            showlakes = True,
#            lakecolor = 'rgb(255, 255, 255)'
#            ),
#            )
#        
#fig = dict( data=data, layout=layout )        

import plotly.figure_factory as ff
mex_fips = pd.read_csv('resources/gadm/MEX_adm2.csv')
mex_fips['fips'] = mex_fips['ID_1'] + mex_fips['ID_2']
mex_fips = list(mex_fips['fips'])
fig = ff.create_mx_choropleth(mex_fips,list(range(len(mex_fips))))

plot( fig, filename='mx_map.html' )

#scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
#            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
#
#mx_gdf2['text'] = mx_gdf2['NAME_1']
#
#data = [ dict(
#        type='choropleth',
#        colorscale = scl,   
#        #autocolorscale = False,
#        locations = mx_gdf2['geometry'],
#        z = mx_gdf2['ID_0'].astype(float) + random.randint(0,50),
#        #locationmode = 'USA-states',
#        text = mx_gdf2['text'],
#        #marker = dict(
#        #    line = dict (
#        #        color = 'rgb(255,255,255)',
#        #        width = 2
#        #    ) ),
#        colorbar = dict(
#            title = "Title here")
#        ) ]
#
#layout = dict(
#        title = 'Mexico states',
#        geo = dict(
#            scope='world',
#            #lonaxis =  { range: [-30, 60] },
#            #lataxis = { range: [-113, -105] },
#            #projection=dict( type='albers usa' ),
#            #showlakes = True,
#            lakecolor = 'rgb(255, 255, 255)'),
#             )
#    
#fig = dict( data=data, layout=layout )
#plot( fig, filename='d3-cloropleth-map' )