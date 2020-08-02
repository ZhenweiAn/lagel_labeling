import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")))
import re

"""
yeyuan 处理 原告诉称 中的文本
"""
def CleanYuanGaoSuChen(Str):
    # 清洗 原告诉称 中的文本信息，帮助获取 原告诉求
    Str = Str.split("相关法律条文")[0]
    return re.split(r"[。\n]", Str)

"""
yeyuan 处理 审理经过 中的文本
"""
def CleanShenLiJingGuo(Str):
    # 清洗 审理经过 中的文本信息，帮助获取 原告诉求
    Str = Str.split("相关法律条文")[0]
    return re.split(r"[。\n]", Str)

"""
yeyuan 优化原告诉求抽取函数1.0
"""
def extract_plaintiff_request(data):
    '''
    提取原告请求--yeyuan--
    关键字信息：申请、请求
    '''
    TextList = CleanYuanGaoSuChen(data.get("原告诉称", "")) + CleanShenLiJingGuo(data.get("审理经过", ""))
    requests = []
    for sent in TextList:
        if "请求" in sent or "申请" in sent:
            if "：" in sent:
                sent = sent.split("：")[1]
                requests += sent.split("；")
            else:
                sent = sent.split("，")
                for i, tmp_span in enumerate(sent):
                    if "请求" in tmp_span or "申请" in tmp_span:
                        requests += sent[i:]
                        break
            break  # TODO 如果抽取所有出现请求的短句的话，需要一个分类器来筛除那些不是诉求的短句
    # print(data["ID"], requests)
    return requests

"""
yeyuan 优化原告证据抽取函数1.0
"""
def extract_plaintiff_evidence(data):
    ''' 提取原告证据 '''
    evidences = []
    for key in ["审理经过","原告诉称","被告辩称","原始文件","附"]:
        if key in data:
            text = data[key]
            sents = [sent for sent in re.split(r'[；。\n]', text) if sent]
            for i, sent in enumerate(sents):
                if ("原告" in sent) and "证据" in sent and sent[-1] == "：":
                    j = i + 1
                    while j < len(sents) and (sents[j][0] in "123456789一二三四五六七八九" or sents[j][:2] == "证据"):
                        evidences.append(sents[j])
                        j += 1
                    break
    return evidences

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
        plaintiffs_requests = extract_plaintiff_request(data)
        plaintiffs_evidences = extract_plaintiff_evidence(data)
