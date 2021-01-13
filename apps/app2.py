# -*- coding: utf-8 -*-
"""

---------------------------------- APP2.py ----------------------------------
Created on Wed Jan  6 08:44:50 2021

@author: Megaport
"""
from app import app

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table
from apps import navbar

import os
import pathlib
import time

import pandas as pd
import json
import plotly.express as px
import geojson
import geopandas

#Import functions
from apps import help_functions


#PROBLEM: DATA MUST BE SHARED -> RETRIEVE DATA FROM STORE!!
#data

#-------------------------------- DATA IMPORT ---------------------------------
#os.chdir(r"C:\Users\Megaport\Desktop\Arbeit\Dash_Multi_Page\datasets")

PATH= pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../datasets').resolve()

#Data
#-------------------------------------
DF2=pd.read_json(DATA_PATH.joinpath('GEM_Data.json.gz'))
df_table2=pd.read_json(DATA_PATH.joinpath('GEM_ShortDesc.json.gz'))

#Select only plottable values (e.g. population etc.)
df_table2=df_table2[df_table2['Variable'].str.contains('^n[0-9]', regex=True)]


#Map-Data
#--------------------------------------
gau_data=geopandas.read_file(DATA_PATH.joinpath('gau_map.geojson'))
kreis_data=geopandas.read_file(DATA_PATH.joinpath('kreis_map.geojson'))


#Meta-Information
#--------------------------
file_list=[
           'GEM_VarLab', 
           'GEM_ValueLab',
           'GEM_LongDesc',
           ]

meta_list={}
for f in file_list:
    with open(DATA_PATH.joinpath(f'{f}.json')) as json_file: 
        meta = json.load(json_file)
        meta_list[f'{f}']=meta
        
        
#DATA-Table GEM
#-------------------
data_table= dash_table.DataTable(
                            id='datatable-interactivity2',
                            columns=[
                                {"name": i, 
                                 "id": i, 
                                 "deletable": False,
                                 "selectable": True} for i in df_table2.columns],
                            style_table={
                                'maxHeight': '300ex',
                                'overflowY': 'scroll',
                                'overflowX':'auto',
                                'width': '100%',
                                'minWidth': '30%',
                                'height': 300,
                            },
                            style_header={
                            'textAlign': 'left',
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'fontWeight': 'bold',
                            'font-family': "Open Sans Semi Bold, sans-serif"
                            },
                            style_cell={
                            'textAlign': 'left',
                            'font-family': "Open Sans Semi Bold, sans-serif",
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color':'white',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0,
                            },
                            style_filter={
                            'backgroundColor': 'rgb(200, 200, 200)',
                            },
                            data=df_table2.to_dict('records'),
                            editable=False,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable="single",
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[0],
                            page_action="none",
                            page_current= 0,
                            page_size= 10,
                            fixed_rows={'headers': True},
                            )

#--------------------- PAGE 2 (GEM-DATA) -------------------------------------
layout = html.Div(
    [
     navbar.navbar_layout,
     dbc.Row( #Row 2 -> 4 + 5 +1
         [
             dbc.Col(
                [
                html.H1('GEM-Data'),
                html.H2('Codebook'),
                html.P('This part contains general Information about the GEM-Dataset'),
                ], 
                className='div-user-controls',
                width={'size':4,'offset':0},
                align='start',
                ),
             dbc.Col(
                dbc.Spinner(html.Div(id='miss-info2')),
                className='div-miss-pie',
                width=2,
                ),
             dbc.Col(
            [
                dbc.Spinner(html.Div([
                    dbc.Tabs(
                        [
                            dbc.Tab(label='Description', tab_id='tab_desc'),
                            dbc.Tab(label='Basic Info', tab_id='tab_info'),
                     
                        ],
                 id='tabs-for-desc2',
                 active_tab='tab_desc'
                 ),
             html.Div(id='var-description2'),
             ])),
            ]
        ,
            className='div-for-description',
             width=6)
             
        ],
    ),
     dbc.Row(
         [
             #Data-Table
             #-------
             dbc.Col(html.Div(data_table), 
                     className='div-user-controls',
                     width=4
                     ),
             #Map-Area
             #----------
             dbc.Col(
                 [
                
                
                html.Div([
                #Choose reference per Dropdwon -> default None
                html.Label([
                    'Choose a percentage base:',
                    dcc.Dropdown(
                    id='ref_drop',
                    options=[
                        {'label': x, 'value': x} for x in df_table2['Variable']
                    ],
                    searchable=True,
                    placeholder='Select..',
                    style={
                        'width':'49%',
                        }
                    ),
                html.P(id="map_ref", className="mt-3"),
                ]),
                #Tabs
                dbc.Tabs(
                        [
                            dbc.Tab(label='Gaue', tab_id='tab_gau'),
                            dbc.Tab(label='Districts', tab_id='tab_dis'),
                        ],
                    id='tabs_for_maps',
                    active_tab='tab_gau'
                 ),
                dbc.Spinner(html.Div(id='map-area')), 
                ]),
                ],
               className='div-for-charts',
                width=8),
             ]),
     ]
)

