#!/usr/bin/env python
# coding=utf-8
# Author: Alexandre Connat ©

################################################################################################
### PYTHON UTILS FILE FOR CHLOROPETH MAP VIZUALISATION TOOL OF THE NETWORKED READINESS INDEX ###
### FROM THE WORLD ECONOMIC FORUM (http://wef.ch/gitr16)                                     ###
################################################################################################

import json
import plotly
import pandas as pd

####### SETTING API-KEY FOR PLOT.LY #######
def getUsernameAndAPIKeyFromFile(FILENAME='credentials.json'):
    JSON_FILE = open(FILENAME)
    credentials = json.load(JSON_FILE)
    USERNAME = credentials['username']
    API_KEY = credentials['api_key']
    JSON_FILE.close()
    return USERNAME, API_KEY

username, api_key = getUsernameAndAPIKeyFromFile('credentials.json') # Usually stored in ~/.plotly/.credentials
plotly.tools.set_credentials_file(username, api_key)
import plotly.plotly as py
############################################


############## PRE-PROCESSING ##############
FILENAME = 'WEF_NRI_2012-2016_Historical_Dataset.xlsx'
xls = pd.ExcelFile(FILENAME)

GLOBAL_DF = xls.parse('Data', skiprows=1)
GLOBAL_DF = GLOBAL_DF.reset_index()

ISO_CODES = GLOBAL_DF[GLOBAL_DF['index'] == 0].values.tolist()[0][9:]
COUNTRIES = GLOBAL_DF[GLOBAL_DF['index'] == 1].values.tolist()[0][9:]
ISO_MAPPING = dict(zip(COUNTRIES, ISO_CODES)) # ISO_MAPPING['Mexico'] --> 'MEX'

GLOBAL_DF = xls.parse('Data', skiprows=3)
GLOBAL_DF = GLOBAL_DF.reset_index()
############################################




def get_dataframe(date, indicator, rank=False): # rank=False returns the actual VALUE, and rank=True the rank / 153
    if rank:
        return GLOBAL_DF[ (GLOBAL_DF['Attribute'] == 'Rank') & (GLOBAL_DF['Edition'] == date) & (GLOBAL_DF['Code NRI 2016'] == indicator) ]
    else:
        return GLOBAL_DF[ (GLOBAL_DF['Attribute'] == 'Value') & (GLOBAL_DF['Edition'] == date) & (GLOBAL_DF['Code NRI 2016'] == indicator) ]


# Should return dataframe of this format :
# COUNTRY | ISO_CODE | RANK | VALUE |
# France     FRA        16     5.87
# Italy      ITA        28     5.02
# etc ...
def create_dataframe(date, indicator):
    df_rank = get_dataframe(date=date, indicator=indicator, rank=True)
    df_value = get_dataframe(date=date, indicator=indicator, rank=False)

    values = []

    for country in COUNTRIES:
        value = []
        value.append(country) # Name of the country
        value.append(ISO_MAPPING[country]) # ISO Country code
        value.append(df_rank[country].values[0]) # Rank of country for the indicator
        value.append(df_value[country].values[0]) # Value of the indicator for this country
        values.append(value)

    df = pd.DataFrame(data=values, columns=['COUNTRY', 'ISO_CODE', 'RANK', 'VALUE'])

    return df

def plot_map_for_indicator(indicator, date=2016, rank=False):

    df = create_dataframe(date=date, indicator=indicator)

    if rank:
        to_display = df['RANK']
        descriptor = '(rank / 139)'
    else:
        to_display = df['VALUE']
        descriptor = '(value)'

    data = [ dict(
            type = 'choropleth',
            locations = df['ISO_CODE'],
            z = to_display,
            text = df['COUNTRY'],
            colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],[0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
            autocolorscale = False,
            reversescale = not rank,
            marker = { 'line': {'color': 'rgb(180,180,180)','width': 0.5} },
            colorbar = dict(
                        autotick = False,
                        tickprefix = '',
                        title = str(indicator) + '<br>' + descriptor
                       )
         ) ]

    layout = dict(
            title = 'Networked Readiness Index<br>Source: <a href="http://wef.ch/gitr16">World Economic Forum</a>',
            geo = dict(
                    showframe = False,
                    showcoastlines = False,
                    projection = {'type': 'Mercator'}
                  )
         )

    fig = {'data':data, 'layout':layout}
    nice_plot = py.iplot(fig, validate=False, filename='d3-world-map')

    return nice_plot
