import os
import sys

import json
import requests


# ============== gloabl ================

ES_ADDR = "localhost"
ES_PORT = 9200 

# ======================== func index =====================

def show_indices():

    '''
        查看当前结点所有index，直接在命令行输出当前状态
    '''

    url = "http://%s:%d/_cat/indices?v" % (ES_ADDR, ES_PORT)
    res = requests.get(url).text
    print(res)

def create_index(index_name, properties):

    '''
        新建一个index
        参数：
            index_name: 字符串，index的名字
            properties: 属性（默认全为中文）
        返回：
            一个字典，为ES返回的json对象
    '''
    mappings = {"mappings":{"properties":{}}}
    for p in properties:
        mappings["mappings"]["properties"][p] = {
                                                    "type": "text",
                                                    "analyzer": "ik_max_word",
                                                    "search_analyzer": "ik_max_word"
                                                }
    url = "http://%s:%d/%s" % (ES_ADDR, ES_PORT, index_name)
    res = requests.put(url, json=mappings).json()
    return res


def delete_index(index_name):

    '''
        删除一个index
        参数：
            index_name: 字符串，index的名字
        返回：
            一个字典，为ES返回的json对象
    '''

    url = "http://%s:%d/%s" % (ES_ADDR, ES_PORT, index_name)
    res = requests.delete(url).json()
    return res


# ======================== func record =====================

def insert_record(index_name, record_id, record):

    '''
        向index中插入一个记录
        参数：
            index_name:  字符串,index名
            record_id:   字符串,记录的id
            record:      字典，一条记录
        返回：
            一个字典，为ES返回的json对象
    '''

    url = "http://%s:%d/%s/_doc/%s" % (ES_ADDR, ES_PORT, index_name, record_id)
    res = requests.put(url, json=record).json()
    return res

def delete_record(index_name, record_id):

    '''
        从index中删除一个记录
        参数：
            index_name:  字符串,index名
            record_id:   字符串,记录的id
        返回：
            一个字典，为ES返回的json对象
    '''

    url = "http://%s:%d/%s/_doc/%s" % (ES_ADDR, ES_PORT, index_name, record_id)
    res = requests.delete(url).json()
    return res


def update_record(index_name, record_id, new_record):

    '''
        更新一条记录
        参数：
            index_name:  字符串,index名
            record_id:   字符串,记录的id
            new_record:  字典，新的记录
        返回：
            一个字典，为ES返回的json对象
    '''
    return insert_record(index_name, record_id, record)


# ======================== func search =====================

def search_all(index_name):

    '''
        返回所有记录
        参数：
            index_name: 字符串,index名
        返回：
            一个字典，为ES返回的json对象
    '''

    parameters = {"from":0, "size":1000}
    url = "http://%s:%d/%s/_doc/_search" % (ES_ADDR, ES_PORT, index_name)
    res = requests.get(url, json=parameters).json()
    return res


def search(index_name, fields, query):

    '''
        全文搜索
        参数：
            index_name:  字符串,index名
            query:       字符串，指定检索内容的query，
                         见：https://www.elastic.co/guide/cn/elasticsearch/guide/current/_most_important_queries.html
            fields：      需要检索的字段,list
        返回：
            一个字典，为ES返回的json对象        
    '''
    wrapped_match_query = {"query":{"multi_match":{"query": query, "fields": fields}}}
    url = "http://%s:%d/%s/_doc/_search" % (ES_ADDR, ES_PORT, index_name)
    res = requests.get(url, json=wrapped_match_query).json()
    return res

def search_multi_fields(index_name, dict_field_query, tie_breaker=0.3):
    '''
        多字段查询
        参数:
            index_name:        字符串, index名
            dict_field_query:  字典 {field: query}
            tir_breaker:       一个权重, [0, 1], 见: https://www.elastic.co/guide/cn/elasticsearch/guide/current/_tuning_best_fields_queries.html
        返回:
            一个字典，为ES返回的json对象
    '''
    queries = [{"match":{field: query}} for field, query in dict_field_query.items()]
    wrapped_match_query = {"query":{"dis_max":{"queries":queries,"tie_breaker":tie_breaker}}}
    print(wrapped_match_query)
    url = "http://%s:%d/%s/_doc/_search" % (ES_ADDR, ES_PORT, index_name)
    res = requests.get(url, json=wrapped_match_query).json()
    return res

def parse_search_result(res):
    ''' 解析es搜索返回的结果 '''
    pass
    

# =============== main =================

def main():
    show_indices()


if __name__ == '__main__':
    main()