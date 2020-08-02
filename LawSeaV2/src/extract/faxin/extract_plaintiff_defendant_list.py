import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")))
import re
from util.data import load_json
from extract.extract_utilts import JiebaCut, IsAllEnglishChar



"""
yeyuan 2020年6月15日 使用结巴分词器进行分词，同时针对原被告列表提取的特点，对分词结果进行后处理
"""
def GetWordList(Str, NewWords):
    """
    1. 结巴中文分词
    2. 针对原被告列表提取的特点，对分词结果进行后处理
    """
    WordList = JiebaCut(Str, "./tmp_data/CustomDict.txt", NewWords) # 结巴分词

    # 对分词结果进行后处理
    index = 0
    NewCutList = []
    while (index < len(WordList)):
        # 1. 将所有的英文单词合在一起, 例如外企的公司名
        if IsAllEnglishChar(WordList[index]):
            # 判断一个word是否全部都是英文字符，如果是循环找到连续的其他英文字符串，并合并为新的word
            index_j = index + 1
            while (index_j < len(WordList) and IsAllEnglishChar(WordList[index_j])):
                index_j += 1
            NewCutList.append(''.join(WordList[index:index_j]))
            index = index_j
        # 2. 将××和前面的词合在一起， 例如杨××
        elif index < len(WordList) - 1 and WordList[index + 1] == '×':
            # 判断一个词的后一个词是否是×，如果是循环找到连续的×，同时将当前词同×一起合并为一个新词：例如 杨××
            index_j = index + 1
            while (index_j < len(WordList) and WordList[index_j] == '×'):
                index_j += 1
            NewCutList.append(''.join(WordList[index:index_j]))
            index = index_j
        else:
            NewCutList.append(WordList[index])
            index += 1
    CutList = NewCutList
    return CutList

"""
yeyuan 处理文本中的\u3000
"""
def DealWithU3000(Str):
    # 处理文本中的\u3000
    if "\u3000" not in Str:
        return Str
    Chars = [chr(i) for i in range(ord("A"), ord("Z") + 1)] + [chr(i) for i in range(ord("a"), ord("z") + 1)]
    # 1. 将多个\u3000在一起的情况转变为一个
    if "\u3000\u3000" in Str:
        while ("\u3000\u3000" in Str):
            Str = Str.replace("\u3000\u3000", "\u3000")
    # 2. 如果\u3000出现在字符串前后，直接消去
    Str = Str.strip("\u3000")
    # 3. 如果\u3000前后均为英文单词的话，就转化为空格
    NewStr = []
    for i, w in enumerate(Str):
        if w == '\u3000' and Str[i - 1] in Chars and Str[i + 1] in Chars:
            NewStr.append(' ')
        else:
            NewStr.append(w)
    Str = "".join(NewStr)
    # 4. 如果\u3000出现的字符串中已经有冒号，则直接去掉\u3000
    if re.search(r"[:：]", Str) != None:
        Str = Str.replace("\u3000", "")
    # 5. 如果\u3000出现的字符串中没有冒号，则替换为冒号
    else:
        Str = Str.replace("\u3000", "：")
    return Str

"""
yeyuan 处理文本中的空格
"""
def DealWithSpace(Str):
    # 处理文本中的空格
    if " " not in Str:
        return Str
    Chars = [chr(i) for i in range(ord("A"), ord("Z") + 1)] + [chr(i) for i in range(ord("a"), ord("z") + 1)]
    # 1. 将多个空格在一起的情况转变为一个
    NewStr = []
    if "  " in Str:
        while ("  " in Str):
            Str = Str.replace("  ", " ")
    # 2. 去除首尾多余的空格
    Str = Str.strip(' ')
    # 3. 如果空格在两个中文字符之间，那么直接去掉
    for i, w in enumerate(Str):
        if w == ' ' and Str[i - 1] not in Chars and Str[i + 1] not in Chars:
            pass
        else:
            NewStr.append(w)
    Str = "".join(NewStr)
    return Str


