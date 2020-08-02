import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")))

import re
from extract.extract_utilts import Str_preprocess

"""
yeyuan 争议焦点抽取-v1.0 2020年6月15日
"""
def extract_dispute_focus(data):
    '''抽取争议焦点'''
    FoucsSent = []
    for key in data:
        SentList = Str_preprocess(str(data[key]))
        for sent in SentList:
            if "争议焦点" in sent:
                FoucsSent.append(sent)
    return FoucsSent

def extract_verdict(data):
    ''' 提起裁判结果 '''
    verdicts = []
    for key in ["裁判结果"]:
        if key in data:
            text = data[key]
            sents = [sent for sent in re.split(r'[；。\n]', text) if sent]
            for i, sent in enumerate(sents):
                verdicts.append(sent)
    return verdicts

def extract_article(data):
    ''' 抽取法条 '''
    if "相关法条" in data:
        return data["相关法条"]
    laws = set()
    for key in ["本院认为", "审理经过", "附"]:
        if key in data:
            laws |= set(re.findall(r"《.*法》", data[key]))
    return list(laws)
