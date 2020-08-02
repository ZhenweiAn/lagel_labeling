import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

import re
import random
import traceback
from itertools import chain, product
from collections import Counter, defaultdict

from tqdm import tqdm
import jieba

from util.path import *
from util.data import *


# ============= function =================

def get_words_of_str(s, stopwords, cut_for_search=True):
    words = Counter()
    cut_func = jieba.cut_for_search if cut_for_search else jieba.cut
    for word in cut_func(s.strip()):
        if not word: continue
        if word in stopwords: continue
        if word.replace(".", "").isdigit(): continue
        words[word] += 1
    return words

def filter_by_idf(words, idf, lo, hi):
    res = []
    for word in words:
        word = word.strip()
        if not word: continue
        if idf[word] < lo or idf[word] > hi: continue
        if word in ["年", "月", "日", "轮", "元"]: continue
        res.append(word)
    return res


def get_item_vocab(item_set):
    vocab = set()
    for item in item_set:
        vocab |= set(item) 
    return vocab

def apriori(datas, max_word_num=5, min_support=0.1):
    ''' apriori算法挖掘频繁模式 '''
    data_size = len(datas)
    print("start apriori: data_size: %d, min_support: %f" % (data_size, min_support))

    # item set initialization
    print("item num 1")
    item_set = defaultdict(int)
    for data in datas:
        for word in data:
            item_set[(word,)] += 1
    for item in list(item_set.keys()):
        if item_set[item] / data_size < min_support:
            del item_set[item]
    vocab = get_item_vocab(item_set)

    print("item_set_size: %d" % len(item_set))
    print("item_vocab_size: %d" % len(vocab))


    res = {1: {"item_set": item_set, "vocab": vocab}}
    for item_num in range(1, max_word_num):
        print("item num: %d" % (item_num+1))

        # expand
        print("expanding ...")
        new_item_set = {}
        for item in tqdm(item_set):
            for word in vocab:
                if word not in item and sum([item_word[-2:] == word[-2:] for item_word in item]) / item_num <= 0.5:
                    new_item_set[tuple(sorted(item+(word,)))] = 0

        # filter
        print("filtering ...")
        for data in tqdm(datas):
            data = set(data)
            for item in new_item_set:
                if set(item).issubset(data):
                    new_item_set[item] += 1
        for item in list(new_item_set.keys()):
            if new_item_set[item] / data_size < min_support:
                del new_item_set[item]

        item_set = new_item_set
        vocab = get_item_vocab(item_set)

        print(sorted(item_set.items(), key=lambda item: item[1]))
        print(vocab)
        print("item_set_size: %d" % len(item_set))
        print("item_vocab_size: %d" % len(vocab))
        print()
        res[item_num+1] = {"item_set": item_set, "vocab": vocab}

    return res

# ============== script ==================

def compute_idf():
    ''' 计算iftdf '''
    load_path = os.path.join(path_extract_stage_1, "法信_抽取.json")
    datas = load_json(load_path)
    stopwords = set(load_str_lst(path_stopwords))

    # 诉求集合，证据集合
    requests, evidences = set(), set()
    for data in datas:
        requests |= set(chain(*[plaintiff["诉求"] for plaintiff in data["原告"]]))
        evidences_plaintiff = set(chain(*[plaintiff["证据"] for plaintiff in data["原告"]]))
        evidences_defendant = set(chain(*[defendant["证据"] for defendant in data["被告"]]))
        evidences |= evidences_plaintiff | evidences_defendant

    # idf of requests
    idf_requests = defaultdict(int)
    for request in requests:
        for word in set(get_words_of_str(request, stopwords, cut_for_search=True)):
            idf_requests[word] += 1
    request_num = len(requests)
    for word, num in idf_requests.items():
        idf_requests[word] = request_num / num

    # idf of evidences
    idf_evidences = defaultdict(int)
    for evidence in evidences:
        for word in set(get_words_of_str(evidence, stopwords, cut_for_search=True)):
            idf_evidences[word] += 1
    evidence_num = len(evidences)
    for word, num in idf_evidences.items():
        idf_evidences[word] = evidence_num / num

    # save
    idf_requests  = sorted([(word, idf) for word, idf in idf_requests.items()],  key=lambda item: item[1])
    idf_evidences = sorted([(word, idf) for word, idf in idf_evidences.items()], key=lambda item: item[1])
    idf_requests  = [word+"\t"+str(idf) for word, idf in idf_requests]
    idf_evidences = [word+"\t"+str(idf) for word, idf in idf_evidences]
    path_idf_requests  = os.path.join(path_data_dir, "idf_requests.txt")
    path_idf_evidences = os.path.join(path_data_dir, "idf_evidences.txt")
    dump_str_lst(idf_requests,  path_idf_requests)
    dump_str_lst(idf_evidences, path_idf_evidences)