"""
yeyuan 2020年6月13日 优化原被告姓名提取函数 v1.0
"""
def extract_plaintiff_defendant_list(data):
    ''' 提取原告被告名字信息'''
    text = data.get("当事人信息", "")
    plaintiffs = [] # 原告
    defendants  = [] # 被告
    TextList = re.split(r'[，。\n]', text)
    EndIndex = len(TextList)
    if re.search(r"(本案|一案|本院)", text) != None:
        # 将“本案、一案、本院”以后的内容删除
        for i, sent in enumerate(TextList):
            if re.search(r"(本案|一案|本院)", sent) != None:
                EndIndex = i # 到第一个发现“本案、一案、本院”的句子为止
                break

    def FindPlaintiffAndDefendant(begin, word_list):
        for word_index in range(begin, len(word_list)):
            if word_list[word_index] not in [":", "："]:
                if word_list[word_index] in ["（", "("]:
                    for tmp_index in range(word_index, len(word_list)):
                        if word_list[word_index] in ["）", ")"]:
                            return word_list[tmp_index+1]
                else:
                    return word_list[word_index]
        return ""

    NewWordList = re.split(r"[\n 。]", data.get("当事人", "").strip())
    for sent in TextList[:EndIndex]:
        # 提取原告、被告信息：
        if re.search(r"(原告|申请人|请求人|被告|被申请人|被请求人)", sent) != None:
            sent = DealWithU3000(sent) # 处理文本中的\u3000
            sent = DealWithSpace(sent) # 处理文本中的空格
            word_list = GetWordList(sent, NewWordList) # 结巴分词并进行后处理
            # 提取原告信息
            # 如果有很强的提示词比如原告：/原告: ，直接提取
            PlaintiffCueWords = ["原告：", "原告:", "请求人：", "请求人:", "申请人：", "申请人:",
                                 "原告（反诉被告）：", "原告（反诉被告）:", "原告(反诉被告)：", "原告(反诉被告):"]
            plaintiffsFlag = False
            for tmpWord in PlaintiffCueWords:
                if tmpWord in sent:
                    plaintiffs.append(sent.split(tmpWord)[1])
                    plaintiffsFlag = True
                    break
            if plaintiffsFlag == False:
                if "原告" in word_list:
                    tmpPlaintiff = FindPlaintiffAndDefendant(word_list.index("原告")+1, word_list)
                    plaintiffs.append(tmpPlaintiff)
                elif "请求人" in word_list:
                    tmpPlaintiff = FindPlaintiffAndDefendant(word_list.index("请求人") + 1, word_list)
                    plaintiffs.append(tmpPlaintiff)
                elif "申请人" in word_list:
                    tmpPlaintiff = FindPlaintiffAndDefendant(word_list.index("申请人") + 1, word_list)
                    plaintiffs.append(tmpPlaintiff)

            # 提取被告信息
            DefendantCueWords = ["被告：", "被告:", "被请求人：", "被请求人:", "被申请人：", "被申请人:",
                                 "被告（反诉原告）：", "被告（反诉原告）:", "被告(反诉原告)：", "被告(反诉原告):"]
            defendantsFlag = False
            for tmpWord in DefendantCueWords:
                if tmpWord in sent:
                    defendants.append(sent.split(tmpWord)[1])
                    defendantsFlag = True
                    break
            if defendantsFlag==False:
                if "被告" in word_list:
                    tmpDefendant = FindPlaintiffAndDefendant(word_list.index("被告")+1, word_list)
                    defendants.append(tmpDefendant)
                elif "被请求人" in word_list:
                    tmpDefendant = FindPlaintiffAndDefendant(word_list.index("被请求人") + 1, word_list)
                    defendants.append(tmpDefendant)
                elif "被申请人" in word_list:
                    tmpDefendant = FindPlaintiffAndDefendant(word_list.index("被申请人") + 1, word_list)
                    defendants.append(tmpDefendant)
    if plaintiffs==[] or defendants==[]:  # TODO 使用分词结果来辅助识别原被告名字
        pass
    # 最后对所有的原被告信息还需要做一个后处理 TODO 学习一个二分类器来判别是否是原告、被告姓名
    plaintiffs = set(plaintiffs) # 处理重复的内容
    defendants = set(defendants)
    StopWords = set(load_json("./tmp_data/PlaintiffDefendantStopWords.json"))
    # 去除停用词，集合差集
    plaintiffs = plaintiffs - StopWords
    defendants = defendants - StopWords
    return list(plaintiffs), list(defendants)

# 测试函数功能
if __name__ == "__main__":
    from datapreprocess.faxin_v0_v1 import Load_faxin_data
    from util.path import path_data_faxin_v1_dir
    from tqdm import tqdm
    faxin_data_v1 = Load_faxin_data(path_data_faxin_v1_dir)
    datas = []
    for name in faxin_data_v1:
        datas += faxin_data_v1[name].values()
    for data in tqdm(datas):
        plaintiffs, defendants = extract_plaintiff_defendant_list(data)
