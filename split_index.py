import time
import os
threshold = 10000
def getname(pt):
    return './index/index_' + str(pt) + '.txt'

def merge_2_files(pt1, pt2):
    if pt1 == pt2:
        return
    filename1 = "./index/index_" + str(pt1) + ".txt"
    filename2 = "./index/index_" + str(pt2) + ".txt"
    f1 = open(filename1, 'r')
    f2 = open(filename2, 'r')
    f3 = open('./index/temp.txt', 'w')
    l1 = f1.readline().strip('\n')
    l2 = f2.readline().strip('\n')
    while (l1 and l2):
        word1 = l1.split(":")[0]
        word2 = l2.split(":")[0]
        if word1 < word2:
            f3.write(l1 + '\n')
            l1 = f1.readline().strip('\n')
        elif word2 < word1:
            f3.write(l2 + '\n')
            l2 = f2.readline().strip('\n')
        else:
            list1 = l1.strip().split(":")[1]
            list2 = l2.strip().split(':')[1]
            f3.write(word1 + ':' + list1 + list2 + '\n')
            l1 = f1.readline().strip('\n')
            l2 = f2.readline().strip('\n')
    while l1:
        f3.write(l1 + '\n')
        l1 = f1.readline().strip('\n')
    while l2:
        f3.write(l2 + '\n')
        l2 = f2.readline().strip('\n')
    f1.close()
    f2.close()
    f3.close()
    os.remove(filename1)
    os.remove(filename2)
    num = pt1//2
    os.rename('./index/temp.txt', "./index/index_"+ str(num) + ".txt")
st = time.time()
r = 34
print("Total files : " + str(r))

while r != 1:
    for i in range(0, r, 2):
        if i + 1 == r:
            new_name = i // 2
            os.rename(getname(i), getname(i // 2))
            break
        merge_2_files(i, i+1)
    if r % 2 == 1:
        r = r // 2 + 1
    else:
        r = r // 2
    print("Number of files left: " + str(r))

print("Time for merging : " + str(time.time() - st))
total_files = 0
def split_sorted():
    file_cntr = 0
    os.rename(getname(0), './index/full.txt')
    file = open('./index/full.txt', 'r')
    sec = open('./index/secondary.txt', 'w')
    line = file.readline().strip('\n')
    lines = []
    while line:
        lines.append(line)
        if len(lines) % threshold == 0:
            writ = open(getname(file_cntr), 'w')
            sec.write(lines[0].split(":")[0] + '\n')
            for l in lines:
                writ.write(l + '\n')
            file_cntr += 1
            lines = []
        line = file.readline().strip('\n')
    if len(lines) > 0:
        writ = open(getname(file_cntr), 'w')
        sec.write(lines[0].split(":")[0] + '\n')
        for l in lines:
            writ.write(l + '\n')
        file_cntr += 1
        lines = []
    file.close()
    os.remove('./index/full.txt')
    file.close()
    sec.close()
    return file_cntr

total_files = split_sorted()
print("Total files after splitting : " + str(total_files))






