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
    text = "".join(text.split())
    text += "."
    # text = re.sub(u"[^\w\s]", u"", text)
    # text = re.sub(u"[()]", u"", text)
    count = np.zeros(len(text))
    cnt = np.zeros(len(text))
    fq = nltk.FreqDist(text)
    bigrams_words = nltk.bigrams(text)
    cfd = nltk.ConditionalFreqDist(bigrams_words)
    for i in range(len(text)-1):
        count[i] = fq[text[i]]
        cnt[i] = cfd[text[i]][text[i+1]]
        if cnt[i] == 0:
            print text[i], text[i+1]
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
    # bigrams_words = nltk.bigrams(u"司XgI")
    # for i in bigrams_words:
    #     print i[0], i[1]
    t = codecs.open('/Users/Har/PycharmProjects/TermFinder/data/test_corpus/000159__2010_n.txt', 'r', 'utf-8').read()
    # print t
    mutual_information(t)
    # print t
    # ts = [i for i in t]
    # print ts.__len__()
    # mutual_information(ts)

    # a = np.array([1,2,3])
    # b = np.array([1,2,3])
    # print a[:-1]+b[1:]
    # print np.log(0)