def frequent_item_mining():
    ''' 挖掘频繁项集 '''

    # load data
    load_path = os.path.join(path_extract_stage_1, "法信_抽取.json")
    datas = load_json(load_path)
    stopwords = set(load_str_lst(path_stopwords))
    idf_requests  = load_idf(os.path.join(path_data_dir, "idf_requests.txt"))
    idf_evidences = load_idf(os.path.join(path_data_dir, "idf_evidences.txt"))


    word_set_total = []
    for data in datas:
        requests = set(chain(*[plaintiff["诉求"] for plaintiff in data["原告"]]))
        evidences_plaintiff = set(chain(*[plaintiff["证据"] for plaintiff in data["原告"]]))
        evidences_defendant = set(chain(*[defendant["证据"] for defendant in data["被告"]]))
        evidences = evidences_plaintiff | evidences_defendant

        # word cut
        requests  = [get_words_of_str(request, stopwords, cut_for_search=True)  for request in requests]
        evidences = [get_words_of_str(evidence, stopwords, cut_for_search=True) for evidence in evidences]

        # idf filter
        requests  = [filter_by_idf(request, idf_requests, 2.1, 1000) for request in requests]
        evidences = [filter_by_idf(evidence, idf_evidences, 3, 1000) for evidence in evidences]

        word_set_requests  = set([word+"_request" for word in chain(*requests)])
        word_set_evidences = set([word+"_evidence" for word in chain(*evidences)])
        word_set_total.append(word_set_requests | word_set_evidences)


    freq_itemset = apriori(word_set_total, max_word_num=10, min_support=0.015)
    path_save = os.path.join(path_data_dir, "freq_itemset_mwn10_ms0.015.pkl")
    dump_pkl(freq_itemset, path_save)


