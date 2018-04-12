import os
import pandas as pd
import geopandas as gpd
import sys
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


mex_districts = mx_df3#pd.read_csv('resources/gadm/MEX_adm2.csv')
#create a new column with the state id and district id concatenated
#we will use that information as input of mx choropleth map
#ID_1 == state id
#ID_2 == district id
mex_districts['ID_1'] =  mex_districts['ID_1'].apply(lambda x: str(x))
mex_districts['ID_2'] =  mex_districts['ID_2'].apply(lambda x: str(x))
mex_districts['district_id'] = mex_districts[['ID_1', 'ID_2']].apply(lambda x: ''.join(x), axis=1)
mex_districts['district_id'] = mex_districts['district_id'].apply(lambda x: int(x))
mex_districts_list = list(mex_districts['district_id'])

def get_state_votes_of(party = ['TOTAL_VOTOS']):
    '''
    Input (list) partye:
    Output (Series) mx_pres_percent
    '''
    #READ votes results per "seccion electoral"
    mx_pres_2012_df = pd.read_csv(os.path.join('resources','Presidente2012Seccion.csv'),\
                              encoding ='latin_1')
    #Add votes if party has more than one entry (coalition)
    if len(party) > 1:
        coalition = '-'.join(party)
        mx_pres_2012_df[coalition] = mx_pres_2012_df[party][:].sum(axis=1)
        party=coalition
    else:
        party = party[0]
        mx_pres_2012_df = mx_pres_2012_df[['ID_ESTADO','NOMBRE_ESTADO',party]]
    #aggregate results by state
    mx_pres_2012_gp = mx_pres_2012_df.groupby(['NOMBRE_ESTADO'])
    mx_pres_2012_total = mx_pres_2012_gp[party].sum()
    mx_pres_2012_percent = mx_pres_2012_total/mx_pres_2012_total.sum()
    mx_pres_2012_percent = mx_pres_2012_percent.apply(lambda x: 100*round(x,2))
    return mx_pres_2012_percent
#2012 coalitions:
#['PAN']
#['PRI', 'PVEM', 'NVA_ALIANZA', 'PRI_PVEM']
# ['PRD', 'PT', 'MC', 'PRD_PT_MC', 'PRD_PT', 'PRD_MC', 'PT_MC']  
#['NUM_VOTOS_NULOS', 'NUM_VOTOS_CAN_NREG']
#['TOTAL_VOTOS']
#['LISTA_NOMINAL']    
total_votes = get_state_votes_of(party=['TOTAL_VOTOS'])

mex_districts['per_state_vote'] = ''
for _ in range(1, 33):
    mex_districts['per_state_vote'][mex_districts['ID_1'] == str(_)] = total_votes[_ - 1]
    print(total_votes[_ - 1])
    
mex_districts_values = list(mex_districts['per_state_vote'])


def generate_colorscale(lcolor, dcolor, bins = 30, values=None):
    vmax = max(values)
    vmin = min(values)
    binning = []
    scl = []
    for i in range(0,bins - 1):
        x = vmin + (i/(bins-2))*(vmax - vmin)
        binning.append(round(x, 3))
    for i in range(0,bins ):
        a = lcolor + i*(dcolor - lcolor)/(bins - 1)
        b = lcolor + i*(dcolor - lcolor)/(bins - 1)
        scl.append(f'rgb({int(a)},{int(b)},{255})')
    scl = [i for i in reversed(scl)]
    return scl, binning
    
scl, binning_endpoints = generate_colorscale(15,200,32,mex_districts_values)

fig = ff.create_mx_choropleth(mex_districts_list,\
                              mex_districts_values, \
                              colorscale=scl,\
                              binning_endpoints=binning_endpoints)
plot( fig, filename='mx_map.html' )
