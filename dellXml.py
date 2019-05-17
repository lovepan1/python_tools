import os
dir = os.getcwd()
img_dir = dir + '/JPEGImages/'
anno_dir = dir + '/Annotations/'
img_list = os.listdir(img_dir)
xml_list = os.listdir(anno_dir)
a = open('error2.sh', 'w')
for xml in xml_list:
#    for
#    print(img)
#    print(xml.replace('xml', 'jpg'))
    if xml.replace('xml', 'jpg') not in img_list:
        line = 'rm ' + anno_dir + xml + '\n'
        a.write(line)
        print(xml)
a.close()