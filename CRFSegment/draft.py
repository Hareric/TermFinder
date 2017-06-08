__author__ = 'Har'
import jieba

f = open('data/learn.txt')
s = f.read()
ns = " ".join(jieba.cut(s))
f1 = open('data/learn_cut.txt', 'w')
print type(ns)
f1.write(ns.encode('utf8'))
