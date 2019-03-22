import os
import string
import sys
dirName = sys.path[0].replace("111.py", '')   
currentPath = dirName + '/JPEGImages/'
fileDir=os.listdir(currentPath)
print(fileDir)
wanZhengDir = []
for picList in fileDir:
    wanZhengDir.append(currentPath  + picList + '/') 
for filename1 in wanZhengDir:
    filename2 = os.listdir(filename1)
    for filename in filename2:
        newname = filename
        newname = newname.split(".")
        if newname[-1] =="bmp" or newname[-1] =="jpeg" :
            newname[-1]="jpg"
            newname = str.join(".",newname)  
            filename = filename1+filename
            newname = filename1+newname
            os.rename(filename,newname)
            print(newname,"updated successfully")