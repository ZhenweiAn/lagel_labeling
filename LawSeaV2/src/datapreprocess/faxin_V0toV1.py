# _*_coding=utf-8_*_
# 数据预处理程序，预处理法信的数据，从V0版本的数据修改为V1版本的数据
'''
一些发现：
文书大致包括如下几种：
裁定书，移送函，判决书，民事决定书，纠纷案

补充资料：
民事判决书: 法院根据bai判决写成的文书du。经过审理，宣布判决时，zhi不论是一审、二审、还是再审，都用判决书。
民事决定书: 民事决定文书，是指人民法院在审理民事案件过程中，为了保证诉讼活动的顺利进行，而对案件审理中出现的某些特殊而紧迫的诉讼程序问题作出决定时所制作的司法文书的总称。 例如法院对当事人申请回避的答复，要用决定书。
民事裁定书: 人民法院在审理民事案件和执行民事判决的过程中，为保障诉讼的顺利进行，就程序问题作出的书面处理决定，称为民事裁定书。例如某人起诉内容不符合法院受理的条件，法院会裁定不予受理。此时用的是裁定书。

修改说明：
1. 将每类案例的存储由List修改为以ID为Key值的Dict数据类型, ID修改为FaxinClass1_id0这样的格式
2. 删除一些不好处理的案例
3. 修改一些不正确的标题
4. 补全一些案例的当事人信息
5. 补全一些案例的审理经过信息

'''
import os, json, re
from util.data import Faxin_ClassDict, Load_faxin_data, Dump_faxin_data
from util.path import path_data_faxin_v0_dir, path_data_faxin_v1_dir

###############################################################################
############################打印查看信息的辅助函数#############################
###############################################################################

def PrintTitle(Datas):
    for name in Faxin_ClassDict:
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

def CheckDangShiRenXin(Datas):
    '''
    检查当事人信息是否完整准确：
    1. 详细查看没有当事人信息的案例的原因，对可以删除的案例进行删除，可以修正的进行修正
    '''
    for name in Faxin_ClassDict:
        ResultIDList = []
        for data_id in Datas[name]:
            if "当事人信息" not in Datas[name][data_id]:
                ResultIDList.append(data_id)
                print(data_id, Datas[name][data_id]["标题"])
        print(ResultIDList, len(ResultIDList))
        for data_id in ResultIDList:
            if "原始文件" not in Datas[name][data_id]:
                print("没有原始文件信息：",data_id)
        PrintCase(ResultIDList, Datas)

def CheckTrialProcessInfo(Datas):
    # 检查审理经过信息是否完善
    for name in Faxin_ClassDict:
        for data_id in Datas[name]:
            if "原告诉称" in Datas[name][data_id] and "被告辩称" in Datas[name][data_id]:
                # 已经有原告诉称和被告辩称，不需要审理经过的详细信息
                continue
            if "审理经过" not in Datas[name][data_id]:
                if re.search(r"(本院|一案|本案)", "@@".join(Datas[name][data_id]["当事人信息"].split("\n")))!=None:
                    # 从当事人信息中补全审理经过的信息
                    pass
                elif "原始文件" not in Datas[name][data_id]:
                    # print("当事人信息中没有审理经过信息；", data_id, Datas[name][data_id]["当事人信息"])
                    pass
                else:
                    # 从原始文件中补全审理经过的信息
                    print("当事人信息中没有审理经过信息；", data_id, Datas[name][data_id]["当事人信息"])
# print(data_id, Datas[name][data_id]["标题"])

###############################################################################
##############################修改数据的函数###################################
###############################################################################

def ConvertList2Dict(Datas):
    # 将每类案例的存储由List修改为以ID为Key值的Dict数据类型
    print("将每类案例的存储由List修改为以ID为Key值的Dict数据类型")
    for name in Faxin_ClassDict:
        NewData = {}
        for data in Datas[name]:
            # 将每个案例的存储改变为{key: value}的形式
            if data["ID"].startswith("FaxinClass") != True:
                data["ID"] = data["ID"].replace("class", "FaxinClass")
            NewData[data["ID"]] = data
        Datas[name] = NewData
    print("Convert Over.")
    return Datas

