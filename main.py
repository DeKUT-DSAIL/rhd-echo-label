import dash
import dash_auth
import pandas as pd
import mysql.connector
import dash.dependencies
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from flask import request
from time import strftime
from modules.slides import slides
#from dash import html, dcc #use for dash 2.0.0
from mysql.connector import errorcode
from modules.imagelist import imagelist
from modules.clouddata import cloud_data
from modules.slideimages import slideimages
from dash_bootstrap_components._components.ModalBody import ModalBody
from dash_bootstrap_components._components.ModalHeader import ModalHeader
from dash_bootstrap_components._components.PopoverBody import PopoverBody
#from modules.annotationlist import filelist



#Username password pairs(Private)
VALID_USERNAME_PASSWORD_PAIRS = {
    #list username password pairs here
}

# external CSS stylesheets
external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                        "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                        "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]

dash_app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
                        meta_tags=[{'name': 'viewport',
                                    'content': 'width=device-width, initial-scale=1.0'}]
                    )

app = dash_app.server

auth = dash_auth.BasicAuth(
    dash_app,
    VALID_USERNAME_PASSWORD_PAIRS
)

dash_app.title = "RHD Annotation Quality Control Check"

list_of_validation = ['Correct', 'Not Correct']

list_of_views = ['Parasternal long axis (PLAX)','Parasternal short axis(PSAX)','Apical Four Chamber(A4C)','Apical three chamber (A3C)','Apical two chamber(A2C)','Suprasternal(SSN)','Subcostal','Doppler']

list_of_thickness_state = ['Thick', 'Not Thick', 'Not Applicable']

list_of_conditions = ['Mitral Valve Regurgitation','Aortic Valve Regurgitation','Tricuspid Valve Regurgitation','Pulmonary Valve Regurgitation','Aortic Valve Stenosis','Mitral Valve Stenosis','Tricuspid Valve Stenosis','Pulmonary Valve Stenosis','Mitral Valve Prolapse','Not Applicable']

list_of_severities = ['Normal','Borderline rhd','Definite rhd','Not Applicable']

x = 0 

imagenames = cloud_data("rhd_imaging_data")  #this is the cloud storage bucketname

#imagenames = imagelist("./assets/static")
#annotation = filelist('./assets/static')   

df = pd.read_csv('RHD-Data.csv', encoding='utf-8')

annotation = []

for index, row in df.iterrows():
    annotation.append((row['FILENAME'],' ',',',' ',row['VIEW'],' ',',',' ', row['COLOUR']))

#cloud_sql_mysql_create_socket
db_user = "root"
db_password = "dsail2021"
db_name = "rhd_db"
host = '127.0.0.1' #local server
port= '3306'
cloud_sql_connection_name = "rhd-imaging-325212:us-west1:rhd-imaging" #use sql connection name given on GCP when hosting on GCP
unix_socket = "/cloudsql/{}".format(cloud_sql_connection_name)

#unix_socket = "{}/{}".format(
#     db_socket_dir,
#     cloud_sql_connection_name
# )

conn = mysql.connector.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name) #use host=host inplace of unix socket when using a local mysql server

cursor = conn.cursor()

#connect to database
def create_connection(conn):
    try:
        host = '127.0.0.1:3306'
        conn = mysql.connector.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name) 
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your usrname or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        conn.close()
        
#create a table in the rhd_db database and give it a connection
TABLES = {}
TABLES['rhdtest1'] = (
    "CREATE TABLE `rhdtest1`("
    " `FILENAME` varchar(255) NOT NULL,"
    " `VIEW` varchar(255) NOT NULL,"
    " `COLOUR` varchar(255) NOT NULL,"
    " `VALIDATE` varchar(255) NOT NULL,"
    " `VIEW_OF_ECHO` varchar(255) NOT NULL,"
    " `THICKNESS_STATE` varchar(255) NOT NULL,"
    " `CONDITIONS` varchar(255) NOT NULL,"
    " `SEVERITY` varchar(255) NOT NULL,"
    " `USER` varchar(255) NOT NULL,"
    " `TIMETAKEN` varchar(255) NOT NULL"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} ".format(db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
try:
    cursor.execute("USE {}".format(db_name))
except mysql.connector.Error as err:
    print("Database does not exist.".format(db_name))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(db_name))
        conn.database = db_name
    else:
        print(err)
        exit()

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
conn.close()

