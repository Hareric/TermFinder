# coding=utf-8
__author__ = 'Har'
import codecs
import os
import MM
import numpy as np
def character_split(output_file):
    input_data = u'你好吗\n你好多哈手动iwahfi'
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.split('\n'):
        for word in line.strip():
            word = word.strip()
            if word:
                output_data.write(word + "\tB\n")
        output_data.write("\n")


if __name__ == '__main__':
    d = np.array(['dasd', 'asdasd','ad'])
    print d