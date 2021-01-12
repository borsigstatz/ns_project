# -*- coding: utf-8 -*-
"""
--------------------------- HELPER FUNCTIONS ---------------------------------

Created on Wed Jan  6 10:32:08 2021

@author: Megaport
"""

import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#--------------------------------- FUNCTIONS ---------------------------------

#Save stats
#-----------------------------------------------------------------------------
def save_stats(df, VAR:str, var_lab:dict, var_val:dict, missings=[]):
    '''
    Save information and statistsics (e.g. number of unique values, 
    missings, range etc.) of a given variable (DataFrame column) for further 
    usage. Function will return the information as dictionary. 
    Returned information will vary depending on the dtype of the given variable.
    Examples:
        Integer
        --------
        type:  integer
        label:  gend
        range:  [-8,2]
        unique values:  4
        missing .:  0/50,325

        tabulation:  Freq.   Numeric  Label
                      6        -8     Nicht les-/zuweisbar
                     23        -7     Schwer interpretierbar
                     45,647     1     Maennlich
                     4,649      2     Weiblich
        Float
        ------
        type:  float
        range:  [15.389385,4658.8125]
        unique values:  42
        missing .:  28,110/50,325
        mean:   456.802
        std. dev:   1071.99
           percentiles:        10%       25%       50%       75%       90%
                           17.9837   23.4961   101.908   118.509   1653.13

        String
        -------
        type:  string (str29)

         unique values:  112
         missing "":  0/50,325

         examples:  "ESSEN"
                    "MITTELFRANKEN"
                    "RHEINPFALZ"
                    "SCHWABEN"
        warning:  variable has embedded blanks

    '''
    #Check if var is in df
    if VAR in df.columns:
        stats={}
        

        #Check data_type of variable
        #---------------------------
        valid_dtypes=['int64', 'float64', 'string', 'datetime64', 'object']
        data_type=str(df[VAR].dtype)
        
        if data_type not in valid_dtypes:
            raise ValueError(f'{data_type} is not a valid data-format')

        #Default Keys
        #------------
        #Variable name
        #stats['Variable name']=VAR
        
        #Variable label
        #----------------
        stats['Label']=var_lab[VAR] 
        
        #Data Type
        #----------
        stats['Data-type']=data_type
        
        #Count Unique Values
        #-------------
        unique=pd.unique(df[VAR])
        unique.sort()
        unique=unique.tolist()
        unique_count=len(unique)
        stats['Unique count']=unique_count
        
        #Missings
        #---------
        if is_numeric_dtype(df[VAR]):
            
            sysmiss=df[VAR].isna().sum()
            if df[VAR].isin(missings).any():#Ceck user defined missings (e.g -9)
                user_missing=df[VAR][df[VAR].isin(missings)].count()
                sysmiss=sysmiss+user_missing
                
                
            stats['Missing Values']=sysmiss
            stats['# of non missing']=df[VAR][~df[VAR].isin(missings)].count()
        
        
        #INTEGER
        #-------
            #if 'int' in data_type:
                #stats['Unique values']=unique #List
                #if var_val is not None:
                    #stats['Value label']=var_val[VAR] #Dict
            
        #FLOAT
        #-----
            if 'float' in data_type:
                #stats['Min']=f'{df[VAR][~df[VAR].isin(missings)].min():.2f}'
                #stats['Max']=f'{df[VAR][~df[VAR].isin(missings)].max():.2f}'
                stats['Mean']=f'{df[VAR][~df[VAR].isin(missings)].mean():.2f}'
                #stats['Std']=f'{df[VAR][~df[VAR].isin(missings)].std():.2f}'
        #STRING
        #-------
        if is_string_dtype(df[VAR]):
            sysmiss=(df[VAR].values == '').sum()
            usemiss=df[VAR][df[VAR].str.contains('^-[0-9]', regex=True)].count()
            stats['Missing Values']=sysmiss + usemiss
            stats['# of non missing']=df[VAR].count()-stats['Missing Values']
    else:
        raise ValueError(f'Variable {VAR} was not found in {df}')
    '''
    #Print results
    #-------------
    for k,v1 in stats.items():
        if isinstance(v1, dict):
            print(k)
            for k2,v2 in v1.items():
                print(k2, v2)
        else:
            print(k, v1)
    '''

    
    return stats
   

def list_stats(stats):
    htmlText = []
    for k,v1 in stats.items():
        if isinstance(v1, dict):
            htmlText.append(f'{k}')
            for k2,v2 in v1.items():
                htmlText.append(f'{k2} : {v2}')
        else:
            htmlText.append(f'{k} : {v1}')
    
    return htmlText