dash_app.layout = html.Div([
    html.Div([
        html.H1("Quality Control Check"),
        html.Img(src="/assets/favicon.ico"),
    ], className="banner"),

    dbc.Button('Welcome to the App.', id="open", n_clicks=0),
    dbc.Modal([
        dbc.ModalHeader('Welcome.'),
        dbc.ModalBody('You have successfully been authorized.'),
        dbc.ModalFooter(
                dbc.Button('Close', id='close')
        )],
        id="modal",
        centered=True,
        is_open=True,),

 html.Div(style = {'textAlign' : 'center'},
                        children = [
                                    html.Div(html.Iframe(id = 'children',src = imagenames[x],width = '645px',height = '485px')),

                                        html.P(),
                                        html.Div(children = [html.Div(id='annotation',children='Current annotation of the image')]),
                                        html.Div(id = 'imagelen', children = annotation[x]),
                                        html.P(),
                                        html.Div(style = {'display': 'flex','align-items':'center','justify-content':'center'},
                                        children = [html.P(children = [html.Label("VALIDATE"),
                                                                        dcc.Dropdown(id = 'validate',
                                                                        options = [ {'label' : i , 'value' : i} for i in list_of_validation], #list of checks
                                                                        placeholder = "Select validation status of current annotation",
                                                                        style={'height': '30px', 'width': '800px', 'textAlign' : "middle"}),

                                                                        html.P(),
                                                                        html.Label("VIEW OF ECHO"),
                                                                        dcc.Dropdown( id = 'view',
                                                                            options = [{'label' : i,'value': i } for i in list_of_views],#list of views
                                                                            placeholder = "Select the view of the echocardiogram",
                                                                            style={'height': '30px', 'width': '800px', 'textAlign' : 'center'}),

                                                                        html.P(),
                                                                        html.Label("THICKNESS STATE"),
                                                                        dcc.Dropdown(id = 'thickness',
                                                                            options = [ {'label' : i , 'value' : i} for i in list_of_thickness_state], #list of thickness_state
                                                                            placeholder = "Select the state of thickness",
                                                                            style={'height': '30px', 'width': '800px', 'textAlign' : "center"}),
                                                                            
                                                                        html.P(),
                                                                        html.Label("CONDITIONS"),
                                                                        dcc.Dropdown(id = 'conditions',
                                                                            options = [ {'label' : i , 'value' : i} for i in list_of_conditions], #list of conditions
                                                                            placeholder = "Select the condition or conditions",
                                                                            multi = True,
                                                                            style={'height': '30px', 'width': '800px', 'textAlign' : "center"}),
                                                            
                                                                        html.P(),
                                                                        html.Label("SEVERITY"),
                                                                        dcc.Dropdown( id = 'severity',
                                                                            options = [{'label' : i,'value': i } for i in list_of_severities],#list of severities
                                                                            placeholder = "Select Severity of RHD",
                                                                            style={'height': '30px', 'width': '800px', 'textAlign' : 'center'}),
                                        html.P(),
                                        dbc.Button('Save', id = 'save', color='info'),
                                        html.Div(id = 'thesaved'),

                                        dbc.Popover(
                                            [dbc.PopoverHeader('Saving to database...'),
                                            dbc.PopoverBody('Successfully saved!')],
                                            id='popover',
                                            trigger='legacy',
                                            is_open=False,
                                            target='save'
                                        ),

                                        html.P(),
                                        html.P(children = [ html.Div(id = 'prevend'),dbc.Button('Prev',id = 'prevbutton', color='secondary'),
                                        dbc.Button('Next', id = 'nextbutton', color='secondary'),html.Div(id = 'nextend')]),
                                        
                                        html.Div(id = 'database', children = []),
                                        
                                                        ])
                                        ])])
])

#Manage the image slider.
@dash_app.callback(
    dash.dependencies.Output('children','src'),
    [dash.dependencies.Input('prevbutton','n_clicks'),
    dash.dependencies.Input('nextbutton','n_clicks'),],
    [dash.dependencies.State('prevbutton','n_clicks_timestamp'),
    dash.dependencies.State('nextbutton','n_clicks_timestamp'),
    dash.dependencies.State('children','src')]
    )
def slide_images(ncp,ncn,ncpts,ncnts,current_image_path):
    nextimage = slideimages(ncp,ncn,ncpts,ncnts,current_image_path,imagenames)
    return nextimage

#Manage the annotation slider
@dash_app.callback(
    dash.dependencies.Output('imagelen','children'),
    [dash.dependencies.Input('prevbutton','n_clicks'),
    dash.dependencies.Input('nextbutton','n_clicks'),],
    [dash.dependencies.State('prevbutton','n_clicks_timestamp'),
   dash.dependencies.State('nextbutton','n_clicks_timestamp'),
    dash.dependencies.State('imagelen','children')]
    )
def slide_ann(pre,nex,prets,nexts,x):
    nextannotation = slides(pre,nex,prets,nexts,x,annotation)
    return nextannotation

