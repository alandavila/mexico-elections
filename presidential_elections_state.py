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


mex_states = mx_df2#pd.read_csv('resources/gadm/MEX_adm2.csv')
#create a new column with the state id and district id concatenated
#we will use that information as input of mx choropleth map
#ID_1 == state id
#ID_2 == district id
mex_states['ID_1'] =  mex_states['ID_1'].apply(lambda x: str(x))
mex_states['district_id'] = mex_states['ID_1']
mex_states['district_id'] = mex_states['district_id'].apply(lambda x: int(x))
mex_states_list = list(mex_states['district_id'])

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
        mx_pres_2012_df = mx_pres_2012_df[['ID_ESTADO','NOMBRE_ESTADO', 'LISTA_NOMINAL', party]]
    #aggregate results by state
    mx_pres_2012_gp = mx_pres_2012_df.groupby(['NOMBRE_ESTADO'])
    #need to provide list to group by in order to get a dataframe
    tmp_list = []
    tmp_list.append(party)
    mx_pres_2012_total = mx_pres_2012_gp[tmp_list].sum()
    mx_pres_2012_nominal = mx_pres_2012_gp[['LISTA_NOMINAL']].sum()
    #normalize by states total voters
    merged = pd.merge(mx_pres_2012_nominal,mx_pres_2012_total, left_index=True, right_index=True)
    mx_pres_2012_percent = merged[party]/merged['LISTA_NOMINAL']
    mx_pres_2012_percent = mx_pres_2012_percent/mx_pres_2012_percent.sum()
    mx_pres_2012_percent = mx_pres_2012_percent.apply(lambda x: 100*round(x,2))
    return mx_pres_2012_percent
#2012 coalitions:
#['PAN']
#['PRI', 'PVEM', 'NVA_ALIANZA', 'PRI_PVEM']
# ['PRD', 'PT', 'MC', 'PRD_PT_MC', 'PRD_PT', 'PRD_MC', 'PT_MC']  
#['NUM_VOTOS_NULOS', 'NUM_VOTOS_CAN_NREG']
#['TOTAL_VOTOS']
#['LISTA_NOMINAL']    
total_votes = get_state_votes_of(party=['TOTAL_VOTOS']  )

mex_states['per_state_vote'] = ''
for _ in range(1, 33):
    mex_states['per_state_vote'][mex_states['ID_1'] == str(_)] = total_votes[_ - 1]
    #print(total_votes[_ - 1])
    
mex_state_values = list(mex_states['per_state_vote'])


def generate_colorscale(lcolor=[0,0,0], dcolor=[255,255,255], bins = 30, values=None):
    vmax = max(values)
    vmin = min(values)
    binning = []
    scl = []
    for i in range(0,bins - 1):
        x = vmin + (i/(bins-2))*(vmax - vmin)
        binning.append(round(x, 3))
    for i in range(0,bins ):
        r = lcolor[0] + i*(dcolor[0] - lcolor[0])/(bins - 1)
        g = lcolor[1] + i*(dcolor[1] - lcolor[1])/(bins - 1)
        b = lcolor[2] + i*(dcolor[2] - lcolor[2])/(bins - 1)
        scl.append(f'rgb({int(r)},{int(g)},{int(b)})')       
    scl = [i for i in reversed(scl)]
    return scl, binning

morena_colors = [[98,1,92],[232,197,230]]
pri_colors = [[140,7,7],[256,196,196]]
pan_colors = [[7, 18, 239], [214, 216, 255]]
prd_colors = [[249, 201, 7], [247, 229, 158]]
voters_colors = [[51, 50, 50], [209, 204, 204]]

scl, binning_endpoints = generate_colorscale(*voters_colors,32,mex_state_values)

fig = ff.create_mx_st_choropleth(mex_states_list,\
                              mex_state_values, \
                              colorscale=scl,\
                              binning_endpoints=binning_endpoints)
#html to view directly in browser
#plot( fig, filename='plot.html')
#div to embed on website
plot( fig, filename='voters_2012.html', include_plotlyjs=False, output_type='div')
