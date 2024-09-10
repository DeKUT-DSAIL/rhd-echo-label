import google.cloud.storage
from google.cloud import storage
import os
import sys

#get the list of images from google cloud storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'rhd-imaging-325212-89c18efb8640.json' #the json key is generated from the IAM service account

storage_client = storage.Client()

def cloud_data(bucket_name):
    #create an empty list
    imageslist = []
    """Lists all the blobs in the bucket."""
    #bucket_name = "rhd_imaging_data"

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        imageslist.append('https://storage.googleapis.com/'+ bucket_name + '/' + blob.name)
        #print(blob.name)

    return imageslist

