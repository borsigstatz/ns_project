# -*- coding: utf-8 -*-
"""
------------------------------------ NAVBAR ----------------------------------
Created on Wed Jan  6 09:57:58 2021

@author: Megaport
"""


import dash_html_components as html
import dash_bootstrap_components as dbc


#--------------------------------- NAV BAR ------------------------------------
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
# Single Links
#-----------------------------------------------------
nav_item = dbc.NavItem(dbc.NavLink("Home", href="/"))

# Drop down menu
#-------------------------------------------------------
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("MBM-Dataset", href="/page-1", id='mbm1'),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("GEM-Dataset", href="/page-2", id='gem1'),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Motiv-Dataset", href="/page-3", id='motiv1'),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
    id='select-df1'
)

#Define NAVBAR
#----------------------------
navbar_layout = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Logo", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://plot.ly",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item, dropdown], className="ml-auto", 
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
                
            ),
        ]
    ),
    color='',
    dark=True,
    className="nbar",
    sticky='top',
    #style={'background_color': 'rgb(250,250,250)'}
)