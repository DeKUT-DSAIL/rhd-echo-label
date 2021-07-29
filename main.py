import dash
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies
import pandas as pd
from modules.imagelist import imagelist
from modules.slideimages import slideimages
from modules.slides import slides
from time import strftime
import mysql
from mysql.connector import errorcode


    

# external CSS stylesheets
external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                        "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                        "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]

dash_app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app = dash_app.server

dash_app.title = "RHD Annotation Quality Control Check"

list_of_validation = ['Correct', 'NOT CORRECT']

list_of_views = ['Parasternal long axis (PLAX)','Parasternal short axis(PSAX)','Apical Four Chamber(A4C)','Apical three chamber (A3C)','Apical two chamber(A2C)','Suprasternal(SSN)','Subcostal']

list_of_conditions = ['Mitral Valve Regurgitation','Aortic Valve Regurgitation','Tricuspid Valve Regurgitation','Pulmonary Valve Regurgitation','Aortic Valve Stenosis','Mitral Valve Stenosis','Tricuspid Valve Stenosis','Pulmonary Valve Stenosis','Mitral Valve Prolapse','Not Applicable']

list_of_severities = ['Normal','Borderline rhd','Definite rhd','Not Applicable']

x = 0 
y = 0

imagenames = imagelist('./assets/static/images')

df = pd.read_csv('RHD-Data - ValidationSet.csv', encoding='utf-8')

annotation = []

for index, row in df.iterrows():
    annotation.append((row['FILENAME'],' ',',',' ',row['VIEW'],' ',',',' ', row['COLOUR']))

db_user = "CLOUD_SQL_USERNAME"
db_password = "CLOUD_SQL_PASSWORD"
db_name = "CLOUD_SQL_DATABASE_NAME"
db_connection_name = "CLOUD_SQL_CONNECTION_NAME"
unix_socket = "/cloudsql/{}".format(db_connection_name)



host = '127.0.0.1'
conn = mysql.connector.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)

cursor = conn.cursor()

#connect to database
def create_connection(conn):
    try:
        
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
TABLES['testing2'] = (
    "CREATE TABLE `testing2`("
    " `FILENAME` varchar(255) NOT NULL,"
    " `VIEW` varchar(255) NOT NULL,"
    " `COLOUR` varchar(255) NOT NULL,"
    " `VALIDATE` varchar(255) NOT NULL,"
    " `VIEW_OF_ECHO` varchar(255) NOT NULL,"
    " `CONDITIONS` varchar(255) NOT NULL,"
    " `SEVERITY` varchar(255) NOT NULL,"
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
 html.Div(style = {'textAlign' : 'center'},
                        children = [
                                    html.Div(html.Img(id = 'image-seen',src = imagenames[x],width = '700px',height = '500px')),

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
                                        html.Button('Save', id = 'save', style = {'color' : 'red'},autoFocus = True),
                                        html.Div(id = 'thesaved'),

                                        html.P(),
                                        html.P(children = [ html.Div(id = 'prevend'),html.Button('Prev',id = 'prevbutton'),
                                        html.Button('Next', id = 'nextbutton'),html.Div(id = 'nextend')],),
                                        
                                        html.Div(id = 'dropdown', children = []),
                                        
                                                        ])
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

#Update and connect to database
@dash_app.callback(
    dash.dependencies.Output('dropdown','children'),
    [dash.dependencies.Input('validate', 'value'),
    dash.dependencies.Input('view', 'value'),
    dash.dependencies.Input('conditions', 'value'),
    dash.dependencies.Input('severity', 'value'),
    dash.dependencies.Input('save', 'n_clicks')],
    [dash.dependencies.State('save', 'n_clicks_timestamp'),
    dash.dependencies.State('nextbutton', 'n_clicks')]
)


def update_output_data(validate,view,conditions,severity,n_clicks,timestamp,nex):
    y = 0
    if nex == None:
        x = 0
        if n_clicks != None:
            conn = mysql.connector.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
            cursor = conn.cursor()
            timestamp = strftime("%Y-%m-%d %H:%M:%S")
            add_annotation = """INSERT INTO testing2 
            (FILENAME, VIEW, COLOUR,VALIDATE,VIEW_OF_ECHO,CONDITIONS,SEVERITY,TIMETAKEN)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""

            values = ((annotation[x][y]), (annotation[x][y+4]), (annotation[x][y+8]), validate, view, str((conditions)), severity, timestamp)

            try:
                cursor.execute(add_annotation,values)
                print("Data annotated successfully.")
                conn.commit()
            except:
                conn.rollback()

            cursor.close()
            conn.close()

    elif nex != None:
        if n_clicks == nex + 1:
            x = nex

            conn = mysql.connector.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
            cursor = conn.cursor()
            timestamp = strftime("%Y-%m-%d %H:%M:%S")
            add_annotation = """INSERT INTO testing2 
            (FILENAME, VIEW, COLOUR,VALIDATE,VIEW_OF_ECHO,CONDITIONS,SEVERITY,TIMETAKEN)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""

            values = ((annotation[x][y]), (annotation[x][y+4]), (annotation[x][y+8]), validate, view, str((conditions)), severity, timestamp)

            try:
                cursor.execute(add_annotation,values)
                print("Data annotated successfully.")
                conn.commit()
            except:
                conn.rollback()

            cursor.close()
            conn.close()


    

#Reset Dropdown
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
