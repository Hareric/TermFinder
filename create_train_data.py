# coding=utf-8
"""
author = Eric_Chan
create_time = 2017/06/1
说明
创建CRF训练文件
"""

import codecs
from MM import *
import os


def get_path(root_path):
    """
    获取文件夹中所有文件的路径
    :param root_path:
    :return:
    """
    path_list = []
    for lists in os.listdir(root_path):
        if lists.startswith('.'):
            continue
        path = os.path.join(root_path, lists)
        path_list.append(path)
    return path_list


def character_tagging(word_list, output_file):
    """
    输入分词后的 词语列表 输出训练集格式txt
    :param word_list:
    :param output_file:
    :return:
    """
    output_data = codecs.open(output_file, 'a', 'utf-8')
    for word in word_list:
        if len(word) == 1:
            output_data.write(word + "\tS\n")
        else:
            output_data.write(word[0] + "\tB\n")
            for w in word[1:len(word) - 1]:
                output_data.write(w + "\tM\n")
            output_data.write(word[len(word) - 1] + "\tE\n")
    output_data.write('\n')
    output_data.close()


def character_tagging_2(word_list, input_file, output_file):
    """

    :param word_list: 标注词
    :param input_file: 识别结果文件
    :param output_file: 合并结果
    :return:
    """
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    line = input_data.readline().strip()

    for word in word_list:
        if not word.strip():
            continue
        if len(word) == 1:
            output_data.write(line + '\t' + word + "\tS\n")
            line = input_data.readline().strip()
        else:
            output_data.write(line + '\t' + word[0] + "\tB\n")
            line = input_data.readline().strip()
            for w in word[1:len(word) - 1]:
                output_data.write(line + '\t' + w + "\tM\n")
                line = input_data.readline().strip()
            output_data.write(line + '\t' + word[len(word) - 1] + "\tE\n")
            line = input_data.readline().strip()
    output_data.write('\n')
    output_data.close()
    input_data.close()




def character_split(input_data, output_file):
    """
    输入文本,输出测试集格式txt
    :param input_data:
    :param output_file:
    :return:
    """
    input_data = ''.join(input_data.split())
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for word in input_data:
        output_data.write(word + "\tB\n")
    output_data.close()


def character_2_word(input_file, output_file):
    """
    将CRF识别出的分词结果 合成为句子 写入新的文档 并返回识别出的术语
    :param input_file:
    :param output_file:
    :return:
    """
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    terms = []  # 识别出的术语
    term = ''
    for line in input_data.readlines():
        if line == "\n":
            output_data.write("\n")
        else:
            char_tag_pair = line.strip().split('\t')
            char = char_tag_pair[0]
            tag = char_tag_pair[2]
            if tag == 'B':
                term += char
                output_data.write('{[' + char)
            elif tag == 'M':
                term += char
                output_data.write(char)
            elif tag == 'E':
                term += char
                terms.append(term)
                term = ''
                output_data.write(char + ']}')
            else:  # tag == 'S'
                output_data.write(char)
    input_data.close()
    output_data.close()
    return terms


def create_crf_train_data(root_folder_path, write_folder_path):
    """
    创建CRF训练文档 将多个文档 合并成一个txt
    :param root_folder_path: 训练数据集的文件夹路径
    :param write_folder_path: 处理后训练文档的文件夹路径
    :return:CRF_train.txt  训练集
            terms_train.txt  训练集中出现的术语
    """
    train_data_path = get_path(root_folder_path)
    cw = CutWord()
    s = train_data_path.__len__()
    i = 1
    for path in train_data_path:
        print s - i, path
        i += 1
        sen = read_file(path)
        words = cw.mm_cut(sen, 15)
        character_tagging(words, write_folder_path + '/CRF_train.txt')
    # print '\n'.join(cw.terms)
    print "出现的术语个数", cw.terms.__len__()
    write_file(write_folder_path + '/terms_train.txt', cw.terms)


def create_crf_train_data_split(root_folder_path, write_folder_path):
    """
    创建CRF训练文档  将多个文档分别存放成txt
    :param root_folder_path: 训练数据集的文件夹路径
    :param write_folder_path: 处理后训练文档的文件夹路径
    :return:CRF_train.txt  训练集
            terms_train.txt  训练集中出现的术语
    """
    train_data_path = get_path(root_folder_path)
    cw = CutWord()
    s = train_data_path.__len__()
    i = 1
    for path in train_data_path:
        print s - i, path
        i += 1
        sen = read_file(path)
        words = cw.mm_cut(sen, 15)
        character_tagging(words, write_folder_path + '/CRF_train_' + path.split('/')[-1])
    # print '\n'.join(cw.terms)
    print "出现的术语个数", cw.terms.__len__()
    write_file(write_folder_path + '/terms_train.txt', cw.terms)


def create_crf_test_data(root_folder_path, write_folder_path):
    """
    创建CRF测试集
    :param root_folder_path: 测试数据集的文件夹路径
    :param write_folder_path: 处理后的测试文档文件夹路径
    :return:
    """
    test_data_path = get_path(root_folder_path)
    s = test_data_path.__len__()
    i = 1
    for path in test_data_path:
        print s - i, path
        i += 1
        content = read_file(path)
        character_split(content, write_folder_path + '/crf_test_' + path.split('/')[-1])


if __name__ == '__main__':

    # 创建CRF训练集
    # create_crf_train_data('/Users/Har/PycharmProjects/corpus/train', 'data/2_train')
    create_crf_train_data('../term_model/1212', '../term_model/1212')
