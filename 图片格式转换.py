import os
import string
dirName = "/home/pcl/darknet/VOCdevkit/VOC2007/JPEGImages/"         
li=os.listdir(dirName)
for filename in li:
    newname = filename
    newname = newname.split(".")
    if newname[-1] !="bmp":
        newname[-1]="jpg"
        newname = str.join(".",newname)  
        filename = dirName+filename
        newname = dirName+newname
        os.rename(filename,newname)
        print(newname,"updated successfully")