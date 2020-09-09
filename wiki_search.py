import re
import bisect
from nltk.corpus import stopwords
from Stemmer import Stemmer
import math
import sys
import time

stop_words = set(stopwords.words('english'))
threshold = 10000
def tokenize(text):
    text = text.lower()
    word_tokens = reg1.findall(text)
    filtered = [(ps.stemWord(w)) for w in word_tokens if (w != "" and w not in stop_words and len(w)>1)]
    return filtered

def count(stri, ch):
    if ch not in stri:
        return 0
    part = stri.split(ch)[1]
    cnt = re.split(r'[^0-9]+', part)[0]
    return int(cnt)
def get_title(doc_no):

    doc_no = int(doc_no)
    off = doc_no // threshold
    rem = doc_no%threshold
    if(rem==0):
        off = off-1
        file = open("./titles/title_" + str(off) + '.txt', "r", encoding="utf-8")
        lines = file.readlines()
        return lines[(len(lines)-1)]
    else:
        file = open("./titles/title_" + str(off) + '.txt', "r", encoding="utf-8")
        lines = file.readlines()
        return lines[rem-1]


file = open('./index/secondary.txt', 'r')
secondary_words = file.readlines()
file.close()
total_docs = 9829059
reg1 = re.compile('[A-Za-z0-9]+')
ps = Stemmer("porter")

#print("====Press Q/q to exit====")
fd = open(sys.argv[1])
for query in fd:
    k = query.split(",")[0].strip()
    k = int(k)
    query = query.split(",")[1].strip()
    if(query== "Q" or query == "q"):
        break
    if(":" not in query):
        st = time.time()
        value = {}
        tokens = tokenize(query)
        for token in tokens:
            posting_list = ""
            ind = bisect.bisect_right(secondary_words, token) - 1
            if(ind==-1):
                continue
            else:
                f = open("./index/index_" + str(ind) + '.txt', "r")
                for line in f:
                    key = line.split(":")[0]
                    if(key == token):
                        posting_list = line.split(":")[1].strip()
                        f.close()
                        break
            if(posting_list != ""):
                all_docs = re.findall("d[^d]*",posting_list)
                idf = total_docs/len(all_docs)
                for doc in all_docs:
                    num = ""
                    for ch in doc:
                        if(ch=='d'):
                            continue
                        elif(ch>='0' and ch<='9'):
                            num+=ch
                        else:
                            break

                    cnt1 = count(doc,'t')*idf
                    cnt2 = count(doc,'b')*idf
                    cnt3 = count(doc,'c')*idf
                    cnt4 = count(doc,'i')*idf
                    cnt5 = count(doc,'r')*idf
                    cnt6 = count(doc,'e')*idf
                    if(num in value):
                        value[num]+=(200*cnt1 + 100*cnt3 + 150*cnt4 +  5*cnt2 + 5*cnt5 + 5*cnt6)
                    else:
                        value[num]=(200*cnt1 + 100*cnt3 + 150*cnt4 +  5*cnt2 + 5*cnt5 + 5*cnt6)
        results = sorted(value.items(), key=lambda x: x[1], reverse = True)
        cntt=0
        for result in results:
            cntt+=1
            if(cntt<=k):
                print(result[0],end="")
                print(", ", end="")
                print(get_title(result[0]),end="")
            else:
                break
        vv = time.time()-st
        print(vv, end="")
        print(", ", end="")
        print(vv/k)
        print()
       # print(time.time()-st)
    else:
        value = {}
        data = re.sub('([tbcire]:)',r'tag\1 ', query)
        data = re.split('tag', data)
        st = time.time()
        for field in data:
            if(field):
                tokens = field.split(":")
                f_type  = tokens[0].strip()
                words_to_check = tokens[1].strip().split()
                for word in words_to_check:
                    posting_list = ""
                    ind = bisect.bisect_right(secondary_words, word) - 1
                    if(ind==-1):
                        continue
                    else:
                        f = open("./index/index_" + str(ind) + '.txt', "r")
                        for line in f:
                            key = line.split(":")[0]
                            if(key == word):
                                posting_list = line.split(":")[1].strip()
                                f.close()
                                break
                    if(posting_list !=""):
                        all_docs = re.findall("d[^d]*",posting_list)
                        idf = total_docs/len(all_docs)
                        for doc in all_docs:
                            num = ""
                            for ch in doc:
                                if(ch=='d'):
                                    continue
                                elif(ch>='0' and ch<='9'):
                                    num+=ch
                                else:
                                    break 
                            cnt1 = count(doc,'t')*idf
                            cnt2 = count(doc,'b')*idf
                            cnt3 = count(doc,'c')*idf
                            cnt4 = count(doc,'i')*idf
                            cnt5 = count(doc,'r')*idf
                            cnt6 = count(doc,'e')*idf
                            if(num in value):
                                value[num]+=(200*cnt1 + 100*cnt3 + 150*cnt4 +  5*cnt2 + 5*cnt5 + 5*cnt6)
                            else:
                                value[num]=(200*cnt1 + 100*cnt3 + 150*cnt4 +  5*cnt2 + 5*cnt5 + 5*cnt6)
                            if(f_type in doc):
                                value[num] +=(1000000000)
        
        results = sorted(value.items(), key=lambda x: x[1], reverse = True)
        cntt = 0
        for result in results:
            cntt+=1
            if(cntt<=k):
                print(result[0],end="")
                print(", ",end="")
                print(get_title(result[0]),end="")
            else:
                break
        vv = time.time()-st
        print(vv, end="")
        print(", ", end="")
        print(vv/k)
        print()


                            






