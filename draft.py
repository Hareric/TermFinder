# coding=utf-8
import xlwt
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
        current_row += 1
        for t in terms_dict[k]:
            table_0.write(current_row, 1, t)
            current_row += 1
    file_0.save('terms.xls')
