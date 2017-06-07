# coding=utf-8
#        ┏┓　　　┏┓+ +
# 　　　┏┛┻━━━┛┻┓ + +
# 　　　┃　　　　　　 ┃ 　
# 　　　┃　　　━　　　┃ ++ + + +
# 　　 ████━████ ┃+
# 　　　┃　　　　　　 ┃ +
# 　　　┃　　　┻　　　┃
# 　　　┃　　　　　　 ┃ + +
# 　　　┗━┓　　　┏━┛
# 　　　　　┃　　　┃　　　　　　　　　　　
# 　　　　　┃　　　┃ + + + +
# 　　　　　┃　　　┃　　　　Codes are far away from bugs with the animal protecting　　　
# 　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug　　
# 　　　　　┃　　　┃
# 　　　　　┃　　　┃　　+　　　　　　　　　
# 　　　　　┃　 　　┗━━━┓ + +
# 　　　　　┃ 　　　　　　　┣┓
# 　　　　　┃ 　　　　　　　┏┛
# 　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　┃┫┫　┃┫┫
# 　　　　　　┗┻┛　┗┻┛+ + + +
"""
Author = Eric Chan
Create_Time = 2016/10/07
中文分词,使用算法为
正向最大匹配法(Maximum Matching Method, 简称MM算法)
逆向最大匹配算法(Reverse Maximum Matching Method, 简称RMM算法)
"""


def read_file(file_name, charset='utf-8'):
    f = open(file_name)
    content = f.read().decode(charset)
    line = ''
    for l in content.split('\n'):
        if l.strip():
            line += (l.strip())
    return line


def load_file(file_name, charset='utf-8', split_tag='\n'):
    """
    读取文件，按列返回列表
    :param file_name: 文件路径
    :param charset: 文本内容decode的编码，默认为utf-8
    :return: 文本内容列表
    """
    f = open(file_name)
    content = f.read().decode(charset)
    # print content
    line_list = []
    for l in content.split(split_tag):
        if l.strip():
            line_list.append(l.strip())
    return line_list

def write_file(path, line_list, charset='utf-8'):
    line_list = list(line_list)
    f = open(path, 'w')
    for line in line_list:
        f.write(line.encode(charset)+'\n')
    f.close()



class CutWord:
    word_set = None

    def __init__(self, term_file_path='./data/terms.txt'):
        self.word_set = set(load_file(term_file_path))
        self.terms = set()

    def mm_cut(self, sentence=u'', max_len=6):
        """
        使用正向最大匹配法划分词语
        :param sentence: str 待划分句子
        :param max_len: int 最大词长 默认为6
        :return: str-list 已分词的字符串列表
        """
        sentence = sentence
        cur = 0  # 表示分词的位置
        sen_len = sentence.__len__()  # 句子的长度
        word_list = []  # 划分的结果
        while cur < sen_len:
            l = None
            for l in range(max_len, 0, -1):
                if sentence[cur: cur + l] in self.word_set:
                    break
            word_list.append(sentence[cur: cur + l])
            if l > 1:
                self.terms.add(sentence[cur: cur + l])
            cur += l
        return word_list

    def rmm_cut(self, sentence=u'', max_len=6):
        """
        使用逆向最大匹配法划分词语
        :param sentence: str 待划分句子
        :param max_len: int 最大词长 默认为6
        :return: str-list 已分词的字符串列表
        """
        sentence = sentence
        sen_len = sentence.__len__()  # 句子的长度
        cur = sen_len  # 表示分词的位置
        word_list = []  # 划分的结果
        while cur > 0:
            l = None
            if max_len > cur:
                max_len = cur
            for l in range(max_len, 0, -1):
                if sentence[cur - l: cur] in self.word_set:
                    break
            word_list.insert(0, sentence[cur - l: cur])
            cur -= l
        return word_list


if __name__ == '__main__':
    import time
    # sen = u'我爱吃大白菜'
    sen = read_file('data/corpus/000001__2010_n.txt')
    # print sen[:300]
    CW = CutWord()

    print "mm"
    r = CW.mm_cut(sen, 15)
    print '|'.join(r)[:880]
    print '\n'.join(CW.terms)
    print CW.terms.__len__()

