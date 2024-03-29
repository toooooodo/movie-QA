import jieba as jb
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re


# 获取所有的文件
def getfilelist(root_path):
    file_path_list = []
    file_name = []
    walk = os.walk(root_path)
    for root, dirs, files in walk:
        for name in files:
            filepath = os.path.join(root, name)
            file_name.append(name)
            file_path_list.append(filepath)
    return file_path_list


class QuestionClassify:
    def __init__(self):
        # 读取训练数据
        self.train_x, self.train_y = self.read_train_data()
        # 训练模型
        self.model = self.train_model_NB()

    # 获取训练数据
    def read_train_data(self):
        train_x = []
        train_y = []
        file_list = getfilelist("./question/")
        # 遍历所有文件
        for i, one_file in enumerate(file_list):
            # 获取文件名中的数字
            num = re.sub(r'\D', "", one_file)
            # 如果该文件名有数字，则读取该文件
            if str(num).strip() != "":
                # 设置当前文件下的数据标签
                label_num = int(num)
                # 读取文件内容
                with(open(one_file, "r", encoding="utf-8")) as fr:
                    data_list = fr.readlines()
                    for one_line in data_list:
                        word_list = list(jb.cut(str(one_line).strip()))
                        # 将这一行加入结果集
                        train_x.append(" ".join(word_list))
                        train_y.append(label_num)
        print('train_x', len(train_x))
        print('train_y', len(train_y))
        return train_x, train_y

    # 训练并测试模型-NB
    def train_model_NB(self):
        x_train, y_train = self.train_x, self.train_y
        self.tv = TfidfVectorizer()
        # fit_transform 先fit，再transform
        train_data = self.tv.fit_transform(x_train).toarray()
        print('train_data: 0', train_data[0])
        clf = MultinomialNB(alpha=0.01)
        clf.fit(train_data, y_train)
        return clf

    # 预测
    def predict(self, question):
        question = [" ".join(list(jb.cut(question)))]
        print('question', question)
        test_data = self.tv.transform(question).toarray()
        print('test_data', test_data)
        print('predict', self.model.predict(test_data))
        y_predict = self.model.predict(test_data)[0]
        return y_predict


if __name__ == '__main__':
    qc = QuestionClassify()
    print(qc.predict("流浪地球的上映时间是什么时候"))
