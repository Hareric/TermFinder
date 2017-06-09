# coding=utf-8
"""
create_time = 2016/6/6
author = Eric_Chan
用来训练crf模型及预测
需要正确安装crf++开源包
"""

from create_train_data import *
import MM


class CRFs:
    def __init__(self, term_file_path, train_term_file_path):
        """
        :param term_file_path: 所有术语 文件路径
        :param train_term_file_path: 训练文本中出现的术语 文件路径
        :return:
        """
        self.cw = MM.CutWord(term_file_path)
        self.terms = set(MM.load_file(term_file_path))
        self.train_terms = set(MM.load_file(train_term_file_path))

    @staticmethod
    def train_CRFs(template_path, crf_train_path, model_path):
        os.system('crf_learn -f 3 -c 4.0 ' + template_path + ' ' + crf_train_path + ' ' + model_path)

    def test_CRFs(self, model_path, test_file_path, test_result_path):
        content = read_file(test_file_path)
        temp_path_crf = 'data/cache/crf_test.txt'
        temp_path_crf_result = 'data/cache/crf_test_result.txt'
        character_split(content, temp_path_crf)
        # 写入预测结果
        os.system('crf_test -m ' + model_path + ' ' + temp_path_crf + ' > ' + temp_path_crf_result)
        # 写入真实结果
        sent = read_file(test_file_path)
        words = self.cw.mm_cut(sent, 15)
        character_tagging_2(words, temp_path_crf_result, test_result_path)

    def elevate_result(self, result_path):
        """
        对预测结果进行评测
        :param result_path:
        :return:
        """
        lines = MM.load_file(result_path)
        new_term_unknown = []  # 识别出新的未知术语
        new_term_sub = []  # 识别出新的已知术语
        id_term_num = 0  # 识别出术语个数
        term_num = 0  # 标注术语个数
        correct_num = 0

        term_id = u''
        term_c = u''
        i = 0
        while i < len(lines):
            if not lines[i]:
                i += 1
                continue
            t = lines[i].split('\t')
            i += 1
            if t[0] != t[3]:
                print result_path + "  该结果文件格式有误"
                return
            if t[2] == t[4]:
                if t[2] == u'S':
                    continue
                elif t[2] == u'B':
                    a, b = i, i
                    term_id += t[0]
                    term_c += t[0]
                    while True:
                        term_id += lines[a].split('\t')[0]
                        if lines[a].split('\t')[2] == u'E':
                            break
                        a += 1
                    while True:
                        term_c += lines[b].split('\t')[0]
                        if lines[b].split('\t')[4] == u'E':
                            break
                        b += 1
                    if a == b:
                        term_num += 1
                        id_term_num += 1
                        correct_num += 1
                        i = a + 1
                        if term_id not in self.train_terms:
                            new_term_unknown.append(term_id)
                    else:
                        term_num += 1
                        id_term_num += 1
                        correct_num += 1
                        i = min([a, b]) + 1
                        if term_id not in self.train_terms:
                            new_term_sub.append(term_id)
                    term_id, term_c = '', ''
            else:
                if t[2] == u'B':
                    id_term_num += 1
                    a = i
                    term_id += t[0]
                    while True:
                        term_id += lines[a].split('\t')[0]
                        if lines[a].split('\t')[2] == u'E':
                            break
                        a += 1
                    if term_id not in self.train_terms:
                            new_term_unknown.append(term_id)
                    term_id = ''
                if t[4] == u'B':
                    term_num += 1
                    term_c += t[0]
                    b = i
                    while True:
                        term_c += lines[b].split('\t')[0]
                        if lines[b].split('\t')[4] == u'E':
                            break
                        b += 1
                    term_c = ''
                # print i, lines[i-1].split('\t')[0]
        print "识别出的新术语(sub)"
        print '\n'.join(set(new_term_sub))
        print "--------"
        print '\n'.join(set(new_term_unknown))
        recall = correct_num * 1.0 / term_num
        precise = correct_num * 1.0 / id_term_num
        print "对新术语忽略不计: 召回率", recall, '精度:' , precise
        print term_num, id_term_num, correct_num








if __name__ == '__main__':
    # 训练crfs模型
    # CRFs.train_CRFs('data/template.txt', 'data/0_train/CRF_train.txt', 'data/0_train/model')

    # 对测试集进行术语识别
    crfs = CRFs(term_file_path='data/terms.txt', train_term_file_path='data/2_train/terms_train.txt')
    # crfs.test_CRFs('data/2_train/model', '/Users/Har/PycharmProjects/corpus/test/600793_2010.txt', '/Users/Har/PycharmProjects/TermFinder/data/2_train/test_result/600793_2010.txt')

    # path_list = get_path('/Users/Har/PycharmProjects/corpus/test/')
    # for path in path_list:
    #     print path
    #     crfs.test_CRFs('data/2_train/model', path, 'data/2_train/test_result/' + path.split('/')[-1])

    # evaluate
    crfs.elevate_result('/Users/Har/PycharmProjects/TermFinder/data/2_train/test_result/600793_2010.txt')