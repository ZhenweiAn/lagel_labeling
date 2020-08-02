import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")))
import re


"""
lzc优化被告辩称抽取函数2.0
"""
def extract_defendant_argues(data, defendant=None):
    argues = []
    for key in ["被告辩称"]:
        if key in data:
            # if data['ID'] == 'class1_id849':
            #     print('!')
            text = data[key]
            sents = [sent for sent in re.split(r'\n', text) if sent]
            if sents[0].startswith('被告') and ('反诉称：' in sents[0] or '书面答辩，' in sents[0]) and '口头答辩称：' not in sents[0] and '未提供' not in sents[0] and '提供证据' not in sents[0]:
                argues += [s for s in re.split("[；。]", sents[0]) if s]
                sents = sents[1:]
            for i, sent in enumerate(sents):
                if sent.startswith('被告') and "辩称" in sent and "：" in sent and sent[-1] != '：':
                    index = sent.index('：')
                    argue = sent[index + 1:]
                    argues += [s for s in re.split("[；。]", argue) if s]
                elif sent.startswith('被告') and "答辩意见：" in sent and sent[-1] != '：':
                    index = sent.index('：')
                    argue = sent[index + 1:]
                    argues += [s for s in re.split("[；。]", argue) if s]
                elif sent.startswith('被告') and ('辩称：' in sent or '辩称:' in sent) and (sent[-1] == '：' or sent[-1] == ':'):
                    j = i + 1
                    if sents[j] and sents[j][0] not in "123456789一二三四五六七八九":
                        argues += [s for s in re.split("[；。]", sents[j]) if s]
                    elif sents[j] and sents[j][0] in "123456789一二三四五六七八九":
                        while j < len(sents) and sents[j] and (sents[j][0] in "123456789一二三四五六七八九" or sents[j][:2] == "证据"):
                            argues += [s for s in re.split("[；。]", sents[j]) if s]
                            j += 1
                elif sent.startswith('被告') and ("辩称" in sent or '被告答辩' in sent) and "，" in sent:
                    index = sent.index('，')
                    argue = sent[index + 1:]
                    argues += [s for s in re.split("[；。]", argue) if s]
                elif sent.startswith('被告') and '管辖权' in sent and '异议' in sent:
                    argues += [s for s in re.split("[；。]", sent) if s]

    return argues


"""
lzc优化被告证据抽取函数2.0
"""
def extract_defendant_evidence(data, defendant=None):
    ''' 提取被告证据 '''
    evidences = []
    for key in ["被告辩称", '本院认为']:
        if key in data:
            text = data[key]
            sents = [sent for sent in re.split(r'\n', text) if sent]
            for i, sent in enumerate(sents):
                if sent.startswith('被告') and ("证据" in sent or '举证' in sent) and sent[-1] == "：" and '原告证据' not in sent and '没有' not in sent and '未' not in sent and '放弃' not in sent:
                    j = i + 1
                    while j < len(sents) and sents[j] and (sents[j][0] in "123456789一二三四五六七八九" or (sents[j][:2] == "证据" and sents[j][2] in "123456789一二三四五六七八九")):
                        evidences.append(sents[j])
                        j += 1
                    break
                ss = [s for s in re.split(r'。', sent) if s]
                for s in ss:
                    if s.startswith("被告") and ("为支持其答辩意见" in s or '用以证明' in s or '用来证明' in s) and s[-1] != "：":
                        evidences.append(s)
    return evidences