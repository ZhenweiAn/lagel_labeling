import re
import jieba

"""
yeyuan 句子划分辅助函数 2020年6月15日
"""
def cut_sent(para):
    para = re.sub('([。！？?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？?][”’])([^，。！？?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")
def Str_preprocess(Str): # 将一段话划分为句子
    # 替换冗余字符、错误字符
    new_str = Str.replace('\n', ' ')
    new_str = new_str.replace('\t', ' ')
    new_str = new_str.replace('\u3000\u3000', ' ')
    new_str = new_str.replace('\u3000', '')
    result = cut_sent(new_str) # 分句
    return result

"""
yeyuan 2020年6月15日 调用Jieba实现一个简单的中文分词器
"""
def JiebaCut(Str, dict_path, NewWords):
    """
    使用结巴分词对中文进行分词，返回分词的List的结果。
    可以从文件../../data/CustomDict.txt中读取新词，也可以通过new_word_list动态的添加新词
    """
    jieba.load_userdict(dict_path) # load CustomDict.txt 字典
    for word in NewWords:
        jieba.add_word(word) # 将new_word_list中的新词加入到字典中
    CutList = jieba.lcut(Str) # 分词
    for word in NewWords:
        jieba.del_word(word) # 将new_word_list中的新词从字典中删除
    return CutList

"""
yeyuan 判断字符串中的所有字符是否是英文或者常用英文符号
"""
def IsAllEnglishChar(Str):
    # 判断字符串中的所有字符是否是英文或者常用英文符号
    Chars = [chr(i) for i in range(ord("A"), ord("Z") + 1)] \
            + [chr(i) for i in range(ord("a"), ord("z") + 1)] \
            + list(",.';:-_ ")
    return set(Str) & set(Chars) == set(Str)


"""
yeyuan 2020年6月15日 调用HanNLP对一个字符串进行命名实体识别标注
"""
def NER(Str):
    import jpype
    pass

def gen_alias(company):
    ''' 生成公司别名 '''
    alias = [company]
    # 去地名
    company = re.split(r'[省市县镇村乡]', company)[-1]
    alias.append(company)
    # 去“有限”
    company = company.replace("有限", "")
    alias.append(company)
    return alias

def description_allocation(data, people):
    ''' 将案情描述部分分配至当事人 '''
    descrip_for_people = {}
    for person in people:
        descrip_for_people[person] = {"审理经过": [], "原告诉称": [], "被告辩称": [], "裁判结果": []}
    for item in ["审理经过", "原告诉称", "被告辩称", "裁判结果"]:
        if item not in data:
            continue
        for text in re.split(r'[；。\n]', data[item]):
            for person in people:
                if "公司" in person:
                    for alias in gen_alias(person):
                        if alias in text:
                            descrip_for_people[person][item].append(text)
                            break
                if person in text:
                    descrip_for_people[person][item].append(text)
    return descrip_for_people