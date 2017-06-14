# coding=utf-8
"""
create_time = 2016/6/6
author = Eric_Chan
用来训练crf模型及预测
需要正确安装crf++开源包
"""
import xlwt

from create_train_data import *
import MM
from create_feature import relevance, mutual_information, entropy, append_feature


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
        """
        :param template_path: 模板文件 路径
        :param crf_train_path: 训练文本 路径
        :param model_path: 生成的模型 路径
        :return:
        """
        os.system('crf_learn -f 3 -c 4.0 ' + template_path + ' ' + crf_train_path + ' ' + model_path)

    def test_CRFs(self, model_path, test_file_path, test_result_path, feature_list=None):
        """
        :param model_path: 使用的模型 路径
        :param test_file_path: 需要识别的测试文本 路径 (原始文本 无需预处理)
        :param test_result_path: 识别出的文本的结果 路径
        :param feature_list: 需要增加的特征(与模型特征保持一致) 可选特征有 rel:相关度 en:信息熵 mi:互信息值
        :return:
        """
        content = codecs.open(test_file_path, 'r', 'utf-8').read()
        content = ''.join(content.split())  # 去除空格
        temp_path_crf = 'data/cache/crf_test.txt'
        temp_path_crf_result = 'data/cache/crf_test_result.txt'
        character_split(content, temp_path_crf)
        if feature_list is not None:
            for f in feature_list:
                if f == 'rel':  # 计算相关度
                    rel_array = relevance(content)
                    append_feature(temp_path_crf, rel_array)
                elif f == 'en':  # 计算信息熵
                    en_array = entropy(content)
                    append_feature(temp_path_crf, en_array)
                elif f == 'mi':  # 计算互信息值
                    mi_array = mutual_information(content)
                    append_feature(temp_path_crf, mi_array)
                else:
                    print f, "   无该特征!!"
                    return
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
        new_term_sub = []  # 识别出新的子术语
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
            if t[0] != t[-2]:
                print result_path + "  该结果文件格式有误"
                return
            if t[-3] == t[-1]:
                if t[-3] == u'S':
                    continue
                elif t[-3] == u'B':
                    a, b = i, i
                    term_id += t[0]
                    term_c += t[0]
                    while True:
                        term_id += lines[a].split('\t')[0]
                        if lines[a].split('\t')[-3] == u'E':
                            break
                        a += 1
                    while True:
                        term_c += lines[b].split('\t')[0]
                        if lines[b].split('\t')[-3] == u'E':
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
                if t[-3] == u'B':
                    id_term_num += 1
                    a = i
                    term_id += t[0]
                    while True:
                        term_id += lines[a].split('\t')[0]
                        if lines[a].split('\t')[-3] == u'E':
                            break
                        a += 1
                    if term_id not in self.train_terms:
                        new_term_unknown.append(term_id)
                    term_id = ''
                if t[-1] == u'B':
                    term_num += 1
                    term_c += t[0]
                    b = i
                    while True:
                        term_c += lines[b].split('\t')[0]
                        if lines[b].split('\t')[-1] == u'E':
                            break
                        b += 1
                    term_c = ''
                    # print i, lines[i-1].split('\t')[0]
        # print "识别出的新术语(sub)"
        # print '\n'.join(set(new_term_sub))
        # print "--------"
        # print '\n'.join(set(new_term_unknown))
        recall = correct_num * 1.0 / term_num
        precise = correct_num * 1.0 / id_term_num
        print "对新术语忽略不计: 召回率", recall, '精度:' , precise
        print term_num, id_term_num, correct_num
        return list(set(new_term_sub + new_term_unknown))


def write_xls(path, terms_dict):
    """
    将新识别的术语存入xls
    :param path: 存入路径
    :param terms_dict: {标题: [术语列表]}
    :return:
    """
    file_0 = xlwt.Workbook(encoding='utf-8')
    table_0 = file_0.add_sheet('term')
    current_row = 2
    for k in terms_dict.keys():
        table_0.write(current_row, 0, k)
        for t in terms_dict[k]:
            table_0.write(current_row, 1, t)
            current_row += 1
    file_0.save(path)


# if __name__ == '__main__':
#     d = {'132':['1','2','3'],'1322':['1','2','3'],'3132':['1','2','3']}
#     write_xls('data/ttt.xls', d)


if __name__ == '__main__':
    # 训练crfs模型
    # CRFs.train_CRFs('data/template.txt', 'data/0_train/CRF_train.txt', 'data/0_train/model')

    # 对测试集进行术语识别
    crfs = CRFs(term_file_path='data/terms.txt',
                train_term_file_path='/Users/Har/PycharmProjects/term_model/model/terms_train.txt')

    def run(fea=''):  # None   _en   _mi   _mi_en   _rel   _rel_en   _rel_mi   rel_mi_en
        feature_list = fea.split('_')[1:]
        print feature_list
        path_list = get_path('/Users/Har/PycharmProjects/term_model/corpus/test')
        new_terms_dict = {}
        for i, path in enumerate(path_list):
            print i, path
            title = path.split('/')[-1]
            result_path = '/Users/Har/PycharmProjects/term_model/corpus/test_result' + fea + '/' + title
            crfs.test_CRFs('/Users/Har/PycharmProjects/term_model/model/model' + fea,
                           path,
                           result_path,
                           feature_list=feature_list)
            # evaluate
            new_terms_dict[title] = crfs.elevate_result(result_path)

        # 保存新术语
        write_xls('data/new_terms/feature' + fea + '.xls', new_terms_dict)

    run()
    run('_rel')  # 添加相关度作为特征
    run('_mi')  # 添加互信息作为特征
    run('_en')  # 添加信息熵作为特征
    run('_mi_en')
    run('_rel_en')
    run('_rel_mi')
    run('_rel_mi_en')

