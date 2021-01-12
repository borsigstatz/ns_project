# -*- coding: utf-8 -*-
"""

--------------------------------- HOME-PAGE ----------------------------------
Created on Wed Jan  6 11:43:23 2021

@author: Megaport
"""

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from apps import navbar


#----------------------------------- HOME PAGE --------------------------------

layout=html.Div([
    navbar.navbar_layout,
    dbc.Container([
        html.Br(),
        html.H1('NSDAP Project'),
        html.P('This is the main section'),
        html.H3('Project History'),
        html.P('This part contains basic information about the NSDAP-Project'),
        html.H3('Go to Dataset'),
        dbc.ButtonGroup(
            [dbc.Button('MBM-Dataset', href="/page-1", id='mbm2', n_clicks_timestamp='0'), 
             dbc.Button('GEM-Dataset',  href="/page-2", id='gem2', n_clicks_timestamp='0'), 
             dbc.Button('Motiv-Dataset', href="/page-3", id='motiv2', n_clicks_timestamp='0')
             ],
            id='select-df2',
            vertical=True)
    ])
])


#-------------------------------- CALLBACKS ----------------------------------

#Button -> Go to Page

