import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")))
import re


"""
lzc优化被告辩称抽取函数2.0
"""
def extract_defendant_evidence(data, defendant=None):
    ''' 提取被告证据 '''
    evidences = []
    if data['ID'] == 25:
        print('!')
    for key in ['庭审过程']:
        if key in data:
            text = data[key]
            sents = [sent for sent in re.split(r'。、', text) if sent]

            for i, sent in enumerate(sents):
                if sent.startswith('被告') and ("证据" in sent or '举证' in sent) and ':' in sent and '本院查明' not in sent and '质证' not in sent and '原告证据' not in sent and '没有' not in sent and '未' not in sent and '放弃' not in sent:
                    j = sent.find(':')
                    evidences += [s for s in re.split("[；。;]", sent[j + 1:]) if s]

                    k = i + 1

                    while k < len(sents) and sents[k]:
                        if sents[k][0] in '1一⑴' or '质证' in sents[k]:
                            break

                        if sents[k][0] in '23456789二三四五六七八九⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇' and ('证据' in  sents[k] or '证明' in sents[k]):
                            evidences.append(sents[k])

                        k += 1

    return evidences


def extract_defendant_argues(data, defendant=None):
    argues = []
    for key in ["庭审过程"]:
        if key in data:
            # if data['ID'] == 'class1_id849':
            #     print('!')
            text = data[key].strip()
            sents = [sent for sent in re.split(r'。、', text) if sent]

            for i, sent in enumerate(sents):
                if sent.startswith('被告') and '辩称' in sent and ('：' in sent or ':' in sent or '，' in sent):
                    j = min(filter(lambda x: x > -1, [sent.find(':'), sent.find('：'), sent.find('，')]))

                    if sent[j + 1] not in "123456789一二三四五六七八九⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇":
                        argues.append(sent[j + 1:])
                    elif sent[j + 1] in "123456789一二三四五六七八九⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇" and ';' not in sent and '；' not in sent:
                        argues.append(sent[j + 1:])
                        k = i + 1

                        while k < len(sents) and sents[k]:
                            if sents[k][0] in '1一⑴':
                                break

                            if sents[k][0] in '23456789二三四五六七八九⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇':
                                argues.append(sents[k])

                            k += 1
                    elif sent[j + 1] in "123456789一二三四五六七八九⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇" and (';' in sent or '；' in sent):
                        argues += [s for s in re.split("[；。;]", sent[j + 1:]) if s]
    return argues