#Initial variables had too many letters.(to simplify I created a key/legend) #a word legend
    #Keys : Value #ncp = n_clicks_of_prev #ncn = n_clicks_of_next #ncpts = n_clicks_timestamp_of_prev #ncnts = n_clicks_timestamp_of_next
#takes above varialbles in order, and current_image_path and imagesnames returns next image name.
def slideimages(ncp,ncn,ncpts,ncnts,current_image_path,imagenames):
        x = 0 #the default image, my code has been built around the default being 0.#esp in single click.
        y = 0 #default1 when both clicked. #used when next_time_greater thanprev_timestamp
        z = 0 #default2 when both clicked. #used when prev_time_greater than next_timestamp

        num_images = len(imagenames) 
    
        image_state = imagenames.index(current_image_path)
        #when only one has been pressed.

        if ncpts == None or ncnts == None:                                  #none clicked or one clicked
            if ncp == None and ncn == None :                                                            #none clicked
                return imagenames[x] #default image.
                #image state no change.           
        
            if ncp != None :                                                                            #only prev clicked
                    return imagenames[x]

            if ncn != None :                                                                            #only next clicked. 
                if  ncn < num_images: #only next has been clicked till last image.
                    image_state = ncn #not updating image_state #will try using pointers and addressing.
                    return imagenames[x + ncn]

                if ncn >= num_images - 1:#clicked till last image 
                    return imagenames[num_images - 1]
    
        elif image_state >= num_images or image_state < 0 : #guards against the upper and lower limits.
            if image_state >= num_images :#state never should go above len of list images.
                image_state = image_state -1
            if image_state < 0 :                #state never goes under index zero.
                image_state = image_state + 1
        else :                                              
            if ncpts > ncnts and image_state > 0 : 
                return imagenames[image_state - 1]
            if ncpts > ncnts and image_state == 0 :
                return imagenames[image_state]
            if ncnts > ncpts and image_state < (num_images - 1):
                return imagenames[image_state + 1]
            if ncnts > ncpts and image_state == (num_images -1 ):
                return imagenames[image_state]
#Timestamps used to determine between prev and next, which was clicked first.
    #print('Timestamp prev button: ',ncpts, '\nType : ',type(ncpts)) 
    #print('Timestamp next button : ',ncnts, '\nType : ',type(ncnts))
    #print('ncn : ',ncn)
    #print('ncp : ',ncp)
    #print("Current image : ",current_image_path)
    #print("Current image length : ",len(current_image_path))
    #print("Image index : ",imagenames.index(current_image_path))
    