def DeleteCases(Datas):
    # 删去一些我们认为不太合适的案例
    print("删去一些我们认为不太合适的案例")
    DeleteList1 = [
        ############李泽昌建议#############
        # 1. 大量莫名其妙的换行符
        {"FaxinClass1":[577, 573, 575, 578], "FaxinClass2":[2391, 2392], "FaxinClass3":[3710, 3727, 4403, 4404, 4405]},

        #############叶元建议##############
        #1. 文书格式不规范： 无法正确的划分每个域对应的内容
        {"FaxinClass1": [], "FaxinClass2": [263, 265, 267, 368, 1182, 1183, 1184, 2382], "FaxinClass3": [], "FaxinClass4":[528, 556]},
        #2. 文书为“移送函”，没有实质内容
        {"FaxinClass2":[453, 630, 632]},
        #3. 文书为民事决定书（目前法信收集到的民事决定书均是“其他民事决定书”），没有实质内容
        {"FaxinClass1":[294], "FaxinClass2":[1993], "FaxinClass3":[2939]},
        # 4. 根据当事人信息的完整程度删除案例
        {"FaxinClass1":[105],
         "FaxinClass2":[518,589,1589,1590,3390,3439,3441],  # 存在笔误，应予补正
         "FaxinClass3":[3662, 6951],
         "FaxinClass4":[8]},
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

def CompletePartiesInfo(Datas):
    # 补全当事人信息
    for name in Faxin_ClassDict:
        oriData = Datas[name]
        for data_id in oriData:
            if "当事人信息" not in oriData[data_id]:
                PartiesInfo = []
                InfoTextList = []
                if re.search(r"(原告|请求人|起诉人)", "@@".join(oriData[data_id]["原始文件"].split('\n'))) != None:
                    # 从原始文件的信息中提取当事人信息
                    InfoTextList = oriData[data_id]["原始文件"].split('\n')
                else:
                    if "审理经过" in oriData[data_id]:
                        # 利用审理经过的信息来提取当事人信息
                        InfoTextList = oriData[data_id]["审理经过"].split('\n')
                PlaintiffFlag, DefendantFlag = False, False
                if InfoTextList!=[]:
                    for sent in InfoTextList:
                        if re.search(r"(原告|请求人|起诉人)", sent) != None and PlaintiffFlag == False:
                            PartiesInfo.append(re.split("[，。]",sent)[0])
                            PlaintiffFlag = True
                        if re.search(r"(被告|被请求人|被起诉人)", sent) != None and DefendantFlag == False:
                            PartiesInfo.append(re.split("[，。]", sent)[0])
                            DefendantFlag = True
                        if PlaintiffFlag == True and DefendantFlag == True:
                            break
                if PlaintiffFlag == True and DefendantFlag == True:
                    Datas[name][data_id]["当事人信息"] = "\n".join(PartiesInfo)
                    print("补全案件%s的当事人信息" %(data_id))
                    print(Datas[name][data_id]["当事人信息"])
                else:
                    print("补全案件%s的当事人信息失败！！！！！！" %(data_id))
                    print("原始文件信息##################")
                    PrintCase([data_id], Datas)
    return Datas

def CompleteTrailProcess(Datas):
    # 补全审理经过
    for name in Faxin_ClassDict:
        for data_id in Datas[name]:
            InfoText = ""
            if "原告诉称" in Datas[name][data_id] or "被告辩称" in Datas[name][data_id]:
                # 已经有原告诉称或者被告辩称，不需要审理经过的详细信息
                continue
            if "审理经过" not in Datas[name][data_id]:
                if re.search(r"(本院|一案|本案)", "@@".join(Datas[name][data_id]["当事人信息"].split("\n")))!=None:
                    # 从当事人信息中补全审理经过的信息
                    InfoText = Datas[name][data_id]["当事人信息"]
                else:
                    if "原始文件" in Datas[name][data_id]:
                    # 从原始文件中补全审理经过的信息
                        if re.search(r"(本院|一案|本案)", "@@".join(Datas[name][data_id]["原始文件"].split("\n")))!=None:
                            InfoText = Datas[name][data_id]["原始文件"]
                        else:
                            # 对于原始文件中没有审理经过信息的案件，先保持不变，依然缺失审理经过信息
                            InfoText = ""
                # 开始补全审理经过信息
                print("############%s###############" % (data_id))
                if InfoText=="": # 如果没有找到对应的InfoText，直接保持 审理经过 信息为空
                    pass
                else:
                    TextList = re.split("\n|。", InfoText.replace("。\n", "。")) # 根据换行和句号切分字符串
                    position = -1
                    for i, sent in enumerate(TextList):
                        if re.search(r"(本院|一案|本案)",sent) != None:
                            position = i # 找到第一个包含（本院、一案、本案）的句子
                            break
                    TrailProcessText = ""
                    if position==-1:
                        pass # 没有找到对应的句子
                    else:
                        TrailProcessText = InfoText[InfoText.find(TextList[position]):]
                    # 对找到的审理经过文本进行后处理
                    if TrailProcessText=="":
                        pass
                    else:
                        # 首先找到本院认为以前的内容
                        TrailProcessText = TrailProcessText.split("本院认为")[0]
                        # 如果有提到“本案现已审理终结”，找到“审理终结”以前的内容
                        if "审理终结" in TrailProcessText:
                            TrailProcessText = TrailProcessText.split("审理终结")[0]+"审理终结"
                        # 处理文本首尾的句号和换行符
                        TrailProcessText = TrailProcessText.strip("。").strip()
                        Datas[name][data_id]["审理经过"] = TrailProcessText
                if "审理经过" in Datas[name][data_id]:
                    print("补全%s的审理经过为：%s" %(data_id, Datas[name][data_id]["审理经过"]))
    return Datas

def CorrectTitle(Datas):
    # 修正一些明显有问题的标题，主要包括以下案例：
    # FaxinClass2_id264, FaxinClass2_id368, FaxinClass2_id3854, FaxinClass3_id458
    print("Begin to correct titles of FaxinClass2_id264, FaxinClass3_id458 ......")
    CorrectInfo = {
        "FaxinClass2_id264":"美国定航国际货运服务有限公司与被告上海华源经济发展公司海上货物运输合同纠纷案",
        "FaxinClass3_id458":"中国武汉长江轮船公司海员对外技术服务公司诉巴拿马索达·格莱特航运有限公司船员雇用合同纠纷案"
    }
    for key in CorrectInfo:
        Datas[key.split("_")[0]][key]["标题"] = CorrectInfo[key]
        print("修改%s的标题为: %s" %(key, CorrectInfo[key]))
    print("Correct Title Over.")
    return Datas

def main(v0_path, v1_path):
    ############################## 加载数据 ########################
    # Datas_v0 = Load_faxin_data(v0_path) # 从 v0_path 中加载数据
    Datas_v1 = Load_faxin_data(v1_path) # 从 v1_path 中加载数据
    #####################将每类案例的存储由List修改为以ID为Key值的Dict数据类型#####################
    # Datas_v1 = ConvertList2Dict(Datas_v0)
    ##############################删除一些已经确定删除的案例#######################################
    # Datas_v1 = DeleteCases(Datas_v1)
    ##############################检查案例的标题，并修改一些案例标题###############################
    # Datas_v1 = CorrectTitle(Datas_v1)
    ##############################检查当事人信息内容，并补全一些案例的当事人信息####################
    # Datas_v1 = CompletePartiesInfo(Datas_v1)
    ##############################检查审理经过内容，并补全一些案例的审理经过########################
    # CompleteTrailProcess(Datas_v1)
    ############################## 存储数据到v1_path ########################
    # Dump_faxin_data(Datas_v1, v1_path)
    #############################打印指定案例的内容##############################################
    # IDList = ["FaxinClass3_id1296"]
    # PrintCase(IDList, Datas_v1)

if __name__=="__main__":
    main(path_data_faxin_v0_dir, path_data_faxin_v1_dir)
    # Datas_v0 = Load_faxin_data(path_data_faxin_v0_dir)
    # Datas_v1 = ConvertList2Dict(Datas_v0)
    # Dump_faxin_data(Datas_v1, path_data_faxin_v1_dir)