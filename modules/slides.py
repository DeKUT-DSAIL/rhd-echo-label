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


def slides(prev,next,prets,nexts,x,final_annotationlist):
    conn =mysql.connector.connect(user=db_user, password=db_password, host=host, db=db_name)
    cursor = conn.cursor()

    df = pd.read_csv('sample.csv', encoding='utf-8')
    annotation = []
    for index, row in df.iterrows():
        annotation.append((row['FILENAME'],' ',',',' ',row['VIEW'],' ',',',' ', row['COLOUR'])) 
        annotation.sort()

    df_db = pd.read_sql_query("SELECT * FROM rhdtest1 ",conn)
    database = []
    database_paths = []
    for index, row in df_db.iterrows():
        database.append((row['FILENAME'],' ',',',' ',row['VIEW'],' ',',',' ', row['COLOUR']))
        database.sort()
        database_paths.append(('assets/' + row['FILENAME']))
        database_paths.sort()
      

    final_annotationlist = sorted(list(set(annotation) - set(database)))

    images = imagelist("./assets/")
    final_imagelist = sorted(list((set(images) - set(database_paths))))
    print(final_imagelist)

    cursor.close()
    conn.close()

    x = 0
    num_annotation = len(final_annotationlist) 
    
    annotation_state = final_annotationlist.index(final_annotationlist[x])

    if prets == None or nexts == None:                                  
        if prev == None and next == None:                                                           
            return final_annotationlist[x] 
        if prev != None:
            return final_annotationlist[x]
            
        if next != None:
            if next < num_annotation:
                annotation_state = next
                return final_annotationlist[x + next]
            if next >= num_annotation - 1:
                annotation_state = num_annotation - 1
                return final_annotationlist[num_annotation - 1]
        


    if prets != None or nexts != None:
        if prev != None and next != None:
            if prev != None:
                annotation_state = next - prev
                if annotation_state >= 0 and annotation_state <= num_annotation - 1:
                    return final_annotationlist[next - prev]
                if annotation_state <= 0:
                    annotation_state = 0
                    return final_annotationlist[0]

            if next != None:
                if next < num_annotation:
                    annotation_state = next
                    if annotation_state > 0:
                        return final_annotationlist[x + next]
                if next >= num_annotation - 1:
                    annotation_state = num_annotation - 1
                    return final_annotationlist[num_annotation - 1]
    

    elif annotation_state >= num_annotation or annotation_state < 0 : #guards against the upper and lower limits.
            if annotation_state >= num_annotation :#state never should go above len of list images.
                annotation_state = annotation_state -1
            if annotation_state < 0 :                #state never goes under index zero.
                annotation_state = annotation_state + 1
    else :                                              
        if prets > nexts and annotation_state > 0 : 
            return final_annotationlist[annotation_state - 1]
        if prets > nexts and annotation_state == 0 :
            return final_annotationlist[annotation_state]
        if nexts >prets and annotation_state < (num_annotation - 1):
            return final_annotationlist[annotation_state + 1]
        if nexts >prets and annotation_state == (num_annotation -1 ):
            return final_annotationlist[annotation_state]

   
                    
 



       
            

        
    


           































# import pandas as pd

# df = pd.read_csv('C:/Users/user/Desktop/Validation-App/RHD-Data - ValidationSet.csv')

# annotation = []

# for index, row in df.iterrows():
#     annotation.append((row['FILENAME'], row['VIEW'], row['COLOUR']))
#     annotation.sort()


#     def slides(annotation):
    
#         x = 0
#         num_annotation = len(annotation)
#         state = annotation.index(annotation[x])

#         return 

#     print(slides(annotation))
    