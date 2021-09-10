
def slideannotation(ncp,ncn,ncpts,ncnts,current_annotation,annotation):
        x = 0 

        num_annotation = len(annotation)

        current_annotation = annotation[x]

        annotation_state = annotation.index(current_annotation)
       
        if ncpts == None or ncnts == None:                                  
            if ncp == None and ncn == None:                                                           
                return annotation[x] 
            if ncp != None:
                return annotation[x]
            
        if ncn != None:
            if ncn < num_annotation:
                annotation_state = ncn
                return annotation[x + ncn]
            if ncn >= num_annotation - 1:
                return annotation[num_annotation - 1]


    
        elif annotation_state >= num_annotation or annotation_state < 0 : 
            if annotation_state >= num_annotation :
                annotation_state = annotation_state -1
            if annotation_state < 0 :               
                annotation_state = annotation_state + 1
        else :                                              
            if ncpts > ncnts and annotation_state > 0 : 
                return annotation[annotation_state - 1]
            if ncpts > ncnts and annotation_state == 0 :
                return annotation[annotation_state]
            if ncnts > ncpts and annotation_state < (num_annotation - 1):
                return annotation[annotation_state + 1]
            if ncnts > ncpts and annotation_state == (num_annotation -1 ):
                return annotation[annotation_state]

