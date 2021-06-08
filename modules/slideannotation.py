#Initial variables had too many letters.(to simplify I created a key/legend) #a word legend
    #Keys : Value #ncp = n_clicks_of_prev #ncn = n_clicks_of_next #ncpts = n_clicks_timestamp_of_prev #ncnts = n_clicks_timestamp_of_next
#takes above varialbles in order, and current_image_path and imagesnames returns next image name.
def slideannotation(ncp,ncn,ncpts,ncnts,currentann,annotation):
        x = 0 #the default image, my code has been built around the default being 0.#esp in single click.
        y = 0 #default1 when both clicked. #used when next_time_greater thanprev_timestamp
        z = 0 #default2 when both clicked. #used when prev_time_greater than next_timestamp

        num_annotation = len(annotation) 
    
        annotation_state = annotation.index(annotation[x])
        #when only one has been pressed.

        if ncpts == None or ncnts == None:                                  #none clicked or one clicked
            if ncp == None and ncn == None :                                                            #none clicked
                return annotation[x] #default image.
                #image state no change.           
        
            if ncp != None :         
                if  ncn > num_annotation: #only next has been clicked till last image.
                    annotation_state = ncp                                                                   #only prev clicked
                    return annotation[x - ncp]

            if ncn != None :                                                                            #only next clicked. 
                if  ncn < num_annotation: #only next has been clicked till last image.
                    annotation_state = ncn #not updating annotation_state #will try using pointers and addressing.
                    return annotation[x + ncn]

                if ncn >= num_annotation - 1:#clicked till last image 
                    return annotation[num_annotation - 1]
    
        elif annotation_state >= num_annotation or annotation_state < 0 : #guards against the upper and lower limits.
            if annotation_state >= num_annotation :#state never should go above len of list images.
                annotation_state = annotation_state -1
            if annotation_state < 0 :                #state never goes under index zero.
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
#Timestamps used to determine between prev and next, which was clicked first.
    #print('Timestamp prev button: ',ncpts, '\nType : ',type(ncpts)) 
    #print('Timestamp next button : ',ncnts, '\nType : ',type(ncnts))
    #print('ncn : ',ncn)
    #print('ncp : ',ncp)
    #print("Current image : ",current_image_path)
    #print("Current image length : ",len(current_image_path))
    #print("Image index : ",annotation.index(current_image_path))
    
