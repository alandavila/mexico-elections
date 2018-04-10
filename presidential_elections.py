import os
import pandas as pd
import geopandas as gpd
import sys
import random
local_path = os.path.join(__file__)
local_path = local_path[:local_path.rfind('/')]
local_path = local_path[:local_path.rfind('/')] +'/plotly.py'
sys.path.insert(0,local_path )

from plotly.graph_objs import Scatter, Figure, Layout
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.figure_factory as ff

mx_df1 = pd.read_csv(os.path.join('resources','gadm','MEX_adm0.csv'))
#Mexico's state info
mx_df2 = pd.read_csv(os.path.join('resources','gadm','MEX_adm1.csv'))
#Mexico's  districts info
mx_df3 = pd.read_csv(os.path.join('resources','gadm','MEX_adm2.csv'))

mx_gdf1 = gpd.read_file(os.path.join('resources','gadm','MEX_adm0.shp'))
#Mexico's state info
mx_gdf2 = gpd.read_file(os.path.join('resources','gadm','MEX_adm1.shp'))
#Mexico's  districts info
mx_gdf3 = gpd.read_file(os.path.join('resources','gadm','MEX_adm2.shp'))


mex_districts = pd.read_csv('resources/gadm/MEX_adm2.csv')

mex_districts['ID_1'] =  mex_districts['ID_1'].apply(lambda x: str(x))
mex_districts['ID_2'] =  mex_districts['ID_2'].apply(lambda x: str(x))
mex_districts['district_id'] = mex_districts[['ID_1', 'ID_2']].apply(lambda x: ''.join(x), axis=1)
mex_districts['district_id'] = mex_districts['district_id'].apply(lambda x: int(x))
mex_districts_list = list(mex_districts['district_id'])
#fig = ff.create_mx_choropleth(mex_districts_list,list(range(len(mex_districts_list))))
#plot( fig, filename='mx_map.html' )

#READ votes results per "seccion electoral"
mx_pres_2012_df = pd.read_csv(os.path.join('resources','Presidente2012Seccion.csv'),\
                              encoding ='latin_1	')
#Total votes per state
mx_pres_2012_df = mx_pres_2012_df[['ID_ESTADO','NOMBRE_ESTADO','TOTAL_VOTOS']]
#aggregate results by state
mx_pres_2012_gp = mx_pres_2012_df.groupby(['NOMBRE_ESTADO'])
mx_pres_2012_total = mx_pres_2012_gp['TOTAL_VOTOS'].sum()
mx_pres_2012_percent = (100)*mx_pres_2012_total/mx_pres_2012_total.sum()


mex_districts['per_state_vote'] = ''
for _ in range(1, 33):
    mex_districts['per_state_vote'][mex_districts['ID_1'] == str(_)] = mx_pres_2012_percent[_ - 1]
    print(mx_pres_2012_percent[_ - 1])
    
mex_districts_values = list(mex_districts['per_state_vote'])
fig = ff.create_mx_choropleth(mex_districts_list,mex_districts_values)
plot( fig, filename='mx_map.html' )
