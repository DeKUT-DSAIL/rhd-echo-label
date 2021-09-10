
app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.Section(id="slideshow",children=[
        html.Div(id="slideshow-container",children=[
            html.Div(id="image"),
            dcc.Interval(id='interval',interval=3000)
        ])
    ])
])

@app.callback(Output('image','children'),
    [Input('interval','n_intervals')])
def display_image(n):
    if n == None or n % 3 == 1:
        img = html.Img(src="static/images/blank.png")
    elif n % 3 == 2 :
        img = html.Img(src="static/images/blank1.png")
    elif n % 3 == 0 :
        img = html.Img(src="static/images/blank2.png")
    else :
        img = "None"
    return img