def rule_generation():
    ''' 关联规则生成 '''

    # load data
    load_path = os.path.join(path_extract_stage_1, "法信_抽取.json")
    datas = load_json(load_path)
    stopwords = set(load_str_lst(path_stopwords))
    idf_requests  = load_idf(os.path.join(path_data_dir, "idf_requests.txt"))
    idf_evidences = load_idf(os.path.join(path_data_dir, "idf_evidences.txt"))
    freq_itemset_path = os.path.join(path_data_dir, "freq_itemset_mwn10_ms0.015.pkl")
    freq_itemset = load_pkl(freq_itemset_path)

    # data preproecss
    data_word_sets = []
    for data in datas:
        requests = set(chain(*[plaintiff["诉求"] for plaintiff in data["原告"]]))
        evidences_plaintiff = set(chain(*[plaintiff["证据"] for plaintiff in data["原告"]]))
        evidences_defendant = set(chain(*[defendant["证据"] for defendant in data["被告"]]))
        evidences = evidences_plaintiff | evidences_defendant

        # word cut
        requests  = [get_words_of_str(request, stopwords, cut_for_search=True)  for request in requests]
        evidences = [get_words_of_str(evidence, stopwords, cut_for_search=True) for evidence in evidences]

        # idf filter
        requests  = [filter_by_idf(request, idf_requests, 2.1, 1000) for request in requests]
        evidences = [filter_by_idf(evidence, idf_evidences, 3, 1000) for evidence in evidences]

        requests_word_set  = set([word for word in chain(*requests)])
        evidences_word_set = set([word for word in chain(*evidences)]) 
        data_word_sets.append((requests_word_set, evidences_word_set))

    rules = {}
    for i, itemset in freq_itemset.items():
        if i == 1: continue 
        itemset = itemset["item_set"]
        for item in itemset:
            pre  = tuple(word.split("_")[0] for word in item if word.endswith("request"))
            post = tuple(word.split("_")[0] for word in item if word.endswith("evidence"))
            rules[(pre, post)] = {"item_support": 0, "pre_support": 0, "post_support": 0}

    # count support
    for request_words, evidence_words in tqdm(data_word_sets):
        for pre, post in rules:
            is_pre_support, is_post_support = False, False
            if set(pre).issubset(request_words):
                rules[(pre, post)]["pre_support"] += 1 
                is_pre_support = True
            if set(post).issubset(evidence_words):
                rules[(pre, post)]["post_support"] += 1 
                is_post_support = True
            if is_pre_support and is_post_support:
                rules[(pre, post)]["item_support"] += 1

    # compute confidence
    for item in rules:
        rules[item]["conf"] = rules[item]["item_support"] / rules[item]["pre_support"]


    # save
    rules_path = os.path.join(path_data_dir, "apriori_rules_mwn10_ms0.015.pkl")
    dump_pkl(rules, rules_path)

    rules = sorted(rules.items(), key=lambda item: item[1]["conf"])
    for item, stat in rules:
        pre, post = item 
        print("request:", pre, stat["pre_support"], "evidence:", post, stat["post_support"], "item:", stat["item_support"],  "conf:", stat["conf"])


def request_evidence_matching():
    ''' 根据频繁模式，对诉求和证据匹配 '''
    
    # load data
    datas_path = os.path.join(path_extract_stage_1, "法信_抽取.json")
    datas = load_json(datas_path)
    stopwords = set(load_str_lst(path_stopwords))
    rules_path = os.path.join(path_data_dir, "apriori_rules_mwn10_ms0.015.pkl")
    rules = load_pkl(rules_path)

    # select rules
    rules = sorted(rules.items(), key=lambda item: item[1]["conf"], reverse=True)
    
    # for rule in rules:
    #     print(rule)


    # matching 
    for data in datas:
        requests = set(chain(*[plaintiff["诉求"] for plaintiff in data["原告"]]))
        evidences_plaintiff = set(chain(*[plaintiff["证据"] for plaintiff in data["原告"]]))
        evidences_defendant = set(chain(*[defendant["证据"] for defendant in data["被告"]]))
        evidences = evidences_plaintiff | evidences_defendant

        if not requests or not evidences:
            continue

        # 分词
        requests  = [(get_words_of_str(request, stopwords, cut_for_search=True), request) for request in requests]
        evidences = [(get_words_of_str(evidence, stopwords, cut_for_search=True), evidence) for evidence in evidences]

        r_e_score = defaultdict(list)
        for r, e in product(requests, evidences):
            r_words, r = r 
            e_words, e = e
            r_words = set(r_words.keys())
            e_words = set(e_words.keys())

            rr = 0 
            for i, rule in enumerate(rules):
                rule_r_words, rule_e_words = rule[0]

                if set(rule_r_words).issubset(r_words) and set(rule_e_words).issubset(e_words):
                    # rr += 1 / (i + 1)
                    rr += (len(rules) - i) / len(rules)
            if rr > 0:
                r_e_score[r].append((e, rr))

            # if rr > 0:
            #     print("r:", r)
            #     print("e:", e)
            #     print(rr)
            #     print()
        
        if r_e_score:
            for r, e_score in r_e_score.items():
                e_score = sorted(e_score, key=lambda item: item[1], reverse=True)
                print("@"+data["ID"], r)
                for e, score in e_score:
                    print("---%.4f---" % score, e)
            print()
            




# =============== main ===================

def main():
    # compute_idf()
    # frequent_item_mining() # 频繁项集的产生
    # rule_generation() # 规则的产生
    request_evidence_matching()


if __name__ == '__main__':
    main()