#!/usr/bin/python
import cv2
import os
w = cv2.VideoWriter("out.avi", cv2.VideoWriter_fourcc(*'XVID'), 20, (1920,1080))
for root,fods,files in os.walk("."):
	for file in files:
		img=cv2.imread(root+"/"+file)
		w.write(img)
w.close()
	

