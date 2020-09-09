import time
import os
threshold = 10000
def getname(pt):
    return './titles/title_' + str(pt) + '.txt'

st = time.time()
f = open("./titles/full.txt","w", encoding="utf-8")
for i in range(0,34):
    filename = "./titles/title_" + str(i) + ".txt"
    with open(filename,"r",encoding="utf-8") as fd:
        for line in fd:
            f.write((line.strip()+'\n'))
    os.remove(filename)
f.close()
print("Time for merging : " + str(time.time() - st))
total_files = 0
def split_sorted():
    file_cntr = 0
    file = open('./titles/full.txt', 'r', encoding="utf-8")
    line = file.readline()
    line2 = line.strip('\n')
    lines = []
    while line:
        lines.append(line2)
        if len(lines) % threshold == 0:
            writ = open(getname(file_cntr), 'w', encoding="utf-8")
            for l in lines:
                writ.write(l.strip() + '\n')
            file_cntr += 1
            lines = []
        line = file.readline()
        line2 =line.strip('\n')
    if len(lines) > 0:
        writ = open(getname(file_cntr), 'w', encoding="utf-8")
        for l in lines:
            writ.write(l + '\n')
        file_cntr += 1
        lines = []
    file.close()
    os.remove('./titles/full.txt')
    file.close()
    return file_cntr

total_files = split_sorted()
print("Total files after splitting : " + str(total_files))




