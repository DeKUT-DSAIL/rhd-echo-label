import pandas as pd
 
def updatecsv(nex,n_clicks,validate,view,condition,severity):
    x = 0
    y = 0
    df = pd.read_csv('RHD-Data - ValidationSet.csv', encoding='utf-8')
    
    annotation = []

    for index, row in df.iterrows():
        annotation.append((row['FILENAME'], row['VIEW'], row['COLOUR']))
        annotation.sort()


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
            
