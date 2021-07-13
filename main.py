import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
#imagelist library.
from modules.imagelist import imagelist
#image slider
from modules.slideimages import slideimages
# annotation slider
from modules.slides import slides
    

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

imagenames = imagelist('./assets/static/images')

df = pd.read_csv('RHD-Data - ValidationSet.csv', encoding='utf-8')

annotation = []

for index, row in df.iterrows():
    annotation.append((row['FILENAME'], row['VIEW'], row['COLOUR']))
    annotation.sort()


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
                                                                        #multi = True,
                                                                        style={'height': '30px', 'width': '800px', 'textAlign' : "middle"}),
                                                            
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
                                     
                                    
                                    html.Div([dash_table.DataTable(
                                                id ='table')])

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



#Update the datatable
@dash_app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('save', 'n_clicks')],
    [dash.dependencies.Input('validate', 'value'),
    dash.dependencies.Input('view', 'value'),
    dash.dependencies.Input('conditions', 'value'),
    dash.dependencies.Input('severity', 'value')],
    [dash.dependencies.State('nextbutton','n_clicks')],
    prevent_initial_call = True
)
def update_table(n_clicks,validate,view,condition,severity,nex):
    y = 0
    df = pd.read_csv('RHD-Data - ValidationSet.csv', encoding='utf-8')

    if nex == None:
        x = 0
        if n_clicks != None:
            dff = pd.DataFrame({"FILENAME": annotation[x][y] ,"VIEW": annotation[x][y+1], "COLOUR": annotation[x][y+2], "VALIDATE": validate, "VIEW_OF_ECHO": view, "CONDITIONS": condition, "SEVERITY": severity}, index=[x])
            
            dff.to_csv('Data.csv', encoding='utf-8',mode='a', index=False, columns=['FILENAME', 'VIEW', 'COLOUR', 'VALIDATE', 'VIEW_OF_ECHO', 'CONDITIONS','SEVERITY'] )
        

    elif nex != None:
        if n_clicks == nex + 1:
            x = nex
            dff = pd.DataFrame({"FILENAME": annotation[x][y] , "VIEW": annotation[x][y+1], "COLOUR": annotation[x][y+2], "VALIDATE": validate, "VIEW_OF_ECHO": view, "CONDITIONS": condition, "SEVERITY": severity}, index=[x])
            
            dff.to_csv('Data.csv', encoding='utf-8', mode='a', header=False, index=False, columns=['FILENAME', 'VIEW', 'COLOUR', 'VALIDATE', 'VIEW_OF_ECHO', 'CONDITIONS','SEVERITY'] )
            


#Reset Dropdown
@dash_app.callback(
    dash.dependencies.Output('validate', 'value'),
    [dash.dependencies.Input('nextbutton', 'n_clicks'),
    dash.dependencies.Input('prevbutton', 'n_clicks')],
    prevent_initial_call = True
)
def reset_dropdown(nex,pre):
    if nex != None or pre != None:
        return ""

@dash_app.callback(
    dash.dependencies.Output('view', 'value'),
    [dash.dependencies.Input('nextbutton', 'n_clicks'),
    dash.dependencies.Input('prevbutton', 'n_clicks')],
    prevent_initial_call = True
)
def reset_dropdown(nex,pre):
    if nex != None or pre != None:
        return ""

@dash_app.callback(
    dash.dependencies.Output('conditions', 'value'),
    [dash.dependencies.Input('nextbutton', 'n_clicks'),
    dash.dependencies.Input('prevbutton', 'n_clicks')],
    prevent_initial_call = True
)
def reset_dropdown(nex,pre):
    if nex != None or pre != None:
        return ""

@dash_app.callback(
    dash.dependencies.Output('severity', 'value'),
    [dash.dependencies.Input('nextbutton', 'n_clicks'),
    dash.dependencies.Input('prevbutton', 'n_clicks')],
    prevent_initial_call = True
)
def reset_dropdown(nex,pre):
    if nex != None or pre != None:
        return ""


if __name__ == '__main__':
    dash_app.run_server(debug = True)