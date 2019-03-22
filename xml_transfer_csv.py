import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import sys

def xml_to_csv(path):
    xml_list = []
    num4 = 0
    num2 = 0
    for xml_file in glob.glob(path + '*.xml'):
        tree = ET.parse(xml_file)
        #print(xml_file)
        root = tree.getroot()
        #print(root.findall('bndbox'))
        for member in root.findall('object'):
#             print(member[0])
#             print(member[1])
#             print(member[2])
#             print(member[3])
#             print(member[4])
            if len(member) != 5:
                #print(xml_file) 
                num2 += 1
                value = (root.find('filename').text,
                         int(root.find('size')[0].text),
                         int(root.find('size')[1].text),
                         member[0].text,
                         int(member[1][0].text),
                         int(member[1][1].text),
                         int(member[1][2].text),
                         int(member[1][3].text)
                         )
#                 continue
# path + '/' + 
            else:
                value = (root.find('filename').text,
                         int(root.find('size')[0].text),
                         int(root.find('size')[1].text),
                         member[0].text,
                         int(member[4][0].text),
                         int(member[4][1].text),
                         int(member[4][2].text),
                         int(member[4][3].text)
                         )
                num4 += 1
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    print(xml_df)
    print('illegal xml object num is %d' %num2)
    print('legal   xml object num is %d' %num4)
    return xml_df


def main():
    #image_path = os.path.join(os.getcwd(), 'annotations')
    #image_path = sys.argv[1]
    #image_path = os.getcwd() + '/data/train/'
    image_path = os.getcwd() + '/data/test/'
#     image_path = 'data/train/'
    #output_path = sys.argv[0].replace('xml_transfer_csv.py', '')
    output_path = os.getcwd()
#     print(image_path)
    print(output_path)
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv(output_path + '/dianli_test.csv', index=None)
    print('Successfully converted xml to csv.')


main()