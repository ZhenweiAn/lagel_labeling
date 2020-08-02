# _*_coding=utf-8_*_
# 数据预处理程序，预处理openlaw的数据，从V0版本的数据修改为V1版本的数据

import os, json, re
from util.data import Openlaw_ClassDict, Load_openlaw_data, Dump_openlaw_data, load_json, dump_json
from util.path import path_data_openlaw_v0_dir, path_data_openlaw_v1_dir

###############################################################################
############################打印查看信息的辅助函数#############################
###############################################################################

def PrintTitle(Datas):
    for name in Openlaw_ClassDict:
        for key in Datas[name]:
            if re.search(r"(裁定书|移送函|判决书|纠纷案|民事决定书)(（.*）)*", Datas[key]["标题"].strip())!=None:
            # if re.match(r".*(民事决定书)(（.*）)*", Datas[key]["标题"].strip())!=None:
            #     print(key, Datas[key]["标题"])
                pass
            elif re.search(r"案$", Datas[key]["标题"].strip())!=None:
                # print(key, Datas[key]["标题"])
                pass
            else:
                print(key, Datas[key]["标题"])
                pass

def PrintCase(ID_list, Datas):
    # 打印ID_list中对应的所有案例的数据
    for ID in ID_list:
        if ID in Datas[ID.split("_")[0]]:
            print(json.dumps(Datas[ID.split("_")[0]][ID], ensure_ascii=False, indent=4, sort_keys=True))
            # print("########################################################")
            # print(ID)
            # print(Datas[ID.split("_")[0]][ID]["原始文件"])
            # print("########################################################")
        else:
            print("Case %s is not existing!!!" %(ID))

###############################################################################
##############################修改数据的函数###################################
###############################################################################
"""
def AddIDInfo(InPath, OutPath):
    # 给V0版本的数据添加ID信息
    for name in Openlaw_ClassDict:
        NewData = []
        oriData = load_json(os.path.join(InPath, Openlaw_ClassDict[name]+".json"))
        for data_id, data in enumerate(oriData):
            tmp_data = data
            tmp_data["ID"] = name+"_id%s" %(str(data_id))
            NewData.append(tmp_data)
        dump_json(NewData, os.path.join(OutPath, Openlaw_ClassDict[name]+".json"))

AddIDInfo(path_data_openlaw_v0_dir, "../../data/raw/openlaw_v1")
"""

def ConvertList2Dict(Datas):
    # 将每类案例的存储由List修改为以ID为Key值的Dict数据类型
    print("将每类案例的存储由List修改为以ID为Key值的Dict数据类型")
    for name in Openlaw_ClassDict:
        NewData = {}
        for data in Datas[name]:
            # 将每个案例的存储改变为{key: value}的形式
            if data["ID"].startswith("OpenlawClass") != True:
                data["ID"] = data["ID"].replace("class", "OpenlawClass")
            NewData[data["ID"]] = data
        Datas[name] = NewData
    print("Convert Over.")
    return Datas

def DeleteCases(Datas):
    # 删去一些我们认为不太合适的案例
    print("删去一些我们认为不太合适的案例")
    DeleteList1 = [
        # 1. 没有当事人信息及其他重要信息
        {"OpenlawClass1":[354], "OpenlawClass2":[], "OpenlawClass3":[41, 43, 165, 177, 208, 128, 230],
         "OpenlawClass4":[1763, 1764, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 1800, 1855, 1856, 1857, 1858,
                           1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873,
                           1874, 1875, 1876, 1925, 1926, 1927, 1928, 1929, 1930, 2022, 2023, 2146, 2314, 2315, 3321, 3396,
                          3830, 3851, 3852, 3853, 3854, 3855, 3856, 3857, 3858, 3860, 3861, 3865, 3890, 3892, 3997,3129, 4057,
                          3998, 3999, 4000, 4017, 4018, 2090, 2306, 2307, 2308, 2352, 2356, 4115, 4120, 4060, 2134, 2337, 2488, 3354, 3889],
         "OpenlawClass5":[79, 81, 167, 211, 346, 414, 447, 419, 421, 449, 477, 180, 187, 216, 327, 353, 546, 446, 426, 225]},
        ]
    for item in DeleteList1:
        for name in item:
            for number in item[name]:
                key = "%s_id%s" %(name, str(number))
                if key in Datas[name]:
                    print("Delete case %s: %s" %(key, Datas[name][key]["标题"]))
                    Datas[name].pop(key)
                else:
                    print("Case %s is not existing, has been deleted." % (key))
    print("Delete Over.")
    return Datas

def ExploitData(Datas):
    Count = 0
    DeleteList = {name:[] for name in Openlaw_ClassDict}
    for name in Openlaw_ClassDict:
        for data_id in Datas[name]:
            if re.search(r"(纠纷案|判决书|裁定书|纠纷|一案)", Datas[name][data_id]["标题"]) == None:
            # if "纠纷案" not in Datas[name][data_id]["标题"] and "判决书" not in Datas[name][data_id]["标题"]:
                print(data_id, Datas[name][data_id]["标题"])
    print(Count)
    print(DeleteList)

def WriteCase(ID, Datas):
    Datas[ID.split("_")[0]][int(ID.split("_id")[1])]["被告"] = "洋浦鹏远船务有限公司、万安县航运公司、汕头市福顺船务有限公司"
    return Datas

def main(v0_path, v1_path):
    ############################## 加载数据 ########################
    # Datas_v0 = Load_openlaw_data(v0_path)  # 从 v0_path 中加载数据
    Datas_v1 = Load_openlaw_data(v1_path) # 从 v1_path 中加载数据
    #####################将每类案例的存储由List修改为以ID为Key值的Dict数据类型#####################
    # Datas_v1 = ConvertList2Dict(Datas_v0)
    ##############################删除一些已经确定删除的案例#######################################
    # Datas_v1 = DeleteCases(Datas_v1)
    ##############################检查审理经过内容，并补全一些案例的审理经过########################
    # CompleteTrailProcess(Datas_v1)
    ############################## 存储数据到v1_path ########################
    # Dump_openlaw_data(Datas_v1, v1_path)
    #############################打印指定案例的内容##############################################
    # PrintCase(["OpenlawClass3_id322"], Datas_v1)
    # ExploitData(Datas_v1)

if __name__=="__main__":
    main(path_data_openlaw_v0_dir, path_data_openlaw_v1_dir)
    # Datas_v0 = Load_faxin_data(path_data_faxin_v0_dir)
    # Datas_v1 = ConvertList2Dict(Datas_v0)
    # Dump_faxin_data(Datas_v1, path_data_faxin_v1_dir)