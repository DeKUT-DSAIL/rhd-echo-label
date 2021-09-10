def slides(pre,nex,prets,nexts,x,annotation):
    x = 0
    num_annotation = len(annotation) 
        
    annotation_state = annotation.index(annotation[x])
    

    if prets == None or nexts == None:                                  
        if pre == None and nex == None:                                                           
            return annotation[x] 
        if pre != None:
            return annotation[x]
            
        if nex != None:
            if nex < num_annotation:
                annotation_state = nex
                return annotation[x + nex]
            if nex >= num_annotation - 1:
                annotation_state = num_annotation - 1
                return annotation[num_annotation - 1]
        


    if prets != None or nexts != None:
        if pre != None and nex != None:
            if pre != None:
                annotation_state = nex - pre
                if annotation_state >= 0 and annotation_state <= num_annotation - 1:
                    return annotation[nex - pre]
                if annotation_state <= 0:
                    annotation_state = 0
                    return annotation[0]

            if nex != None:
                if nex < num_annotation:
                    annotation_state = nex
                    if annotation_state > 0:
                        return annotation[x + nex]
                if nex >= num_annotation - 1:
                    annotation_state = num_annotation - 1
                    return annotation[num_annotation - 1]

    elif annotation_state >= num_annotation or annotation_state < 0 : #guards against the upper and lower limits.
            if annotation_state >= num_annotation :#state never should go above len of list images.
                annotation_state = annotation_state -1
            if annotation_state < 0 :                #state never goes under index zero.
                annotation_state = annotation_state + 1
    else :                                              
        if prets > nexts and annotation_state > 0 : 
            return annotation[annotation_state - 1]
        if prets > nexts and annotation_state == 0 :
            return annotation[annotation_state]
        if nexts >prets and annotation_state < (num_annotation - 1):
            return annotation[annotation_state + 1]
        if nexts >prets and annotation_state == (num_annotation -1 ):
            return annotation[annotation_state]

   
                    
 



       
            

        
    


           































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
    