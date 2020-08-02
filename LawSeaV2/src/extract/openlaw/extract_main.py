import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")))

import traceback
from tqdm import tqdm
from util.path import path_data_openlaw_v1_dir, path_extract_stage_1
from util.data import load_json, dump_json, Load_openlaw_data, Openlaw_ClassDict

from extract.openlaw.extract_plaintiff import extract_plaintiff_evidence, extract_plaintiff_request
from extract.openlaw.extract_defendant import extract_defendant_argues, extract_defendant_evidence
from extract.openlaw.extract_judge import extract_article, extract_verdict, extract_dispute_focus
from extract.openlaw.extract_plaintiff_defendant_list import extract_plaintiff_defendant_list


def extract_stage_1():
    '''
        第一阶段抽取
        步骤：
            1、 抽取原告被告
            1、 原告被告案情分配
            2、 证据、诉求、相关法律
    '''

    """
    yeyuan 数据加载，数据格式变为 {ID1:data1, ID2:data2} 的字典存储格式（详细见 ../datapreprocess/openlaw_V0toV1.py）
    """
    openlaw_data_v1 = Load_openlaw_data(path_data_openlaw_v1_dir)
    datas = []
    for name in openlaw_data_v1:
        datas += openlaw_data_v1[name].values()
    jdatas = {name:{} for name in Openlaw_ClassDict}
    FocusCount = 0
    EmptyCount = 0
    for data in tqdm(datas):
        try:
            # ---- 原被告列表----
            plaintiffs, defendants = extract_plaintiff_defendant_list(data)
            if plaintiffs==[] or defendants==[]:
                EmptyCount += 1
            # ---- 原告: 诉求、证据 ----
            plaintiffs_requests  = extract_plaintiff_request(data)
            plaintiffs_evidences = extract_plaintiff_evidence(data)

            # ---- 被告: 辩称、证据 ----
            defendant_argues = extract_defendant_argues(data)
            defendant_evidences = extract_defendant_evidence(data)

            # ---- 法院: 证据、审判结果、法律 ----
            articles = extract_article(data) # 法条
            verdicts = extract_verdict(data) # 法院审判结果

            # ----争议焦点----
            DisputeFocus = extract_dispute_focus(data)
            if DisputeFocus!=[]:
                FocusCount += 1
            jdata = {"ID": data.get("ID", None),
                     "原告":{"原告列表": plaintiffs, "原告证据": plaintiffs_evidences, "原告诉求": plaintiffs_requests},
                     "被告":{"被告列表": defendants, "被告证据": defendant_evidences, "被告辩称": defendant_argues},
                     "法院":{"法院证据":[], "审判结果": verdicts,"法条": articles, "争议焦点": DisputeFocus}}
            jdatas[jdata["ID"].split('_')[0]][jdata["ID"]] = jdata

        except Exception as e:
            traceback.print_exc()
    print(len(datas), FocusCount)
    print(EmptyCount)
    dump_json(jdatas, os.path.join(path_extract_stage_1, "Openlaw_抽取.json"))

if __name__ == "__main__":
    extract_stage_1()