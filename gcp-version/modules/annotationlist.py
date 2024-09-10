import os
import pathlib

def filelist(path) :
    #define path
    path = pathlib.Path(path)
    #string path to be appended as part of image #relative path.
    pathstr = str(path)
    #create empty list
    fileslist = [] 

    #create list of images in path given
    with os.scandir(path) as listOfEntries:
        for entry in listOfEntries:
            #print all entries that are files.
            if entry.is_file():
                fileslist.append(entry.name)
                #print(entry.name)
    #sort list alphanumerically
    fileslist.sort()
    #print(fileslist)
    return fileslist