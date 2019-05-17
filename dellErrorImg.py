import os
f = open('annotations.csv', 'r')
b = open('error.sh', 'w')
a = open('new_anno.csv', 'w')
for line in f:
    list = line.split(',')
#    print(line)
    print('ok')
    if list[2] == list[4] or list[1] == list[3]:
        print(list[0])
        b.write('rm ' + str(list[0]) + '\n')
        b.write('rm ' + str(list[0].replace('JPEGImages', 'Annotations').replace('jpg', 'xml')) + '\n')
    else:
        a.write(line)
f.close()
b.close()
a.close()