#------------------------------ CALLBACKS -------------------------------------

#Retrieve Data from Store
#-----------------------



#Data Table
#-----------------------------------------------------------------------------
#Update row Background, when row is selected
@app.callback(
    Output('datatable-interactivity2', 'style_data_conditional'),
    [Input('datatable-interactivity2', 'selected_rows')]
)
def update_styles(selected_rows):
    return [{
        'if': { 'row_index': i },
        'background_color': 'rgb(26, 123, 133)',
        'color':'rgb(250,250,250)'
    } for i in selected_rows]


#Missing-Values
#-----------------------------------------------------------------------------
@app.callback(
    Output('miss-info2', "children"),
    [Input('datatable-interactivity2', "derived_virtual_data"),
     Input('datatable-interactivity2', "derived_virtual_selected_rows"),
     ], #Input('memory-output', 'data')
    [State('datatable-interactivity2', 'selected_rows')]
    )

def update_miss_case(rows,derived_virtual_selected_rows, selected_rows):
    #Acces first column of derived_data_table of selected row
    #I need the row_IDs of derive data_table ()
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
        
    if derived_virtual_selected_rows:
        DF=DF2
        df_table=df_table2
        var=df_table.iloc[selected_rows[0],0]
        VAR_lab=meta_list['GEM_VarLab']
        VAL_lab=meta_list['GEM_ValueLab']
        stats=help_functions.save_stats(DF,var, VAR_lab, VAL_lab,
                         missings=[x for x in range(-9,1)])
        #Chart 1: % of Missing Values (pie chart)
        #------------------------------------------
        values=[['Missings', int(stats['Missing Values'])], 
                ['Valid',int(stats['# of non missing'])]]
        df_miss = pd.DataFrame(values, columns=['names', 'values'])
        no_miss=(df_miss['values'][1]/df_miss['values'].sum())*100
        fig=px.pie(df_miss, values='values', names='names', color='names',
                   color_discrete_map={
                       'Missings':'rgb(50,50,50)',
                       'Valid':'rgb(2, 160, 207)'},
                   hole=0.6,
                   #opacity=0.8
                   )
        fig.update_layout(
            title=dict(
                text='Valid Cases',
                y=0.95,
                x=0.55,
                xanchor='center',
                yanchor='top',
                font_family='Arial'
                ),
        title_font_size=18,
        title_font_color='rgb(250,250,250)',
        annotations=[dict(
            text=f'{no_miss:3.1f}%', 
                          x=0.21, 
                          y=0.5, 
                          font_size=13,
                          font_color='rgb(250, 250, 250)',
                          showarrow=False)],
        width=120, 
        height=120,
        autosize=True,
        margin=dict(l=20, r=20, t=28, b=20),
        paper_bgcolor="rgb(50, 50, 50)",
        showlegend=False,
        )
        fig.update_traces(hovertemplate=None,
                          textinfo='none',
                          )
        
        #Missing-Pie-Box
        #--------------
        missing_pie=[
            dcc.Graph(id='pie_miss',
                      figure=fig,
                      style={'width':'35%',
                             'height':'35%',
                             'padding-top': '15px'}),
            ]
        return missing_pie

#Description-Block (with Tabs)
#--------------------------------------
@app.callback(
    Output('var-description2', "children"),
    [Input('datatable-interactivity2', "derived_virtual_data"),
     Input('datatable-interactivity2', "derived_virtual_selected_rows"),
     Input('tabs-for-desc2', 'active_tab'),
     ], #Input('memory-output', "data")
     [State('datatable-interactivity2', 'selected_rows')]
    )

def update_description(rows,derived_virtual_selected_rows, at, selected_rows):
    #Acces first column of derived_data_table of selected row
    #I need the row_IDs of derive data_table ()
    #print(rows, derived_virtual_selected_rows,at)
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
        
    if derived_virtual_selected_rows:

        DF=DF2
        df_table=df_table2
        var=df_table.iloc[selected_rows[0],0]
        VAR_lab=meta_list['GEM_VarLab']
        VAL_lab=meta_list['GEM_ValueLab']
        description=meta_list['GEM_LongDesc']
        stats=help_functions.save_stats(DF,var, VAR_lab, VAL_lab,
                         missings=[x for x in range(-9,1)])
        df_stats=pd.DataFrame(stats.items(), columns=['Variable', var])
        
        #Tab1
        #--------------
        if at == 'tab_desc':
            var_description=[
                dcc.Markdown(f'{description[var]}'),
                ]
            return var_description
        if at == 'tab_info':
            table_info=[
            help_functions.generate_table(df_stats)
            ]
        return table_info
            
    
