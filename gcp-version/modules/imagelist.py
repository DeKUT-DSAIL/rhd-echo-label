#Prep imagenames list libraries
import os
import pathlib

#Takes a path returns a list of files.
def imagelist(path) :
    #define path
    path = pathlib.Path(path)
    #string path to be appended as part of image #relative path.
    pathstr = str(path)
    #create empty list
    imageslist = [] 

    #create list of images in path given
    with os.scandir(path) as listOfEntries:
        for entry in listOfEntries:
            #print all entries that are files.
            if entry.is_file():
                imageslist.append(pathstr + "/" + entry.name)
                #print(entry.name)
    #sort list alphanumerically
    imageslist.sort()
    #print(imageslist)
    return imageslist
