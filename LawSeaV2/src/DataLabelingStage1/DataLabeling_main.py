# _*_coding=utf-8_*_
# 数据标注系统数据准备相关代码
# 1. 找到抽取质量比较高的数据
import json, codecs
from util.data import load_json, dump_json, Load_faxin_data, Load_openlaw_data
from util.path import path_data_faxin_v1_dir, path_data_openlaw_v1_dir
from DataLabelingStage1.data_labelling_util import merge_data
from DataLabelingStage1.ClusterCases import cluster

# def ChangeID():
#     IDList = load_json("lzc_defendant_high_quality.json")
#     NewIDList = []
#     for ID in IDList:
#         if str(ID).startswith("class"):
#             NewIDList.append(str(ID).replace("class", "FaxinClass"))
#         else:
#             NewIDList.append("FaxinClass3_id"+str(ID))
#     dump_json(NewIDList, "lzc_xiugai.json")
# ChangeID()
def score_function(data):
    # 根据抽取到的数据数目给每个案件打分：<原告诉求1分、原告证据1分、被告辩称1分、被告证据1分、审判结果1分、争议焦点3分>
    Score = 0.0
    if data["原告"]["原告诉求"]!=[]:
        Score += 1
    if data["原告"]["原告证据"] != []:
        Score += 1
    if data["被告"]["被告辩称"] != []:
        Score += 1
    if data["被告"]["被告证据"] != []:
        Score += 1
    if data["法院"]["审判结果"] != []:
        Score += 1
    if data["法院"]["争议焦点"] != []:
        Score += 3
    return Score

def ordering_extractions(extracted_datas):
    # 根据抽取到的数据数目给每个案件打分：<原告诉求1分、原告证据1分、被告辩称1分、被告证据1分、审判结果1分、争议焦点3分>
    score_dict = {}
    for key in extracted_datas:
        score_dict[key] = score_function(extracted_datas[key])
    sorted_list = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_list

def filter_function(high_quality_ordered_list, case_clusters):
    flag_dict = {}
    result_list = []
    for t in high_quality_ordered_list:
        flag_dict[t[0]] = 0
    for t in high_quality_ordered_list:
        if flag_dict[t[0]] == 1:
            continue
        else:
            result_list.append(t[0])
            for cluster in case_clusters:
                if t[0] in cluster:
                    for id in cluster:
                        flag_dict[id] = 1
                    break
    return result_list

if __name__=="__main__":
    faxin_datas = Load_faxin_data(path_data_faxin_v1_dir)
    faxin_extracted_datas = load_json("../../data/extract/stage1/法信_抽取.json")
    openlaw_datas = Load_openlaw_data(path_data_openlaw_v1_dir)
    openlaw_extracted_datas = load_json("../../data/extract/stage1/Openlaw_抽取.json")
    datas = merge_data(faxin_datas, openlaw_datas)
    extracted_datas = merge_data(faxin_extracted_datas, openlaw_extracted_datas)
    high_quality_ordered_list = ordering_extractions(extracted_datas)
    case_clusters = cluster(datas, extracted_datas)
    # 通过case_clusters信息排除掉一些内容
    result_list = filter_function(high_quality_ordered_list, case_clusters)
    with codecs.open('result_list.json', 'w', encoding='utf8') as f:
        json.dump(result_list, f, indent=2, ensure_ascii=False)