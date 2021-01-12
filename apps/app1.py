# -*- coding: utf-8 -*-
"""

---------------------------------- APP1.py ----------------------------------
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

import pandas as pd
import json
import plotly.express as px

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
DF1=pd.read_json(DATA_PATH.joinpath('MBM_Data.json.gz'))
df_table1=pd.read_json(DATA_PATH.joinpath('MBM_ShortDesc.json.gz'))

#Meta-Information
#--------------------------
file_list=[
           'MBM_VarLab', 
           'MBM_ValueLab',
           'MBM_LongDesc',
           ]

meta_list={}
for f in file_list:
    with open(DATA_PATH.joinpath(f'{f}.json')) as json_file: 
        meta = json.load(json_file)
        meta_list[f'{f}']=meta



#---------------------------- DATA TABLE -------------------------------------
#DATA-Table MBM
#-------------------
data_table= dash_table.DataTable(
                            id='datatable-interactivity',
                            columns=[
                                {"name": i, 
                                 "id": i, 
                                 "deletable": False,
                                 "selectable": True} for i in df_table1.columns],
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
                            data=df_table1.to_dict('records'),
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



#--------------------- PAGE 1 (MBM-DATA) LAYOUT -------------------------------
layout = html.Div(
    [
     navbar.navbar_layout,
     dbc.Row( #Row 2 -> 4 + 5 +1
         [
             dbc.Col(
                [
                html.H1('MBM-Dataset'),
                html.H2('Codebook'),
                html.P('This part contains general Information about the Membership-Dataset'),
                ], 
                className='div-user-controls',
                width={'size':4,'offset':0},
                align='start',
                ),
             dbc.Col(
                dbc.Spinner(html.Div(id='miss-info')),
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
                 id='tabs-for-desc',
                 active_tab='tab_desc'
                 ),
             html.Div(id='var-description'),
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
             dbc.Col(dbc.Spinner(html.Div(id='plot-area')),
                className='div-for-charts',
                width=8
                ),
                
        ]
    ),
     ]
)


#------------------------------ CALLBACKS -------------------------------------

#Retrieve Data from Store
#-----------------------



#Data Table
#-----------------------------------------------------------------------------
#Update row Background, when row is selected
@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_rows')]
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
    Output('miss-info', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows"),
     ], #Input('memory-output', 'data')
    [State('datatable-interactivity', 'selected_rows')]
    )

def update_miss_case(rows,derived_virtual_selected_rows, selected_rows):
    #Acces first column of derived_data_table of selected row
    #I need the row_IDs of derive data_table ()
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
        
    if derived_virtual_selected_rows:
        DF=DF1
        df_table=df_table1
        var=df_table.iloc[selected_rows[0],0]
        VAR_lab=meta_list['MBM_VarLab']
        VAL_lab=meta_list['MBM_ValueLab']
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
    Output('var-description', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows"),
     Input('tabs-for-desc', 'active_tab'),
     ], #Input('memory-output', "data")
     [State('datatable-interactivity', 'selected_rows')]
    )

def update_description(rows,derived_virtual_selected_rows, at, selected_rows):
    #Acces first column of derived_data_table of selected row
    #I need the row_IDs of derive data_table ()
    #print(rows, derived_virtual_selected_rows,at)
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
        
    if derived_virtual_selected_rows:

        DF=DF1
        df_table=df_table1
        var=df_table.iloc[selected_rows[0],0]
        VAR_lab=meta_list['MBM_VarLab']
        VAL_lab=meta_list['MBM_ValueLab']
        description=meta_list['MBM_LongDesc']
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
    Output('table-info', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows"),
     ], #Input('memory-output', "data")
    [State('datatable-interactivity', 'selected_rows')]
    )
def update_table_info(rows,derived_virtual_selected_rows, selected_rows):
    #Acces first column of derived_data_table of selected row
    #I need the row_IDs of derive data_table ()
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
        
    if derived_virtual_selected_rows:
        DF=DF1
        df_table=df_table1
        var=df_table.iloc[selected_rows[0],0]
        VAR_lab=meta_list['MBM_VarLab']
        VAL_lab=meta_list['MBM_ValueLab']
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
    
    
#Plot-Area
#---------------------------------
@app.callback(
   Output('plot-area', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows"),
     ], #Input('memory-output', "data")
    [State('datatable-interactivity', 'selected_rows')]
    )

def update_plot(rows,derived_virtual_selected_rows, selected_rows):
    #Acces first column of derived_data_table of selected row
    #I need the row_IDs of derive data_table ()
    if selected_rows is None:
        selected_rows = []
    if selected_rows:
        DF=DF1
        df_table=df_table1
        var=df_table.iloc[selected_rows[0],0]
        VAR_lab=meta_list['MBM_VarLab']
        VAL_lab=meta_list['MBM_ValueLab']
        var=df_table.iloc[selected_rows[0],0]
        stats=help_functions.save_stats(DF,var, VAR_lab, VAL_lab,
                         missings=[x for x in range(-9,1)])
        #print(stats)
        #print(f'''Selected VAR: {var} with dtype {stats['Data-type']}''')
        
        #Integer type variable
        #---------------------------------------------
        if 'int' in stats['Data-type']:
            #Return Statement for Integers
            #-----------------------------
            graph=html.Div([
            dcc.RadioItems(
                id='int_radio',
                options= [{'label': i, 'value': i} for i in ['Absolut', 'Percentage (%)']],
                labelStyle={
                    'display': 'inline-block',
                    'padding':'10px',
                    'font': 'Open Sans Semi Bold'
                    },
                value='Absolut'),
            dcc.Graph(id='int_plot')
            ],)
            return graph
        
        #Float-Variables
        #---------------
        if 'float' in stats['Data-type']:
            fig=help_functions.create_figure(DF, var,
                          var_lab=VAR_lab,
                          val_lab=VAL_lab, 
                          missings=[x for x in range(-9,1)])
            graph=html.Div(dcc.Graph(id='float_plot', figure=fig))
            return graph
        
        #String-Objects
        #----------
        if 'object' in stats['Data-type']:
            min_r=0
            max_r=20
            graph=html.Div([
                dcc.Graph(id='str_plot'),
                dcc.Slider(
                    id='str_plot_slider',
                    min=1,
                    max=max_r,
                    step=1,
                    value=5,
                    marks={x:f'#{y}' for x,y in zip(range(min_r,max_r), range(min_r,max_r))}
                    ),
                ],
                )
            return graph


#Update figure (for integers)
#----------------------
@app.callback(
    Output('int_plot', "figure"),
    [Input('int_radio', 'value')], #Input('memory-output', "data")
    [State('datatable-interactivity', 'selected_rows')]
    )
def update_int_graph(value, selected_rows):
    DF=DF1
    df_table=df_table1
    VAR_lab=meta_list['MBM_VarLab']
    VAL_lab=meta_list['MBM_ValueLab'] #VAL LAB is none
    var=df_table.iloc[selected_rows[0],0]
    print(VAL_lab[var])
    stats=help_functions.save_stats(DF,var, VAR_lab, VAL_lab,
                     missings=[x for x in range(-9,1)])
    print(stats['Data-type'])
    if 'int' in stats['Data-type']:
        print('INTEGER FIGURE!')
        fig1, fig2=help_functions.create_figure(
            DF, 
            var,
            var_lab=VAR_lab, 
            val_lab=VAL_lab, 
            missings=[x for x in range(-9,1)]
            )
        
        if value =='Absolut':
            #fig1.show()
            return fig1
        else:
            #fig2.show()
            return fig2

#Update figure (for strings)
#-----------------------------
@app.callback(
    Output('str_plot', "figure"),
    [Input('str_plot_slider', 'value'),
      ], #Input('memory-output', "data")
    [State('datatable-interactivity', 'selected_rows')])
def update_str_graph(value, selected_rows):
    DF=DF1
    df_table=df_table1
    VAR_lab=meta_list['MBM_VarLab']
    VAL_lab=meta_list['MBM_ValueLab']
    var=df_table.iloc[selected_rows[0],0]
    stats=help_functions.save_stats(DF,var, VAR_lab, VAL_lab,
                     missings=[x for x in range(-9,1)])
    if 'object' in stats['Data-type']:
        #print(type(value))
        #print(f'VALUE-Range= {value[0]} - {value[1]}') 
        fig=help_functions.create_figure(DF, var, var_lab=VAR_lab,
                           top=value)
        #fig.show()
        return fig
























