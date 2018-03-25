# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 13:05:24 2018

@author: davil
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
import os
#from shapely.geometry import Polygon

mexican_states_people = {'AGS': 20,'BC': 57, 'BCS': 562, 'CAMP': 594,'CHIH': 442,'CHIS': 69,'COAH': 100,'COL': 237,'DF': 7323,'DGO': 689,'GRO': 40,'GTO': 295,'HGO': 1134,'JAL': 875,'MEX': 1,'MICH': 393, 'MOR': 301,'NAY': 404,'NL': 327,'OAX': 391,'PUE': 670,'QRO': 270,'QROO': 156,'SIN': 63,'SLP': 689,'SON': 291,'TAB': 306,'TAMPS': 59,'TLAX': 108,'VER': 17,'YUC': 35,'ZAC': 890}
exit()
m = Basemap(llcrnrlon=-115,llcrnrlat=5,urcrnrlon=-80,urcrnrlat=35,
            resolution='i',projection='tmerc',lon_0=-99,lat_0=19)
m.readshapefile(os.path.join('resources','MEX_adm1'), "mexican_states")

max_people = np.max(mexican_states_people.values())

for coordinates, state in zip(m.mexican_states, m.mexican_states_info):
    print state
    if state["NAME_1"] in mexican_states_people.keys():
        shade = mexican_states_people[state["NAME_1"]]/max_people


m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')
m.drawparallels(np.arange(-40,61.,2.))
m.drawmeridians(np.arange(-20.,21.,2.))
m.drawmapboundary(fill_color='aqua')
plt.title("Mexico")
plt.show()