#Stats-Table
#--------------------------------------
@app.callback(
    Output('table-info2', "children"),
    [Input('datatable-interactivity2', "derived_virtual_data"),
     Input('datatable-interactivity2', "derived_virtual_selected_rows"),
     ], #Input('memory-output', "data")
    [State('datatable-interactivity2', 'selected_rows')]
    )
def update_table_info(rows,derived_virtual_selected_rows, selected_rows):
    #Acces first column of derived_data_table of selected row
    #I need the row_IDs of derive data_table ()
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
        
    if derived_virtual_selected_rows:
        DF=DF2
        df_table=df_table2
        var=df_table.iloc[selected_rows[0],0]
        VAR_lab=meta_list['GEM_VarLab']
        VAL_lab=meta_list['GEM_ValueLab']
        var=df_table.iloc[selected_rows[0],0]
        stats=help_functions.save_stats(DF,var, VAR_lab, VAL_lab,
                         missings=[x for x in range(-9,1)])
        df_stats=pd.DataFrame(stats.items(), columns=['Variable', var])
        #Info_Box
        #--------------
        table_info=[
            help_functions.generate_table(df_stats)
            ]
        return table_info
    
#------------------------------------------------------------------------------
#Map-Callback
@app.callback(
   Output('map-area', "children"),
    [Input('datatable-interactivity2', "derived_virtual_data"),
     Input('datatable-interactivity2', "derived_virtual_selected_rows"),
     Input('tabs_for_maps', 'active_tab'),
     Input('ref_drop', 'value')
     ],
    [State('datatable-interactivity2', 'selected_rows')]
    )

def map_plot(rows,derived_virtual_selected_rows, at, value, selected_rows):
    if selected_rows is None:
        selected_rows = []
        #print(f'Selected Row is None')
    if selected_rows:
        DF=DF2
        df_table=df_table2
        var=df_table.iloc[selected_rows[0],0]
        
        
        #If Gau -> Aggregate GEM-Variables by GAU
        #------------------------------
        if at == 'tab_gau':
            if value:
                gau_agg=DF[['Gau',var, value]][DF['agglvl'].isin([4,5,6,7,8])].groupby(['Gau']).sum().reset_index()
            else:
                gau_agg=DF[['Gau',var]][DF['agglvl'].isin([4,5,6,7,8])].groupby(['Gau']).sum().reset_index()
            #Merge to geopandas
            #---------------------
            map_data=pd.merge(gau_data, gau_agg,
                   how='left',
                   on='Gau',
                   )
        #If District -> Aggregate GEM-Variables by krnr (ERROR!! Maybe State?!)
        #----------------------------------------------
        elif at == 'tab_dis':
            if value:
                kreis_agg=DF[['krnr',var, value]][DF['agglvl'].isin([4,5,6,7,8])].groupby(['krnr']).sum().reset_index()
            else:
                 kreis_agg=DF[['krnr',var]][DF['agglvl'].isin([4,5,6,7,8])].groupby(['krnr']).sum().reset_index()
            #Merge to geopandas
            #---------------------
            map_data=pd.merge(kreis_data, kreis_agg,
                   how='left',
                   on='krnr',
                   )
            #time.sleep(5)
        
        #Compute %Share (based on Reference)
        #------------------------------------
        if value:
            map_data[var]=(map_data[var][map_data[var] >= 0] /map_data[value][map_data[value] >= 0])*100
            print(map_data[var])
        
        #Draw Map
        #------------------------------
        map_fig = px.choropleth(map_data,
                   geojson=map_data.geometry,
                   locations=map_data.index,
                   color=var,
                   color_continuous_scale="Viridis",
                   hover_name='Name',
                   )
        
        
        '''
        #Map-Box Style
        map_fig = px.choropleth_mapbox(map_data,
                   geojson=map_data.geometry,
                   locations=map_data.index,
                   color=var,
                   hover_name='Name',
                   mapbox_style="carto-positron",
                   zoom=4.4, 
                   center = {"lat": 52.5200, "lon": 13.4049},
                   opacity=0.75,
                   )
        '''
        
        map_fig.update_layout(height=400, #width=1000, 
                              margin={"r":0,"t":0,"l":0,"b":0},
                              geo=dict(bgcolor= 'rgb(50,50,50)',
                                       ),
                              paper_bgcolor='rgb(50,50,50)',
                              coloraxis_colorbar=dict(
                                  tickfont_color='rgb(250,250,250)',
                                  titlefont_color='rgb(250,250,250)',
                                  )
                              )

        map_fig.update_geos(fitbounds="locations", 
                            visible=False,
                            subunitcolor='white',
                            )
        
        return html.Div(dcc.Graph(figure=map_fig))


#Map-Referencer
@app.callback(
    Output("map_ref", "children"), 
    [Input('ref_drop', 'value')]
)
def map_referencer(value):
    if value:
        return f"Reference: {meta_list['GEM_VarLab'][value]}"
    return "Reference: None"

