# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 15:16:14 2018

@author: davil
"""
import os
import pandas as pd
import geopandas as gpd

#mx_df1 = pd.read_csv(os.path.join('resources','MEX_adm0.csv'))
#mx_df2 = pd.read_csv(os.path.join('resources','MEX_adm1.csv'))
#mx_df3 = pd.read_csv(os.path.join('resources','MEX_adm2.csv'))

mx_gdf1 = gpd.read_file(os.path.join('resources','gadm','MEX_adm0.shp'))
mx_gdf2 = gpd.read_file(os.path.join('resources','gadm','MEX_adm1.shp'))
mx_gdf3 = gpd.read_file(os.path.join('resources','gadm','MEX_adm2.shp'))

#very big!!!
mx_secciones = gpd.read_file(os.path.join('resources','oliveraherbert','SECCION.shp'))

import random
random_numbers = [random.randint(0,50) for _ in range(32)]

mx_gdf2['rnd'] = random_numbers

mx_gdf2.plot(column='rnd', cmap='OrRd')
#mx_secciones.plot()

from shapely.geometry import mapping
mx_gdf2['geometry'] = mx_gdf2['geometry'].apply(mapping)


from plotly.graph_objs import Scatter, Figure, Layout
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


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