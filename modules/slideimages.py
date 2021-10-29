
def slideimages(ncp,ncn,ncpts,ncnts,current_image_path,final_imagelist):
        x = 0 

        num_images = len(final_imagelist) 
    
        image_state = final_imagelist.index(current_image_path)

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
