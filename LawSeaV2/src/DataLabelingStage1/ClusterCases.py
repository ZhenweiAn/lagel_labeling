import jieba
import codecs
import json
from collections import defaultdict
from util.data import *
from tqdm import tqdm
from DataLabelingStage1.data_labelling_util import merge_data

def cluster(datas, extracted_datas):
    d = defaultdict(int)
    keys_list = list(datas.keys()) # 对keys排个序？
    result = []
    s = dict()

    # for key in keys_list:
    #     s[key] = set(jieba.cut(datas[key]['标题']))

    for i in tqdm(range(len(keys_list))):
        if d[keys_list[i]] == 1:
            continue
        d[keys_list[i]] = 1
        plaintiff1 = set(extracted_datas[keys_list[i]]["原告"]["原告列表"])
        defendant1 = set(extracted_datas[keys_list[i]]["被告"]["被告列表"])
        # mergeList = [(datas[keys_list[i]]['ID'], datas[keys_list[i]]['标题'], extracted_datas[keys_list[i]]["原告"]["原告列表"], extracted_datas[keys_list[i]]["被告"]["被告列表"])]
        mergeList = [datas[keys_list[i]]['ID']]
        for j in range(i + 1, len(keys_list)):
            if d[keys_list[j]] == 1:
                continue
            plaintiff2 = set(extracted_datas[keys_list[j]]["原告"]["原告列表"])
            defendant2 = set(extracted_datas[keys_list[j]]["被告"]["被告列表"])
            if (plaintiff1==plaintiff2 and len(plaintiff1)!=0) or (defendant1==defendant2 and len(defendant1)!=0):
                # mergeList.append((datas[keys_list[j]]['ID'], datas[keys_list[j]]['标题'], extracted_datas[keys_list[j]]["原告"]["原告列表"], extracted_datas[keys_list[j]]["被告"]["被告列表"]))
                mergeList.append(datas[keys_list[j]]['ID'])
                d[keys_list[j]] = 1
        result.append(mergeList)
    print(len(result))
    return result



if __name__ == '__main__':
    faxin_datas = Load_faxin_data(path_data_faxin_v1_dir)
    faxin_extracted_datas = load_json("../../data/extract/stage1/法信_抽取.json")
    openlaw_datas = Load_openlaw_data(path_data_openlaw_v1_dir)
    openlaw_extracted_datas = load_json("../../data/extract/stage1/Openlaw_抽取.json")
    datas = merge_data(faxin_datas, openlaw_datas)
    extracted_datas = merge_data(faxin_extracted_datas, openlaw_extracted_datas)
    result = cluster(datas, extracted_datas)

    with codecs.open('merge.json', 'w', encoding='utf8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
