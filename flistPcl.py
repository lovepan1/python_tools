#!/usr/bin/python
#create list *png *xml
import os
import sys
import random
if len(sys.argv) <= 1:
    pwd = sys.path[0]
else:
    pwd = sys.argv[1]
print pwd
pwdList = pwd.split('/')
listLen = len(pwdList) 
print listLen
exts = [".png", ".PNG", ".jpg", ".JPG"]
f = open(pwd+"/list.txt", "w")
str = []
for root, dirs, files in os.walk(pwd):
    dir = root.split('/')[-1]
    print dir
    for file in files:
        for ext in exts:
            if (file.find(ext) != -1):
                xml = file.replace(ext, ".xml")
                if (os.path.exists(root+"/"+xml)):
                    source1 = os.path.join(root,file)
                    source = source1.split('/')
                    for i in range(0, listLen):
                        del source[0]
                    rightSource = ''
                    rightSource1 = ''
                    for i in source:
                        rightSource += i
			rightSource += '/'  
                    rightSource1 = rightSource[:-1]
                    print rightSource1
                    source2 = rightSource1.replace(ext, ".xml")
                    print rightSource1
                    str.append(rightSource1+" "+source2 + "\n")
                break
random.shuffle(str)
for s in str:
	f.write(s)
f.close()
