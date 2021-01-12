# -*- coding: utf-8 -*-
"""
--------------------------------- APP PY -------------------------------------

Created on Wed Jan  6 08:44:16 2021

@author: Megaport
"""

import dash
import dash_bootstrap_components as dbc

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, inittial-sacle=1.0'}])

server = app.server
