#coding=utf-8
import sre_constants

import numpy as np
import nltk.collocations
import codecs
import re

def mutual_information(text):
    """
    计算每个字(词)相邻右边的互信息
    :return:
    """
    text += " "
    # text = re.sub(u"[^\w\s]", u"", text)
    # text = re.sub(u"[()]", u"", text)
    count = np.zeros(len(text))
    cnt = np.zeros(len(text))
    fq = nltk.FreqDist(text)
    for i in range(len(text)-1):
        count[i] = fq[text[i]]
        try:
            cnt[i] = re.findall(text[i]+text[i+1], text).__len__()
        except sre_constants.error:
            print i
            print text[i]+text[i+1]
            cnt[i] = 1

    count[-1] = fq[text[-1]]
    ct = np.log(text.__len__()*cnt[:-1] / (count[:-1]*count[1:])) / np.log(2)
    # 离散化
    ct_sort = np.sort(ct)
    a1, a2, a3, a4 = ct_sort[ct.size/5], ct_sort[ct.size*2/5],ct_sort[ct.size*3/5],ct_sort[ct.size*4/5]
    result = []
    for c in ct:
        if c >= a4:
            result.append(1)
        elif c >= a3:
            result.append(2)
        elif c >= a2:
            result.append(3)
        elif c >= a1:
            result.append(4)
        else:
            result.append(5)
    for i, j in zip(result, text[:-1]):
        print i, j





if __name__ == '__main__':
    text = "你好吗a"
    text = re.sub(u"[^\w\s]", u"", text)
    text = re.sub(u"[()]", u"", text)
    print text
    t = codecs.open('/Users/Har/PycharmProjects/TermFinder/data/test_corpus/000159__2010_n.txt', 'r', 'utf-8').read()
    # print t
    # ts = [i for i in t]
    # print ts.__len__()
    # mutual_information(ts)

    mi(t)
    # a = np.array([1,2,3])
    # b = np.array([1,2,3])
    # print a[:-1]+b[1:]
    # print np.log(0)