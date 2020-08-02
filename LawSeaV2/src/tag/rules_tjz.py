import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

import re

from util.path import *
from util.data import *

'''
需要找：

1. 船员雇主基本属性： 
    自然人、法人、其他

2. 工资标准的约定：
    月工资、年薪、人民币、美元、基础工资、工龄工资、技能工资、补助、其他

'''


# ================ function =============

def d_or(dict1, dict2):
    ''' 合并两个value为布尔型的字典 '''
    ret = {}
    for key in dict1:
        if key in dict2:
            ret[key] = dict1[key] or dict2[key]
        else:
            ret[key] = dict1[key]
    for key in dict2:
        if key not in dict1:
            ret[key] = dict2[key]
    return ret

def CYGZJBSX(s, ret_type=list):
    ''' 船员雇主基本属性 '''
    s = s.replace("\n", "").replace("\t", "")
    ret = {"自然人": False, "法人": False, "其他": False}
    if "公司" in s:
        ret["法人"] = True
    else:
        ret["自然人"] = True 
    if ret_type == list:
        ret = [key for key in ret if ret[key]]
    ret = {"船员雇主基本属性": ret}
    return ret


def GZBZDYD(s, ret_type=list):
    ''' 工资标准的约定，对应字段庭审过程 '''
    s = s.replace("\n", "").replace("\t", "")
    ret = {
        "月工资":  False,
        "年薪":    False,
        "人民币":  False,
        "美元":    False,
        "基础工资": False,
        "技能工资": False,
        "补助":    False,
        "其他":    False
    }
    # 直接匹配
    keywords = ["月工资","年薪","人民币","美元","基础工资","技能工资","补助"]
    for word in keywords:
        if word in s:
            ret[word] = True
    # 正则表达式匹配
    patterns_re = {
        "月工资":   [r"月薪", r"每月.*\d+[百千万]*[美]*元", r"\d+[百千万]*[美]*元/月"],
        "年薪":     [r"年工资", r"每年.*\d+[百千万]*[美]*元", r"\d+[百千万]*[美]*元/年"],
        "人民币":   [r"\d+[百千万]*元"],
        "美元":     [],
        "基础工资": [r"基本工资", r"保底工资"],
        "技能工资": [],
        "补助":     [r"补贴"],
        "其他":     []
    }
    for key, patterns in patterns_re.items():
        if not ret[key]:
            for pattern in patterns:
                if re.search(pattern, s):
                    ret[key] = True 
    if ret_type == list:
        ret = [key for key in ret if ret[key]]
    ret = {"工资标准的约定": ret}
    return ret
    


# ================ process =============

def tagging_process():
    ''' 标注整个过程 '''

    ######################################
    #               openlaw              #
    ######################################
    datas_openlaw = load_json(path_openlaw_laowu)
    no_tag_datas = []
    for i in range(len(datas_openlaw)):
        # 船员雇主基本属性
        cygzjbsx = CYGZJBSX(datas_openlaw[i]["被告"])
        datas_openlaw[i]["船员雇主基本属性"] = cygzjbsx
        
        # 工资标准的约定
        gzbzdyd = {}
        for key, s in datas_openlaw[i].items():
            if key.startswith("庭审") or key.startswith("法院"):
                gzbzdyd = d_or(gzbzdyd, GZBZDYD(s))
        datas_openlaw[i]["工资标准的约定"] = gzbzdyd
        if gzbzdyd["其他"]:
            no_tag_datas.append(datas_openlaw[i])
    
    # 生成临时文件检查
    # txts = []
    # for data in no_tag_datas:
    #     for key, s in data.items():
    #         if key.startswith("庭审") or key.startswith("法院"):
    #             txts.append(s)
    # dump_str_lst(txts, os.path.join(path_data_tmp_dir, "no_tag.txt"))

    # save
    path_openlaw_tag = os.path.join(path_data_rule_tag_dir, "openlaw_laowu.json")
    dump_json(datas_openlaw, path_openlaw_tag)

    #####################################
    #                  法信             #
    #####################################
    datas_faxin = load_json(path_faxin_laowu)
    no_tag_datas = []
    for i in range(len(datas_faxin)):
        # 船员雇主基本属性
        if "当事人" in datas_faxin[i]:
            cygzjbsx = CYGZJBSX(datas_faxin[i]["当事人"])
        elif "当事人信息" in datas_faxin[i]:
            cygzjbsx = CYGZJBSX(datas_faxin[i]["当事人信息"])
        elif "原始文件" in datas_faxin[i]:
            cygzjbsx = CYGZJBSX(datas_faxin[i]["原始文件"])
        datas_faxin[i]["船员雇主基本属性"] = cygzjbsx


        # 工资标准的约定
        gzbzdyd = {}
        for key, s in datas_faxin[i].items():
            if key.startswith("原告") or key.startswith("被告") or key.startswith("本院") or key.startswith("审理"):
                gzbzdyd = d_or(gzbzdyd, GZBZDYD(s))
        datas_faxin[i]["工资标准的约定"] = gzbzdyd
        if not gzbzdyd["月工资"]:
            no_tag_datas.append(datas_faxin[i])

    # 生成临时文件检查
    # txts = []
    # for data in no_tag_datas:
    #     for key, s in data.items():
    #         if key.startswith("原告") or key.startswith("被告") or key.startswith("本院"):
    #             txts.append(s)
    # dump_str_lst(txts, os.path.join(path_data_tmp_dir, "no_tag.txt"))

    # save
    path_faxin_tag = os.path.join(path_data_rule_tag_dir, "faxin_laowu.json")
    dump_json(datas_faxin, path_faxin_tag)


def view_data():
    datas_openlaw = load_json(path_openlaw_laowu)
    keys = set()
    for data in datas_openlaw:
        keys.update(data.keys())
    for key in keys:
        print(key)

# ================= main ================

def main():
    # view_data()
    tagging_process()

if __name__ == '__main__':
    # main()

    des = "原告张标为与被告王玉龙、被告安徽省怀远县远洋航运有限公司(以下简称“远洋航运公司”)船员劳务合同纠纷一案，于2019年1月10日向本院提起诉讼，本院于同日立案受理。在此之前，本院在执行(2018)沪72执恢2号案件过程中，依法扣押并拍卖了登记在被告远洋航运公司名下的“中海18”轮，原告张标向本院进行了债权登记，后提起本案确权诉讼。审理中，案外人鞠某某于2019年1月17日向本院提出申请，认为本案处理结果与其有法律上的利害关系，请求作为第三人参加本案诉讼。本院经审查后，于2019年2月13日作出参加诉讼通知书，通知鞠某某作为无独立请求权的第三人参加本案诉讼。2019年2月27日，本院依法适用确权程序公开开庭审理本案。原告委托代理人贾冲冲、被告王玉龙、被告远洋航运公司委托代理人侯建武、第三人鞠某某委托代理人岳洪武到庭参加诉讼。本案现已审理终结。"
    d1 = CYGZJBSX(des)
    print(d1)
    d2 = GZBZDYD(des)
    print(d2)