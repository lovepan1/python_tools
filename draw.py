import xml.etree.ElementTree as ET
import cv2
import os
for root,dirs,files in os.walk("."):
	if (root.find("baiShi") == -1):
		continue
	for file in files:
		if (file.find(".png") != -1):
			f = root+"/"+file
			img = cv2.imread(f)
			xml = f.replace(".png", ".xml")
			ifile = open(xml)
			tree = ET.parse(ifile)
                        r = tree.getroot()
                        for obj in r.iter('object'):
                                cls = obj.find('name').text
				xmlbox = obj.find('bndbox')
				xmin = int(xmlbox.find('xmin').text)
				xmax = int(xmlbox.find('xmax').text)
				ymin = int(xmlbox.find('ymin').text)
				ymax = int(xmlbox.find('ymax').text)
				cv2.rectangle(img, (xmin, ymin), (xmax,ymax), (255,255,255))
				cv2.putText(img, cls, (xmin, ymin), 0, 1, (0,0,0),1,8)
			cv2.imshow("1",img)
			cv2.waitKey()
#			break;
	else:
		continue
#	break
