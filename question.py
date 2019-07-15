import jieba as jb
from jieba import posseg
from question_classification import QuestionClassify
from question_template import QuestionTemplate
import re


class Question:
    def __init__(self):
        self.classify = QuestionClassify()
        self.template = QuestionTemplate()
        with(open("./question/question_classification.txt", "r", encoding="utf-8")) as f:
            question_mode_list = f.readlines()
        self.question_mode_dict = {}
        for one_mode in question_mode_list:
            # 读取一行
            mode_id, mode_str = str(one_mode).strip().split(":")
            # 处理一行，并存入
            self.question_mode_dict[int(mode_id)] = str(mode_str).strip()
        # print(self.question_mode_dict)
        self.clean_question = self.question_flag = self.question_word = None
        self.answer = None

    def process(self, question):
        # 接收问题
        raw_question = str(question).strip()
        # 对问题进行词性标注
        labeled_question = self.label(raw_question)
        # 得到问题的模板
        question_template_id_str = self.get_question_template()
        # 查询图数据库,得到答案
        self.answer = self.query_template(labeled_question, question_template_id_str)
        return self.answer

    def label(self, raw):
        jb.load_userdict('./user-dic.txt')
        clean_question = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+", "", raw)
        self.clean_question = clean_question
        question_seged = posseg.cut(str(clean_question))
        question_word, question_flag, result = [], [], []
        for w in question_seged:
            temp_word = f"{w.word}/{w.flag}"
            result.append(temp_word)
            # 预处理问题
            word, flag = w.word, w.flag
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        assert len(question_flag) == len(question_word)
        self.question_word = question_word
        self.question_flag = question_flag
        print(result)
        return result

    def get_question_template(self):
        # 抽象问题
        for item in ['nr', 'nm', 'ng']:
            while item in self.question_flag:
                ix = self.question_flag.index(item)
                self.question_word[ix] = item
                self.question_flag[ix] = item + "ed"
        # 将问题转化字符串
        str_question = "".join(self.question_word)
        print("抽象问题为：", str_question)
        # 通过分类器获取问题模板编号
        question_template_num = self.classify.predict(str_question)
        print("使用模板编号：", question_template_num)
        question_template = self.question_mode_dict[question_template_num]
        print("问题模板：", question_template)
        question_template_id_str = str(question_template_num) + "\t" + question_template
        return question_template_id_str

    def query_template(self, labeled_question, question_template_id_str):
        print(labeled_question)
        print(question_template_id_str)
        # 调用问题模板类中的获取答案的方法
        try:
            answer = self.template.get_question_answer(labeled_question, question_template_id_str)
        except:
            answer = "呜呜呜我还不知道。"
        return answer


if __name__ == '__main__':
    q = Question()
    print(q.process('姜文导演过什么类型的电影'))
