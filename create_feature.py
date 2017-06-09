# coding=utf-8
"""
author = Eric Chan
create_time = 2016/10/07

create_train_data.py 中已创建的训练集 添加新的特征

互信息
相关度
信息熵
"""
import numpy as np
import nltk
import codecs
from create_train_data import create_crf_train_data_split, get_path


def load_crf_train_data(path):
    c = codecs.open(path, 'r', 'utf-8').read()
    text = ''.join(c.split()[::2])
    # print text
    return text


def append_feature(path, feature_array):
    """
    对CRF训练文本添加新特征
    :param path:
    :param feature_array:
    :return:
    """
    origin_data = codecs.open(path, 'r', 'utf-8').readlines()
    new_data = codecs.open(path, 'w', 'utf-8')
    for i in range(len(feature_array)):
        new_data.write(origin_data[i].strip() + '\t' + str(feature_array[i]) + '\n')
    new_data.close()

def merge_feature(path_1, path_2):
    """
    将path_2的特征加在path_1的末尾
    :param path_1:
    :param path_2:
    :return:
    """
    path_1_data = codecs.open(path_1, 'r', 'utf-8').readlines()
    path_2_data = codecs.open(path_2, 'r', 'utf-8').readlines()
    new_data = codecs.open(path_1, 'w', 'utf-8')
    for i in range(len(path_1_data)):
        new_data.write(path_1_data[i].strip() + '\t' + path_2_data[i].split()[-1] + '\n')
    new_data.close()


def merge_file(root_folder_path, new_file_path):
    """
    将文件夹内所有文件 合并成一个文件
    :param root_folder_path:
    :param new_file_path:
    :return:
    """
    output_data = codecs.open(new_file_path, 'w', 'utf-8')
    path_list = get_path(root_folder_path)
    for path in path_list:
        output_data.write(codecs.open(path, 'r', 'utf-8').read())
        output_data.write('\n')
    output_data.close()


def mutual_information(text):
    """
    计算每个字(词)相邻与相邻右边字(词)的互信息值
    将所有的互信息值进行排序 划分为5个等级. 互信息值最大为1 最小为5
    :param text: 字符串 或 分词后的列表
    :return: 已离散化后的互信息值
    """
    if isinstance(text, unicode):
        text = "".join(text.split())
    k = len(text)
    text += "."  # 最后添加一个字符防止数组越界
    count = np.zeros(k + 1)
    cnt = np.zeros(k)
    fq = nltk.FreqDist(text)
    bigrams_words = nltk.bigrams(text)
    cfd = nltk.ConditionalFreqDist(bigrams_words)
    for i in range(k):
        count[i] = fq[text[i]]
        cnt[i] = cfd[text[i]][text[i + 1]]
        if cnt[i] == 0:
            print text[i], text[i + 1]
    count[-1] = fq[text[-1]]
    mi = np.log(text.__len__() * cnt / (count[:-1] * count[1:])) / np.log(2)
    # 离散化
    mi_sort = np.sort(mi)
    a1, a2, a3, a4 = mi_sort[k / 5], mi_sort[k * 2 / 5], mi_sort[k * 3 / 5], mi_sort[k * 4 / 5]
    discrete_mi = np.zeros(k, dtype=np.int32)
    for c in range(k):
        if mi[c] >= a4:
            discrete_mi[c] = 1
        elif mi[c] >= a3:
            discrete_mi[c] = 2
        elif mi[c] >= a2:
            discrete_mi[c] = 3
        elif mi[c] >= a1:
            discrete_mi[c] = 4
        else:
            discrete_mi[c] = 5
    # for i, j in zip(discrete_mi, text[:-1]):
    #     print i, j
    return discrete_mi


def relevance(text):
    """

    :param text: 字符串 或 分词后的列表
    :return: 已离散化后的相关度值
    """
    if isinstance(text, unicode):
        text = "".join(text.split())
    n = len(text)
    text += "."  # 最后添加一个字符防止数组越界
    fq = nltk.FreqDist(text)
    bigrams_words = nltk.bigrams(text)
    cfd = nltk.ConditionalFreqDist(bigrams_words)
    n_11 = np.zeros(n)
    n_12 = np.zeros(n)
    n_21 = np.zeros(n)
    n_22 = np.zeros(n)
    for i in range(n):
        n_11[i] = cfd[text[i]][text[i + 1]]
        n_12[i] = fq[text[i]] - n_11[i]
        n_21[i] = fq[text[i + 1]] - n_11[i]
        n_22[i] = n - n_11[i] - n_12[i] - n_21[i]
    rel = np.power(n * (n_11 * n_22 - n_12 * n_21), 2) / (n_11 + n_12) * (n_21 + n_22) * (n_11 + n_21) * (n_22 + n_12)

    # 离散化
    rel_sort = np.sort(rel)
    a1, a2, a3, a4 = rel_sort[n / 5], rel_sort[n * 2 / 5], rel_sort[n * 3 / 5], rel_sort[n * 4 / 5]
    discrete_rel = np.zeros(n, dtype=np.int32)
    for c in range(n):
        if rel[c] >= a4:
            discrete_rel[c] = 1
        elif rel[c] >= a3:
            discrete_rel[c] = 2
        elif rel[c] >= a2:
            discrete_rel[c] = 3
        elif rel[c] >= a1:
            discrete_rel[c] = 4
        else:
            discrete_rel[c] = 5
    return discrete_rel


