# RHD-Quality_Control_Check_App
This web application will be used to validate the current annotation we have of the Rheumatic Heart Disease data provided by Dr. Liesl Zuhlke.

## RHD Data
The data we got originally was in the form of images and videos of echocardiograms. We needed to annotate this data train a model using machine learning algorithms.

As a first step in this project, we will concentrate on the view of the heart as parasternal long axis view(PLAX) or not. We will also concentrate on whether the images and videos of the echocardiograms have colour or not. The idea of having a colour classifier is to help identify leaking heart valves.
The web Application will be used by experts of echocardiograms to validate our annotation.

## Web Application Deployment
This web app is developed using [Dash](https://dash.plotly.com/) and has been deployed here: [Quality Control Check](https://rhd-quality-control.uw.r.appspot.com/).

  #Steps taken to deploy the app
  
  I followed steps outlined a [blog post](https://www.phillipsj.net/posts/deploying-dash-to-google-app-engine/) by [Jamie Phillips](https://www.phillipsj.net/)
  
  1. Create a virtual environment and activate it.
  2. Install requirements that are in the requirements.txt file.
  3. Run py file: main.py (The default behaviour of Google App engine is to assume the entrypoint is located in a file called main.py) 
  4. Create a app.yaml configure it.
  5. Run "gcloud app deploy" on the Google Cloud SDK tool.



