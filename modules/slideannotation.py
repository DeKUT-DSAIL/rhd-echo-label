
def slideannotation(ncp,ncn,ncpts,ncnts,current_annotation,final):
        x = 0 

        num_annotation = len(final)

        annotation_state = final.index(current_annotation)
       
        if ncpts == None or ncnts == None:                                  
            if ncp == None and ncn == None:                                                           
                return final[x] 

            if ncp != None:
                    return final[x]
            
            if ncn != None:
                if ncn < num_annotation:
                    annotation_state = ncn
                    return final[x + ncn]
                    
            if ncp != None:
                if ncn >= num_annotation - 1:
                    return final[num_annotation - 2]
    
        elif annotation_state >= num_annotation or annotation_state < 0 : 
            if annotation_state >= num_annotation :
                annotation_state = annotation_state - 1
            if annotation_state < 0 :               
                annotation_state = annotation_state + 1
        else :                                              
            if ncpts > ncnts and annotation_state > 0 : 
                return final[annotation_state - 1]
            if ncpts > ncnts and annotation_state == 0 :
                return final[annotation_state]
            if ncnts > ncpts and annotation_state < (num_annotation - 1):
                return final[annotation_state + 1]
            if ncnts > ncpts and annotation_state == (num_annotation -1 ):
                return final[annotation_state]