#Update and connect to mysql database
@dash_app.callback(
    dash.dependencies.Output('database','children'),
    [dash.dependencies.Input('validate', 'value'),
    dash.dependencies.Input('view', 'value'),
    dash.dependencies.Input('thickness', 'value'),
    dash.dependencies.Input('conditions', 'value'),
    dash.dependencies.Input('severity', 'value'),
    dash.dependencies.Input('save', 'n_clicks')],
    [dash.dependencies.State('save', 'n_clicks_timestamp'),
    dash.dependencies.State('nextbutton', 'n_clicks')]
)


def update_output_data(validate,view,thickness,conditions,severity,n_clicks,timestamp,nex):
    username = request.authorization['username']
    #address =  request.remote_addr

    y = 0
    if nex == None:
        x = 0
        if n_clicks != None:
            conn = mysql.connector.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
            cursor = conn.cursor()
            timestamp = strftime("%Y-%m-%d %H:%M:%S")
            add_annotation = """INSERT INTO rhdtest1 
            (FILENAME, VIEW, COLOUR,VALIDATE,VIEW_OF_ECHO,THICKNESS_STATE,CONDITIONS,SEVERITY,USER,TIMETAKEN)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            values = ((annotation[x][y]), (annotation[x][y+4]), (annotation[x][y+8]), validate, view, thickness, str((conditions)), severity, str((username)), timestamp)

            
            cursor.execute(add_annotation,values)
            print("Data annotated successfully.")
            conn.commit()
            

            cursor.close()
            conn.close()

    elif nex != None:
        if n_clicks == nex + 1:
            x = nex
            conn = mysql.connector.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name) 
            cursor = conn.cursor()
            timestamp = strftime("%Y-%m-%d %H:%M:%S")
            add_annotation = """INSERT INTO rhdtest1 
            (FILENAME, VIEW, COLOUR,VALIDATE,VIEW_OF_ECHO,THICKNESS_STATE,CONDITIONS,SEVERITY,USER,TIMETAKEN)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            values = ((annotation[x][y]), (annotation[x][y+4]), (annotation[x][y+8]), validate, view, thickness, str((conditions)), severity, str((username)), timestamp)

            
            cursor.execute(add_annotation,values)
            print("Data annotated successfully.")
            conn.commit()
            
                

            cursor.close()
            conn.close()



#Trigger popover to show data has been saved successfully to the database
@dash_app.callback(
    dash.dependencies.Output('popover', 'is_open'),
    [dash.dependencies.Input('save', 'n_clicks')],
    [dash.dependencies.State('popover', 'is_open')]
)
def save_popover(n_clicks, is_open):
    if n_clicks != None:
        return not is_open
    return is_open


#opening and closing the modal  
@dash_app.callback(
    dash.dependencies.Output("modal", "is_open"),
    [dash.dependencies.Input("open", "n_clicks"), 
    dash.dependencies.Input("close", "n_clicks")],
    [dash.dependencies.State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


#Reset Dropdowns
@dash_app.callback(
    dash.dependencies.Output('validate', 'value'),
    [dash.dependencies.Input('nextbutton', 'n_clicks'),
    dash.dependencies.Input('prevbutton', 'n_clicks')]
)
def reset_dropdown(nex,pre):
    if nex != None or pre != None:
        return ""


@dash_app.callback(
    dash.dependencies.Output('view', 'value'),
    [dash.dependencies.Input('nextbutton', 'n_clicks'),
    dash.dependencies.Input('prevbutton', 'n_clicks')]
)
def reset_dropdown(nex,pre):
    if nex != None or pre != None:
        return ""


@dash_app.callback(
    dash.dependencies.Output('thickness', 'value'),
    [dash.dependencies.Input('nextbutton', 'n_clicks'),
    dash.dependencies.Input('prevbutton', 'n_clicks')]
)
def reset_dropdown(nex,pre):
    if nex != None or pre != None:
        return ""


@dash_app.callback(
    dash.dependencies.Output('conditions', 'value'),
    [dash.dependencies.Input('nextbutton', 'n_clicks'),
    dash.dependencies.Input('prevbutton', 'n_clicks')]
)
def reset_dropdown(nex,pre):
    if nex != None or pre != None:
        return ""


@dash_app.callback(
    dash.dependencies.Output('severity', 'value'),
    [dash.dependencies.Input('nextbutton', 'n_clicks'),
    dash.dependencies.Input('prevbutton', 'n_clicks')]
)
def reset_dropdown(nex,pre):
    if nex != None or pre != None:
        return ""


if __name__ == '__main__':
    dash_app.run_server(debug = True )
