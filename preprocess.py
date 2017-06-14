# coding=utf-8
"""
Author = Eric Chan
Create_Time = 2017/6/1
"""
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


def read_file(path, split_tag, encoding):
    """
    获取指定文件的内容
    :param path:
    :param split_tag:
    :return:
    """
    f = open(path)
    content = f.read().decode(encoding)
    # print content
    line_list = []
    for l in content.split(split_tag):
        if l.strip():
            line_list.append(l.strip())
    return line_list


def get_term_list():
    """
    :param root_path:
    :return:
    """
    path_list = []
    path_list += (get_path('data/金融/金融术语'))
    path_list += (get_path('data/金融/金融百科'))
    print '\n'.join(path_list)
    term_list = set()
    for path in path_list:
        term_list = term_list.union(read_file(path, '\n', 'utf-8_sig'))
    path_list = get_path('data/wiki')
    for path in path_list:
        term_list = term_list.union(read_file(path, '\n', 'GBK'))
    return list(term_list)

if __name__ == '__main__':
    terms = get_term_list()
    print '\n'.join(terms)
    print terms.__len__()