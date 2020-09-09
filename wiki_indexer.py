import xml.sax
import sys
import time
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from Stemmer import Stemmer
class PageHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.data = ""
        self.title = ""
        self.text = ""  
        self.page_no = int(sys.argv[3])
        self.word_dict  = {}
        self.titles = []

    def startElement(self, tag, attributes):
        self.data = ""
    def endElement(self, tag):
        if(tag == "page"):
            self.page_no += 1
            print(self.page_no,end=" ")
            make_index(self.title, self.page_no,self.text, self.word_dict)
            print(time.time()-start)
            
        elif(tag == "title"):
            self.title = self.data
            (self.titles).append(self.title)
            self.data = ""
            
        elif(tag == "text"):
            self.text = self.data
            self.data = ""

    def characters(self, content):
        self.data = "".join([self.data,content])

stop_words = set(stopwords.words('english'))
def tokenize(text):
    text = text.lower()
    word_tokens = reg1.findall(text)
    filtered = [(ps.stemWord(w)) for w in word_tokens if (w != "" and w not in stop_words and len(w)>1)]
    return filtered

def extract_category(text):
    tokens = []
    categories = reg2.findall(text)
    for category in categories:
        tokens += tokenize((category))
    return tokens
def extract_info_box(text):
    tokens = []
    boxes = reg4.findall(text)
    for info in boxes:
        tokens += tokenize(str(info))
    return tokens
def extract_external_links(text):
    raw = text.split()
    tokens = []
    links = reg3.findall(text)
    for link in links:
        tokens+=(tokenize(link))
    return tokens
def extract_references(text):
    ans = []
    raw = text.split("\n")
    for lines in raw:
        if ("[[Category" in lines) or ("==" in lines) or ("DEFAULTSORT" in lines):
            break
        line = tokenize(lines)
        if "Reflist" in line:
            line.remove("Reflist")
        if "reflist" in line:
            line.remove("reflist")
        ans += line
    return ans

def process_field(tokens, ind, page, word_dict):
    for token in tokens:
        if token in word_dict:
            if page in word_dict[token]:
                word_dict[token][page][ind] += 1
            else:
                word_dict[token][page] = [0, 0, 0, 0, 0, 0]
                word_dict[token][page][ind] += 1
        else:
            word_dict[token] = {}
            word_dict[token][page] = [0, 0, 0, 0, 0, 0]
            word_dict[token][page][ind] += 1

def make_index(title, page, text, word_dict):
    process_field(tokenize(title), 0, page, word_dict)
    process_field(extract_category(text), 2, page, word_dict)
    process_field(extract_info_box(text), 3, page, word_dict)
    raw = text.split("==References==")
    process_field(tokenize(raw[0]), 1, page, word_dict)
    if(len(raw)>1):
        process_field(extract_external_links(raw[1]), 5, page, word_dict)
        process_field(extract_references(raw[1]), 4, page, word_dict)

def write_to_disk(word_dict, titles):
    loc = "./index/index_" + str(sys.argv[2]) + ".txt"
    f = open(loc, 'w')
    for word in (sorted(word_dict.keys())):
    	if(len(word)<=1):
    		continue
    	else:
	        arr = []
	        arr.append(word)
	        arr.append(":")
	        
	        for page in word_dict[word]:
	            arr.append('d')
	            arr.append(str(page))
	            if(word_dict[word][page][0]):
	                arr.append('t' + str(word_dict[word][page][0]))
	            if(word_dict[word][page][1]):
	                arr.append('b' + str(word_dict[word][page][1]))
	            if(word_dict[word][page][2]):
	                arr.append('c' + str(word_dict[word][page][2]))
	            if(word_dict[word][page][3]):
	                arr.append('i' + str(word_dict[word][page][3]))
	            if(word_dict[word][page][4]):
	                arr.append('r' + str(word_dict[word][page][4]))
	            if(word_dict[word][page][5]):
	                arr.append('e' + str(word_dict[word][page][5]))
	        line = "".join(arr)
	        f.write((line + '\n'))
    f.close()
    f = open("./titles/title_" + str(sys.argv[2]) + ".txt", 'w', encoding = "utf-8")
    for title in titles:
        f.write(title + '\n')
    f.close()


start = time.time()
reg1 = re.compile('[A-Za-z0-9]+')
reg2 = re.compile("\[\[Category:(.*)\]\]")
reg3 = re.compile("\[.*?\]")
reg4 = re.compile('\{\{\s*Infobox ((.*?\n)*?) *?\s*\}\}')
ps = Stemmer("porter")
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = PageHandler()
parser.setContentHandler( Handler )
parser.parse(("./Data/"+sys.argv[1]))
write_to_disk(Handler.word_dict, Handler.titles)
print(time.time()-start)
print(Handler.page_no)