# 基于条件随机场的术语识别


---
## 代码说明
### 开源包
numpy

nltk

crf++ 
### py说明
***preprocess.py*** 对金融术语的预处理

***MM.py*** 提供词库对指定字符串进行分词

***create_train_data.py*** 指定语料文件夹，创建CRF训练文件

***create_feature.py*** 计算信息熵 互信息 相关度并离散化 添加进训练文本或测试文本

***test_elevate_CRF.py*** 使用训练的模型对新语料进行识别和评价

### 示例代码
test_elevate_CRF.py
```python
# 实例化CRFs, 读入术语词库 和 训练集中出现的已登录术语
crfs = CRFs(term_file_path='data/terms.txt',
            train_term_file_path='data/model/terms_train.txt')

test_path = 'data/test/600851_2010.txt'  # 测试文本的路径
result_path = 'data/test/600851_2010_result.txt'  # 识别结果存放的路径
feature_list = ['rel', 'mi', 'en']  # 使用的特征组合
model_path = 'data/model/model_rel_mi_en'  # 模型的路径

crfs.test_CRFs(model_path=model_path,  # 使用的模型的路径
               test_file_path=test_path,
               test_result_path=result_path,
               feature_list=feature_list)
# evaluate
new_terms_dict = {'title': crfs.elevate_result(result_path)}

# 保存新术语
write_xls('data/test/new_terms.xls', new_terms_dict)
```

## 测试结果文本
### 原始文本
![test txt][2]
### 模型预测后输出的结果
前1-5列为输入的训练集

第6列为预测的结果标注

第7-8列为直接使用词典分词的标注
![test result][3]
### 识别出的未登录术语
![new terms][1]

## 下载
训练集及测试集语料[下载][4]


  [1]: https://raw.githubusercontent.com/Hareric/tuchuang/master/graph/new_terms_xls.png
  [2]: https://raw.githubusercontent.com/Hareric/tuchuang/master/graph/test_txt.png
  [3]: https://raw.githubusercontent.com/Hareric/tuchuang/master/graph/test_result.png
  [4]: https://raw.githubusercontent.com/Hareric/tuchuang/master/document/%E9%87%91%E8%9E%8D%E8%AF%AD%E6%96%99%E9%9B%86.zip
