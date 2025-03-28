# RHD-imaging-App
This web application will be used to label the Rheumatic Heart Disease data provided by Dr. Liesl Zuhlke.

## RHD Data
The data we got originally was in the form of images and videos of echocardiograms. We needed to annotate this data train a model using machine learning algorithms.

As a first step in this project, we will concentrate on the view of the heart as parasternal long axis view(PLAX) or not. We will also concentrate on whether the images and videos of the echocardiograms have colour or not. The idea of having a colour classifier is to help identify leaking heart valves.
The web Application will be used by experts of echocardiograms to validate our annotation.

![Screenshot (298)](https://user-images.githubusercontent.com/74656615/133057040-c2cfd21a-7ac7-429d-94ee-edab3845c9c2.png)

## Web Application Deployment
This web app is developed using [Dash](https://dash.plotly.com/) and has been deployed here: [RHD imaging Web app](https://rhd-imaging-325212.uw.r.appspot.com/).

  # Steps taken to deploy the app on GCP
  
  I followed steps outlined a [blog post](https://www.phillipsj.net/posts/deploying-dash-to-google-app-engine/) by [Jamie Phillips](https://www.phillipsj.net/)
  
  1. Create a virtual environment and activate it.
              
         python -m venv rhd-env
  2. Install requirements that are in the requirements.txt file.
         
         pip install -r requirements.txt
  3. Create a app.yaml configure it.
  
  5. Download and install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install). 
     From the Google Cloud SDK terminal change into the directory where you have saved your main.py, requirements.txt and app.yaml files. 
     
     (The default behaviour of Google App engine is to assume the entrypoint is located in a file called main.py).
     
     Enter y if prompted for a y/n response.
          
          gcloud app deploy --promote
     




