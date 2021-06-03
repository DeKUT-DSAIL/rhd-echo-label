import dash
import dash_table
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import pandas as pd
import os
import plotly
#authentication library
from flask import request
#timestamp to date time
import datetime
#imagelist library.
from modules.imagelist import imagelist
#image slider
from modules.slideimages import slideimages

list_of_validation = ['Correct', 'NOT CORRECT']

list_of_views = ['Parasternal long axis (PLAX)','Parasternal short axis(PSAX)','Apical Four Chamber(A4C)','Apical three chamber (A3C)','Apical two chamber(A2C)','Suprasternal(SSN)','Subcostal']

list_of_conditions = ['Mitral Valve Regurgitation','Aortic Valve Regurgitation','Tricuspid Valve Regurgitation','Pulmonary Valve Regurgitation','Aortic Valve Stenosis','Mitral Valve Stenosis','Tricuspid Valve Stenosis','Pulmonary Valve Stenosis','Mitral Valve Prolapse']

list_of_severities = ['Normal','Borderline rhd','Definite rhd']
    

# external CSS stylesheets
external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                        "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                        "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]

dash_app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app = dash_app.server
x = 0 #the default image, my code has been built around the default being 0.#esp in single click.
y = 0 #default1 when both clicked. #used when next_time_greater thanprev_timestamp
z = 0 #default2 when both clicked. #used when prev_time_greater than next_timestamp
imagenames = imagelist('./assets/static/images')

dash_app.title = "RHD Annotation Quality Control Check"

df = pd.read_csv('RHD-Data - ValidationSet.csv')
csv_list = []
for row_index, row in df.iterrows():
    csv_list.append((row['FILENAME'],  ',', ' ', row['VIEW'], ',', ' ', row['COLOUR']))


dash_app.layout = html.Div([
    html.Div([
        html.H1("Quality Control Check"),
        html.Img(src="/assets/favicon.ico"),
    ], className="banner"),
 html.Div(style = {'textAlign' : 'center'},
                        children = [
                                    html.Div(html.Img(id = 'image-seen',src = imagenames[x],width = '700px',height = '500px')),
                                        
                                        html.P(),
                                        html.Div(children = [html.Div(id='annotation',children='Current annotation of the image')]),
                                        html.Div(csv_list[0]),
                                        html.P(),
                                        html.Div(style = {'display': 'flex','align-items':'center','justify-content':'center'},
                                        children = [html.P(children = [dcc.Dropdown(id = 'validate',
                                                                        options = [ {'label' : i , 'value' : i} for i in list_of_validation], #list of checks
                                                                        placeholder = "Select validation status of current annotation ",
                                                                        multi = True,
                                                                        style={'height': '30px', 'width': '800px', 'textAlign' : "middle"}),

                                                                        html.P(),
                                                                        dcc.Dropdown( id = 'view',
                                                                            options = [{'label' : j,'value': j } for j in list_of_views],#list of views
                                                                            placeholder = "Select the view of the echocardiogram",
                                                                            style={'height': '30px', 'width': '800px', 'textAlign' : 'center'}),

                                                                        html.P(),
                                                                        dcc.Dropdown(id = 'condition',
                                                                        options = [ {'label' : i , 'value' : i} for i in list_of_conditions], #list of conditions
                                                                        placeholder = "Select the condition or conditions",
                                                                        multi = True,
                                                                        style={'height': '30px', 'width': '800px', 'textAlign' : "middle"}),
                                                            
                                                                        html.P(),
                                                                        dcc.Dropdown( id = 'severity',
                                                                            options = [{'label' : j,'value': j } for j in list_of_severities],#list of severities
                                                                            placeholder = "Select Severity of RHD",
                                                                            style={'height': '30px', 'width': '800px', 'textAlign' : 'center'}),
                                        html.P(),
                                        html.P(children = [ html.Div(id = 'prevend'),html.Button('Prev',id = 'prevbutton'),html.Button('Next', id = 'nextbutton'),html.Div(id = 'nextend')],),

                                        html.P(),
                                        html.Button('Submit', id = 'submit',style = {'color' : 'red'},autoFocus = True),
                                        html.Div(id = 'thesubmitted'),
                                     
                                    html.P(),
                                    html.Div(children = [html.Div(id='inference',children='Annotation for images'),
                                    
                                    dash_table.DataTable(
                                                id='table',
                                                columns=[{"name": i, "id": i} for i in df.columns],
                                                data=df.to_dict('records'),
                                                export_format="csv",
                                                page_size=5)

                                   
                                                    ])])
                                    ])])
])

#Manage the image slider.
@dash_app.callback(
    dash.dependencies.Output('image-seen','src'),
    [dash.dependencies.Input('prevbutton','n_clicks'),
    dash.dependencies.Input('nextbutton','n_clicks'),],
    [dash.dependencies.State('prevbutton','n_clicks_timestamp'),
    dash.dependencies.State('nextbutton','n_clicks_timestamp'),
    dash.dependencies.State('image-seen','src')]
    )
def slide_images(ncp,ncn,ncpts,ncnts,current_image_path):
    nextimage = slideimages(ncp,ncn,ncpts,ncnts,current_image_path,imagenames)
    return nextimage


if __name__ == '__main__':
    dash_app.run_server(debug = True)