import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")))
import re
from util.data import load_json
from extract.extract_utilts import JiebaCut, IsAllEnglishChar

"""
yeyuan 原被告姓名提取函数 v1.0
"""
def extract_plaintiff_defendant_list(data):
    ''' 提取原告被告名字信息'''
    plaintiffs = data["原告"].split("、")
    defendants  = data["被告"].split("、") #被告
    return list(plaintiffs), list(defendants)

# 测试函数功能
if __name__ == "__main__":
    from datapreprocess.openlaw_V0toV1 import Load_openlaw_data
    from util.path import path_data_faxin_v1_dir
    from tqdm import tqdm
    faxin_data_v1 = Load_openlaw_data(path_data_faxin_v1_dir)
    datas = []
    for name in faxin_data_v1:
        datas += faxin_data_v1[name].values()
    for data in tqdm(datas):
        plaintiffs, defendants = extract_plaintiff_defendant_list(data)
