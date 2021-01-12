# -*- coding: utf-8 -*-
"""

---------------------------------- INDEX.py ----------------------------------

-> First Page loaded

Created on Wed Jan  6 08:44:50 2021

@author: Megaport
"""

#Connect to main app.py file
from app import app
from app import server

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

#Connect to pages
from apps import homepage, app1, app2, app3
#from apps import navbar


#--------------------------- APP LAYOUT --------------------------------------
app.layout = html.Div([
    dcc.Store(id='memory-output', storage_type='session'), #Store Data #storage_type='session'
    dcc.Location(id='url', refresh=False),
    #html.Div(id='intermediate_value', style={'display': 'none'}), #hidden signal
    html.Div(id='page-content'),
    
])



#------------------------ CALLBACKS ------------------------------------------


#URL ROUTING
#------------------------------------------------------------------------------
#NAV BAR Callbacks
# we use a callback to toggle the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# the same function (toggle_navbar_collapse) is used in all three callbacks
for i in [1, 2, 3]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return app1.layout
    elif pathname == '/page-2':
        return app2.layout
    elif pathname == '/page-3':
        return app3.layout
    else:
        return homepage.layout
    # You could also return a 404 "URL not found" page here

#DATA-STORE
# ----------------------------------------------------------------------------
#Store Data in dcc.Store


#----------------------------------- END -------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)