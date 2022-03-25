import pandas as pd
import mysql.connector
from modules.imagelist import imagelist
from modules.dbcredentials import *


#cloud_sql_mysql_create_socket
db_user = db_user
db_password = db_password
db_name = db_name
host = host #local server
port = port
cloud_sql_connection_name = cloud_sql_connection_name  #use sql connection name given on GCP when hosting on GCP
unix_socket = unix_socket


def slideimages(ncp,ncn,ncpts,ncnts,x,final_imagelist):
    conn =mysql.connector.connect(user=db_user, password=db_password, host=host, db=db_name)
    cursor = conn.cursor()

    df_db = pd.read_sql_query("SELECT * FROM rhdtest1 ",conn)
    database = []
    database_paths = []

    for index, row in df_db.iterrows():
        database.append((row['FILENAME'],' ',',',' ',row['VIEW'],' ',',',' ', row['COLOUR']))
        database.sort()
        database_paths.append(('assets/' + row['FILENAME']))
        database_paths.sort()

    
    images = imagelist("./assets/")
    final_imagelist = sorted(list((set(images) - set(database_paths))))
    
    cursor.close()
    conn.close()
    
    
    x = 0
    num_images = len(final_imagelist) 

    image_state = final_imagelist.index(final_imagelist[x])

    if ncpts == None or ncnts == None:                                  #none clicked or one clicked
        if ncp == None and ncn == None :                                                            #none clicked
            return final_imagelist[x]        
    
        if ncp != None :                                                                           
                return final_imagelist[x]

        if ncn != None :                                                                            
            if  ncn < num_images: 
                image_state = ncn 
                return final_imagelist[x + ncn]

            if ncn >= num_images - 1:
                return final_imagelist[num_images - 1]

    elif image_state >= num_images or image_state < 0 : 
        if image_state >= num_images :
            image_state = image_state - 1
        if image_state < 0 :                
            image_state = image_state + 1
    else :                                              
        if ncpts > ncnts and image_state > 0 : 
            return final_imagelist[image_state - 1]
        if ncpts > ncnts and image_state == 0 :
            return final_imagelist[image_state]
        if ncnts > ncpts and image_state < (num_images - 1):
            return final_imagelist[image_state + 1]
        if ncnts > ncpts and image_state == (num_images -1 ):
            return final_imagelist[image_state]
