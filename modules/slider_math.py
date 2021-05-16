#image slider/caraousel functionality
@app.callback(
    dash.dependencies.Output('image-seen','src'),
    [dash.dependencies.Input('prevbutton','n_clicks')])
def slide_images_previous(n_clicks_prev):
	num_images = len(imagenames)
	clicksfromdefaulttofirst = 0
	if (n_clicks_prev < num_images) and (default_image - int(n_clicks_prev)) >= 0 :
		clicksfromdefaulttofirst = clicksfromdefaulttofirst + 1
		return imagenames[default_image - int(n_clicks_prev)]
	else : 
		return imagenames[clicksfromdefaulttofirst]

@app.callback(
	dash.dependencies.Output('image-seen','src'),
	[dash.dependencies.Input('nextbutton','n_clicks')])
def slide_images_next(n_clicks_next):
	num_images = len(imagenames)
	clicksfromdefaulttolast = 0
	if (n_clicks_next < num_images) and (default_image + int(n_clicks_next) <= num_images):
		clicksfromdefaulttolast = clicksfromdefaulttolast + 1
		return imagenames[default_image + int(n_clicks_next)]
	else :
		return imagenames[clicksfromdefaulttolast - 1] #one is subtracted as it is the difference between lenghth last and index last


'''This brought an error :You have already assigned a callback to the output
with ID "image-seen" and property "src". An output can only have
a single callback function. Try combining your inputs and
callback functions together into one function

'''
#So I tried to do use a single callback. 