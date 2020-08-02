import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

import pickle
import json
from tqdm import tqdm
from collections import defaultdict

import xlrd

from util.path import *

Faxin_ClassDict = {"FaxinClass1": "faxin_海上、通海水域人身损害责任纠纷",
                   "FaxinClass2": "faxin_海上、通海水域货物运输合同纠纷",
                   "FaxinClass3": "faxin_船员劳务合同纠纷",
                   "FaxinClass4": "faxin_船舶碰撞（触碰）损害责任纠纷"}

Openlaw_ClassDict = {"OpenlawClass1": "openlaw_海上货物运输无单放货纠纷",
                     "OpenlawClass2": "openlaw_海上货物运输货损货差纠纷",
                     "OpenlawClass3": "openlaw_船员人身伤亡损害赔偿纠纷",
                     "OpenlawClass4": "openlaw_船员劳务合同报酬给付纠纷",
                     "OpenlawClass5": "openlaw_船舶碰撞损害赔偿纠纷"}

# ============= function ==============

def load_pkl(path):

    '''
        读取pkl数据
        参数：
            path： 字符串， 数据的path
        返回：
            pickle数据
    '''

    with open(path, "rb") as f:
        return pickle.load(f)


def dump_pkl(data, path):

    '''
        通过pickle存储
        参数:
            data: 待存储的数据
            path: 存储路径
        返回：
            无
    '''

    with open(path, "wb") as f:
        pickle.dump(data, f, protocol=2)

def load_str_lst(path):
    
    '''
        读取字符串表
        参数：
            path： 字符串，词表的path
        返回：
            words： 列表，即字符串表
    '''

    strs = []
    with open(path, "r", encoding="utf8") as f:
        for line in tqdm(f):
            strs.append(line.strip())
    return strs

def dump_str_lst(lst, path):

    '''
        存储字符串表，一行一个
        参数:
            lst:  字符串列表
            path: 路径
        返回：
            无
    '''

    with open(path, "w", encoding="utf8") as f:
        for string in tqdm(lst):
            f.write(string+'\n')

def load_json(file_path):
    ''' 读取json文件 '''
    with open(file_path, "r", encoding="utf8") as f:
        data = json.load(f)
        return data

def dump_json(data, file_path):
    ''' 存储json文件 '''
    with open(file_path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def dict_to_defaultdict(d, data_type):
    ''' 将dict转为defaultdict '''
    dd = defaultdict(data_type)
    for k, v in d.items():
        dd[k] = v 
    return dd

# ============= data specific ===========

def load_idf(path):
    ''' 读取idf文件 '''
    word_idf = {}
    for line in load_str_lst(path):
        try:
            word, idf = line.strip().split("\t")
            word_idf[word] = float(idf)
        except:
            pass
    return word_idf

###############################################################################
##########################加载保存法信数据的函数###############################
###############################################################################
"""
yeyuan 修改法信数据加载保存函数 2020年6月18日
"""
def Load_faxin_data(path):
    # 加载faxin的数据
    Datas = {}
    print("从文件夹%s中加载法信数据."%(path))
    for name in Faxin_ClassDict:
        Datas[name] = load_json(os.path.join(path, Faxin_ClassDict[name]+".json"))
        print(Faxin_ClassDict[name], len(Datas[name]))
    print("Load data over.")
    return Datas

def Dump_faxin_data(Datas, path):
    # 存储法信数据
    print("存储法信数据到文件夹%s"%(path))
    for name in Faxin_ClassDict:
        dump_json(Datas[name], os.path.join(path, Faxin_ClassDict[name]+".json"))
    print("Dump faxin data over.")

###############################################################################
##########################加载保存Openlaw数据的函数###############################
###############################################################################
"""
yeyuan 修改openlaw数据加载保存函数 2020年6月18日
"""
def Load_openlaw_data(path):
    # 加载openlaw的数据
    Datas = {}
    print("从文件夹%s中加载openlaw数据."%(path))
    for name in Openlaw_ClassDict:
        Datas[name] = load_json(os.path.join(path, Openlaw_ClassDict[name]+".json"))
        print(Openlaw_ClassDict[name], len(Datas[name]))
    print("Load openlaw data over.")
    return Datas

def Dump_openlaw_data(Datas, path):
    # 存储openlaw数据
    print("存储openlaw数据到文件夹%s"%(path))
    for name in Openlaw_ClassDict:
        dump_json(Datas[name], os.path.join(path, Openlaw_ClassDict[name]+".json"))
    print("Dump openlaw data over.")

def load_openlaw_raw():
    ''' 读取openlaw文件 '''
    datas = []
    for name in os.listdir(path_data_openlaw_dir):
        file_path = os.path.join(path_data_openlaw_dir, name)
        # openlaw是excel
        table = xlrd.open_workbook(file_path).sheets()[0]
        properties = table.row(0)
        for r in range(1, table.nrows):
            row = table.row(r)
            data = {p.value:r.value for p, r in zip(properties, row)}
            datas.append(data)
    return datas

def load_faxin_data0410():
    ''' 读取法律信0410数据 '''
    datas = []
    for name in os.listdir(path_data_data0410_dir):
        if name.startswith("faxin"):
            file_path = os.path.join(path_data_data0410_dir, name)
            datas += load_json(file_path)
    return datas

def load_openlaw_data0410():
    ''' 读取法律信0410数据 '''
    datas = []
    for name in os.listdir(path_data_data0410_dir):
        if name.startswith("openlaw"):
            file_path = os.path.join(path_data_data0410_dir, name)
            datas += load_json(file_path)
    return datas

# ============== main ====================

def main():
    load_openlaw_raw()


if __name__ == '__main__':
    main()