def entropy(text):
    """
    计算每个字(词)的信息熵
    if entropy_left < entropy_right
        标注为lft (该字(词)偏向于与左相连 )
    else
        标注为 rgh
    :param text: 字符串 或 分词后的列表
    :return: [lft, rgh, ....,]
    """
    if isinstance(text, unicode):
        text = "".join(text.split())
    n = len(text)
    bigrams_words = nltk.bigrams(text)
    cfd = nltk.ConditionalFreqDist(bigrams_words)
    bigrams_words_reversed = nltk.bigrams(text[::-1])
    cfd_reversed = nltk.ConditionalFreqDist(bigrams_words_reversed)
    ent_right = np.zeros(n)
    ent_left = np.zeros(n)
    result = ['rgh']
    for i in range(n)[1:-1]:
        en = np.array(cfd[text[i]].values(), dtype=np.float)
        en = en / en.sum()
        en = en * (np.log(en) / np.log(2))
        ent_right[i] = -en.sum()
        en = np.array(cfd_reversed[text[i]].values(), dtype=np.float)
        en = en / en.sum()
        en = en * (np.log(en) / np.log(2))
        ent_left[i] = -en.sum()

        if ent_left[i] < ent_right[i]:
            result.append('lft')
        else:
            result.append('rgh')
    result.append('lft')
    # for i, j in zip(result, text):
    #     print i, j
    return result


if __name__ == '__main__':
    # 创建CRF_train训练集
    # create_crf_train_data_split('/Users/Har/PycharmProjects/corpus/train', 'data/3_train')
    # create_crf_train_data_split('/Users/Har/PycharmProjects/corpus/未命名文件夹','/Users/Har/PycharmProjects/corpus/未命名文件夹')

    # 添加互信息特征
    # path_list = get_path('/Users/Har/PycharmProjects/term_model/3_train_mi')
    # s = path_list.__len__()
    # c = 1
    # for path in path_list:
    #     print s - c, path
    #     c += 1
    #     text = load_crf_train_data(path)
    #     mi_array = mutual_information(text)
    #     append_feature(path, mi_array)

    # 添加信息熵特征
    # path_list = get_path('/Users/Har/PycharmProjects/term_model/3_train_en')
    # s = path_list.__len__()
    # c = 1
    # for path in path_list:
    #     print s - c, path
    #     c += 1
    #     text = load_crf_train_data(path)
    #     en_array = entropy(text)
    #     append_feature(path, en_array)

    # 添加相关度值
    # path_list = get_path('/Users/Har/PycharmProjects/term_model/3_train_rel')
    # s = path_list.__len__()
    # c = 1
    # for path in path_list:
    #     print s - c, path
    #     c += 1
    #     text = load_crf_train_data(path)
    #     en_array = relevance(text)
    #     append_feature(path, en_array)


    # merge en mi
    # path_list = get_path('/Users/Har/PycharmProjects/term_model/3_train_en_mi')
    # s = path_list.__len__()
    # c = 1
    # for path in path_list:
    #     print s - c, path
    #     c += 1
    #     merge_feature(path, '/Users/Har/PycharmProjects/term_model/3_train_mi/'+path.split('/')[-1])

    # merge rel en
    path_list = get_path('/Users/Har/PycharmProjects/term_model/3_train_rel_en')
    s = path_list.__len__()
    c = 1
    for path in path_list:
        print s - c, path
        c += 1
        merge_feature(path, '/Users/Har/PycharmProjects/term_model/3_train_en/'+path.split('/')[-1])

    # merge rel mi
    path_list = get_path('/Users/Har/PycharmProjects/term_model/3_train_rel_mi')
    s = path_list.__len__()
    c = 1
    for path in path_list:
        print s - c, path
        c += 1
        merge_feature(path, '/Users/Har/PycharmProjects/term_model/3_train_mi/'+path.split('/')[-1])

