import jieba.analyse
import re
import time


def makeIndex(filepath):
    index = {}
    with open(filepath) as handle:
        for i,ln in enumerate(handle):
            for word in re.compile("\w+").findall(ln):
                index.setdefault(word,[]).append(i+1)#添加键、值
    return index

def indexQuery(index,*words):#可容纳多个变量组成的lis   ('台湾',)<class 'tuple'>元祖
    found = None#美国[4, 15, 19, 25, 33, 65, 67, 67, 67, 67, 67, 67]
    for word in words:
        got = index.get(word, [])
        if not got:#wordlist里面没有
            return None
        if not found:
            found = set(got)#转化为集合
        else:
            found &= set(got)#去重复元素
    return list(found)


def getLine(filepath, line_num):#获得指定行的内容
    if line_num<1:
        return ''
    for cur_line_num,line in enumerate(open(filepath,'r')):
        if (cur_line_num/2) == line_num-1: #/2的原因是读的两每行对应实际urls.txt的一个url
            return line
    return ''


def count_tfidf(locations,keywords):
    location_dic = {}
    for i,location in enumerate( locations):#循环关键词所在的每篇文档
        temp = 0
        word_line = getLine('../docs/wordList.txt',location)#word_list.txt的地址
        words = word_line.split()
        for j,word in enumerate(words):#所在文章中的每个单词 0~19
            for top in keywords:
                if word == top[0]:
                    tf_idf_line = getLine("../docs/tfidfList.txt",location) #获取该篇文章20个词的tf行
                    tf_idf = tf_idf_line.split()
                    tf = float(tf_idf[j])*float(top[1]) #将word_list和keyword中的tf相乘后累加
                    temp = temp + tf
        location_dic[location] = temp
    return location_dic


def print_location(location_sort):
    i = 0
    print("共搜索到:"+str(len(location_sort))+"个结果:")
    for location in location_sort:
        url = getLine("../docs/urls.txt",location)
        if(url!=""):
            i = i+1
            print(url)
    print(i)

word_list_path = '../docs/wordList.txt'
index = makeIndex(word_list_path)
userinput = input("请输入关键字:")

startTime = time.time()
keywords = jieba.analyse.extract_tags(userinput,topK=5,withWeight=True,allowPOS=(),withFlag=False)
locations = []

for top in keywords:#检索每个词获取文档下标
    location = indexQuery(index,top[0])# top[0] str
    print(location)
    locations.extend(location)

location_dic = count_tfidf(locations,keywords)

print(location_dic)
# location_sort = sorted(location_dic.keys(),reverse=True)
location_sort = sorted(location_dic.keys())
print(location_sort)
print_location(location_sort)

endTime = time.time()
print('running time')
print(endTime-startTime)
