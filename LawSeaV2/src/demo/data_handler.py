import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

from util.data import *
from util.path import *
from demo.es_api_wrapper import *

# ============= function ================

def filter_datas_raw():
    ''' 选择数据，并根据key做预处理 '''
    datas_faxin   = load_faxin_data0410() 
    datas_openlaw = load_openlaw_data0410() 

    datas_selected = []
    for data in datas_faxin:
        data = dict_to_defaultdict(data, str)
        selected = {}
        selected["来源"] = "法信"
        selected["标题"] = data["标题"]
        selected["案由"] = data["案由"]
        selected["案号"] = data["案号"]
        selected["当事人"] = data["当事人"]
        selected["书记员"] = data["书记员"]
        selected["审判员"] = "\n".join([data["审判人员"], data["裁判人员"]])
        selected["审理法院"] = data["审理法院"]
        selected["庭审过程"] = "\n".join([data["审理经过"], data["原告诉称"], data["被告辩称"], data["第三人辩称"]]) 
        selected["法院意见"] = "\n".join([data["本院查明"], data["本院认为"]])
        selected["判决结果"] = data["裁判结果"]
        datas_selected.append(selected)

    for data in datas_openlaw:
        data = dict_to_defaultdict(data, str)
        selected = {}
        selected["来源"] = "openlaw"
        selected["标题"] = data["标题"]
        selected["案由"] = data["案由"]
        selected["案号"] = data["案号"]
        selected["当事人"] = data["当事人"]
        selected["书记员"] = data["书记员"]
        selected["审判员"] = "\n".join([data["法官"], data["审判长"], data["审判员"]])
        selected["审理法院"] = data["法院"]
        selected["庭审过程"] = "\n".join([data["庭审过程"], data["庭审过程2"], data["庭审过程3"], data["庭审过程4"], data["庭审过程5"], data["庭审过程6"], data["庭审程序说明"], data["庭审程序说明2"]]) 
        selected["法院意见"] = "\n".join([data["法院意见"], data["法院意见2"]])
        selected["判决结果"] = "\n".join([data["判决结果"], data["判决结果2"]])
        datas_selected.append(selected)

    return datas_selected


def filter_datas_tag():
    ''' 读取标注过后的数据 '''

    tag_field = ["船员雇主基本属性", "劳务合同形式", "劳务关系存在的证明", "工资标准的约定", "应付劳务报酬和费用", "已经支付工资的证明", "船员在船工作及工作时间的证明", "争议解决方式的约定", "诉讼请求" , "法律依据"]

    datas_selected = []
    # 合并法信数据
    datas_faxin = {}
    paths_faxin = [path_data_rule_tag_faxin_1, path_data_rule_tag_faxin_2, path_data_rule_tag_faxin_3, path_data_rule_tag_faxin_4_1, path_data_rule_tag_faxin_4_2]
    for filepath in paths_faxin:
        datas = load_json(filepath)
        for data in datas:
            ID = str(data["ID"])
            # 第一次见
            if ID not in datas_faxin:
                datas_faxin[ID] = {}
                for k, v in data.items():
                    if type(v) == dict:
                        lst = [vk for vk, vv in v.items() if vv == True]
                        datas_faxin[ID][k] = lst
                    else:
                        datas_faxin[ID][k] = v
            # 增量加
            else:
                for k, v in data.items():
                    if k not in datas_faxin[ID]:
                        if type(v) == dict:
                            lst = [vk for vk, vv in v.items() if vv == True]
                            datas_faxin[ID][k] = lst
                        else:
                            datas_faxin[ID][k] = v
    for _, data in datas_faxin.items():
        data = dict_to_defaultdict(data, str)
        selected = {}
        selected["来源"] = "法信"
        selected["标题"] = data["标题"]
        selected["案由"] = data["案由"]
        selected["案号"] = data["案号"]
        selected["当事人"] = data["当事人"]
        selected["书记员"] = data["书记员"]
        selected["审判员"] = "\n".join([data["审判人员"], data["裁判人员"]])
        selected["审理法院"] = data["审理法院"]
        selected["庭审过程"] = "\n".join([data["审理经过"], data["原告诉称"], data["被告辩称"], data["第三人辩称"]]) 
        selected["法院意见"] = "\n".join([data["本院查明"], data["本院认为"]])
        selected["判决结果"] = data["裁判结果"]
        for field in tag_field:
            selected[field] = "\n".join(data[field])
        datas_selected.append(selected)


    # 合并openlaw数据
    datas_openlaw = {}
    paths_openlaw = [path_data_rule_tag_openlaw_1, path_data_rule_tag_openlaw_2, path_data_rule_tag_openlaw_3, path_data_rule_tag_openlaw_4]
    for filepath in paths_openlaw:
        datas = load_json(filepath)
        for data in datas:
            ID = str(data["ID"])
            # 第一次见
            if ID not in datas_openlaw:
                datas_openlaw[ID] = {}
                for k, v in data.items():
                    if type(v) == dict:
                        lst = [vk for vk, vv in v.items() if vv == True]
                        datas_openlaw[ID][k] = lst
                    else:
                        datas_openlaw[ID][k] = v
            # 增量加
            else:
                for k, v in data.items():
                    if k not in datas_openlaw[ID]:
                        if type(v) == dict:
                            lst = [vk for vk, vv in v.items() if vv == True]
                            datas_openlaw[ID][k] = lst
                        else:
                            datas_openlaw[ID][k] = v
    for _, data in datas_openlaw.items():
        data = dict_to_defaultdict(data, str)
        selected = {}
        selected["来源"] = "openlaw"
        selected["标题"] = data["标题"]
        selected["案由"] = data["案由"]
        selected["案号"] = data["案号"]
        selected["当事人"] = data["当事人"]
        selected["书记员"] = data["书记员"]
        selected["审判员"] = "\n".join([data["法官"], data["审判长"], data["审判员"]])
        selected["审理法院"] = data["法院"]
        selected["庭审过程"] = "\n".join([data["庭审过程"], data["庭审过程2"], data["庭审过程3"], data["庭审过程4"], data["庭审过程5"], data["庭审过程6"], data["庭审程序说明"], data["庭审程序说明2"]]) 
        selected["法院意见"] = "\n".join([data["法院意见"], data["法院意见2"]])
        selected["判决结果"] = "\n".join([data["判决结果"], data["判决结果2"]])
        for field in tag_field:
            selected[field] = "\n".join(data[field])
        datas_selected.append(selected)

    return datas_selected



# ============== process ================

def build_es():
    ''' 将文书数据导入ES '''
    res = delete_index("law")

    print("loading ... ")
    datas = filter_datas_tag() + filter_datas_raw()

    print("adding data to es ...")
    res = create_index("law", datas[0].keys())
    print(res)
    for i, data in enumerate(tqdm(datas)):
        res = insert_record("law", str(i), data)

    show_indices()


# =============== main ==================

def main():
    build_es()

if __name__ == '__main__':
    main()