#Überarbeiten
#-------------
#Create figure
#---------------
def create_figure(df, var:str, **kwargs):
    var_lab=kwargs.get('var_lab', None)
    val_lab=kwargs.get('val_lab', None)
    missings=kwargs.get('missings', None)
    top=kwargs.get('top', None)
    data_type=str(df[var].dtype)
    
    
    
    #Check if  keys in value lab are int -> match to df index
    #---------------------------------------------------------
    
    
    
    '''
    if missings:
        #val_lab=val_lab[var]
        val_lab={k: val_lab[var][k] for k in val_lab[var] if k not in [str(x) for x in missings]}
        print(f'VAL LABS {val_lab}')
    '''
    #Basic-Layout
    #------------
    marker_color='rgb(255, 82, 2)'
    marker_line_color='rgb(255, 82, 2)'
    marker_line_width=1.5
    marker_opacity=1
    paper_bgcolor='rgb(50, 50, 50)'
    y_color='rgb(250,250,250)'
    x_color='rgb(250,250,250)'
    plot_bgcolor='rgb(50,50,50)'
    box_plot='rgb(2, 160, 207)'
    
    if missings:
        df=df[var][~df[var].isin(missings)]
    else:
        df=df[var]

    #INTEGER
    #---------------------
    if 'int' in data_type:
        #print('You choosed an integer!')
        
        #Basic Bar chart
        #---------------
        #Compute values
        data=pd.DataFrame(df.value_counts())
        #print(data)
        #print(f'VARIABLE LABEL {val_lab[var]}')
        data['prc']=(df.value_counts(normalize=True) * 100)
        
        #Value Labels
        val_lab=val_lab[var]
        val_lab={int(k): val_lab[k] for k in val_lab} 
        data['names']=pd.Series(val_lab)
        
        data.columns=['count','prc', 'names']
        #print(data)
        #print(val_lab[var])
        #Absolute Counts
        #---------------
        #print('TEST FIG 1')
        fig1=px.bar(data, 
            x='names',
            y='count',
            labels={'count':f'Count of {var}', 'names':''})
        #print(fig1)
        fig1.update_traces(marker_color=marker_color, 
                          marker_line_color=marker_line_color,
                          marker_line_width=marker_line_width, 
                          opacity=marker_opacity)
        fig1.update_layout(
        paper_bgcolor=paper_bgcolor,
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        yaxis=dict(
            color=y_color,
            showgrid=False,
            ),
        xaxis=dict(
            tickmode='auto',
            color=x_color),
        plot_bgcolor=plot_bgcolor
        )
        
        #%-Percentage
        #------------
        fig2=px.bar(data, 
            x='names',
            y='prc',
            labels={'prc':f'% of {var}', 'names':''})
        
        fig2.update_traces(marker_color=marker_color, 
                          marker_line_color=marker_line_color,
                          marker_line_width=marker_line_width, 
                          opacity=marker_opacity)
        fig2.update_layout(
        paper_bgcolor=paper_bgcolor,
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        yaxis=dict(
            tickmode='auto',
            color=y_color,
            showgrid=False,
            ),
        xaxis=dict(
            tickmode='auto',
            color=x_color),
        plot_bgcolor=plot_bgcolor
        )
        #fig1.show()
        return fig1, fig2
    #FLOAT
    #-------------------------
    if 'float' in data_type:
        #Histogram + Box-Plot
        #-----------------------
        fig=make_subplots(rows=1, cols=2)
        trace1=go.Histogram(
                        x=df,
                        name=var,
                        autobinx=True,
                        marker_color=marker_color
                        )
        trace2=go.Box(
                     y=df,
                     name=f'{var_lab[var]}',
                     boxmean=True,
                     fillcolor=paper_bgcolor,
                     opacity=0.75,
                     line_color='rgb(107,174,214)',
                     marker_color='rgb(107,174,214)',
                     marker_line_color=marker_line_color,
                     )

        fig.add_trace(trace1,row=1,col=1)
        fig.add_trace(trace2,row=1,col=2)
        
        fig.update_yaxes(showgrid=False,
                         tickmode='auto',
                         color=y_color,
                         autorange=True)
        fig.update_xaxes(showgrid=False,
                         tickmode='auto',
                         color=y_color,
                         autorange=True
                         )
        
        fig.update_layout(
            showlegend=False,
            paper_bgcolor=paper_bgcolor,
            uniformtext_minsize=8, 
            uniformtext_mode='hide',
            plot_bgcolor=plot_bgcolor,
                        )
        
        #fig.show()
        return fig
        

    #String Graph (top Answers)
    #-----------------------
    if 'object' in data_type:
        #print(f' {top}')
        top_df=df.groupby(df[~df \
                                  .str.contains('^-[0-9]', regex=True)]) \
                                  .count() \
                                  .sort_values(ascending=False)[:top] \
                                  .to_frame()
        
        top_df['name']=top_df.index
        top_df=top_df.reset_index(drop=True).sort_values(by=[var], ascending=True)
        
        #Plot
        #----------------
        fig=px.bar(top_df,
                   x=var,
                   y='name',
                   orientation='h',
                   labels={var:f'Count of {var}', 'name':f'Top #{top} strings'},
                   )
        
        fig.update_traces(
            marker_color=marker_color,
            marker_line_color=marker_line_color,
            marker_line_width=marker_line_width)
        
        fig.update_layout(
        paper_bgcolor=paper_bgcolor,
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        yaxis=dict(
            tickmode='auto',
            color=y_color,
            showgrid=False,
            ),
        xaxis=dict(
            tickmode='auto',
            color=x_color,
            showgrid=False),
        plot_bgcolor=plot_bgcolor
        )
        
        return fig
    

def generate_table(df):
    return dbc.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns]) ] +
        # Body
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(min(len(df),len(df)))],
    bordered=True,
    dark=True,
    hover=True,
    responsive=True,
    striped=True,
    style={'font-size':'11px',
           'margin-left':'0px',
           'overflowY': 'scroll',
           'overflowX':'auto'
           })


