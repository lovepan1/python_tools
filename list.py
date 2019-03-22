import os
import sys
pwd = sys.path[0]
print pwd
exts = [".png", ".PNG", ".jpg", ".JPG"]
f = open("train.txt", "w")
for root, dirs, files in os.walk(pwd):
	for file in files:
		for ext in exts:
			if (file.find(ext) != -1):
				f.write(os.path.abspath(root+"/"+file))
				f.write("\n")
				break
f.close()
