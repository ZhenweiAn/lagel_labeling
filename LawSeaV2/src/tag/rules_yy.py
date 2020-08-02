# _*_coding=utf-8_*_
import re, json
# 针对一个给定的文本生成对应的标签内容
# 标签包括：应付劳务报酬和费用：工资、利息、遣返费用、其他；（不定项）；已经支付工资的证明：未支付、银行付款记录、转账记录、收据、其他；（不定项）

'''一些辅助函数'''
def cut_sent(para):
    # 通过一些标志符将输入字符串划分为短句
    para = re.sub('([；。！？?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？?][”’])([^，。！？?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

def re_match(re_list, str):
    # 给定一个string和一个正则表达式列表，判断当前string是否符合列表中的某一条正则表达式
    for tmp in re_list:
        # print(re.search(tmp, str))
        if re.search(tmp, str) is None:
            continue
        else:
            return True
    return False

def Str_preprocess(Str):
    # 替换冗余字符、错误字符
    new_str = Str.replace('\n', ' ')
    new_str = new_str.replace('\t', ' ')
    new_str = new_str.replace('\u3000\u3000', ' ')
    new_str = new_str.replace('\u3000', '')
    result = cut_sent(new_str) # 分句
    return result

def fee_and_evidence_output(input):
    '''
    输入一个string，得到对应的标签内容，如果无法确定就为空
    :param input: string 类型的字符串
    :return: 返回值是一个tuple([应付劳务报酬和费用的标签列表], [已经支付工资的证明标签列表])
    '''

    #####应付劳务报酬和费用的分析#####
    # 假设一句话里面只会提到一种相关的费用问题
    # “工资”相关的正则表达式
    salary_re_rules = [r'工资', r'劳动报酬', r'劳务报酬', r'劳务费']
    # “利息”相关的正则表达式
    interest_re_rules = [r'利息']
    # “遣返费用”相关的正则表达式
    cost_of_repatriation_re_rules = [r'遣返费用', r'遣返费']
    # “其他”相关的正则表达式
    others_re_rules = [r'人民币(.*)元', r'报酬', r'款项', r'费(.*[0-9]*)元', r'借款', r'([0-9]+)元', r'([0-9]+)万元', r'违约金']
    fee_labels = ['工资', '利息', '遣返费用', '其他']
    label_flag, tmp_label_flag = {label: False for label in fee_labels}, {}
    for sent in Str_preprocess(input):
        tmp_label_flag['工资'] = re_match(salary_re_rules, sent)  # 判断是否和工资相关
        tmp_label_flag['利息'] = re_match(interest_re_rules, sent)  # 判断是否和利息相关
        tmp_label_flag['遣返费用'] = re_match(cost_of_repatriation_re_rules, sent)  # 判断是否和遣返费用相关
        tmp_label_flag['其他'] = re_match(others_re_rules, sent) and not (tmp_label_flag['工资'] or tmp_label_flag['利息'] or tmp_label_flag['遣返费用'])  # 判断是否和其他相关
        for label in fee_labels:
            if label_flag[label] == False:
                label_flag[label] = tmp_label_flag[label]
    return_fee_label = []
    for label in fee_labels:
        if label_flag[label]:
            return_fee_label.append(label)
    #####已经支付工资的证明的分析#####
    # 假设一句话里面只会提及一种情况
    # “未支付”相关的正则表达式
    no_pay_re_rules = [r'请求(.*)支付(.*)工资', r'欠', r'拒绝支付', r'未(.*)支付', r'应得(.*)工资', r'未(.*)给付劳务费', r'未发放工资', r'未付工资款']
    # “银行付款记录”相关的正则表达式
    bank_record_re_rules = [r'银行卡(.*)付款', r'付款(.*)银行卡']
    # “转账记录”相关的正则表达式
    transfer_record_re_rules = [r'记录(.*)转账', r'转账(.*)记录']
    # “收据”相关的正则表达式
    receipt_re_rules = [r'收据']
    # “其他”相关的正则表达式
    others_re_rules = [r'收到(.*)支付(.*)工资(.*)([0-9]+)元', r'已(.*)付(.*)([0-9]+)元']
    evidence_labels = ['未支付', '银行付款记录', '转账记录', '收据', '其他']
    label_flag, tmp_label_flag = {label: False for label in evidence_labels}, {}
    for sent in Str_preprocess(input):
        tmp_label_flag['未支付'] = re_match(no_pay_re_rules, sent)  # 判断是否和未支付相关
        tmp_label_flag['银行付款记录'] = re_match(bank_record_re_rules, sent)  # 判断是否和银行付款记录相关
        tmp_label_flag['转账记录'] = re_match(transfer_record_re_rules, sent)  # 判断是否和转账记录相关
        tmp_label_flag['收据'] = re_match(receipt_re_rules, sent)  # 判断是否和收据相关
        tmp_label_flag['其他'] = re_match(others_re_rules, sent) and not (tmp_label_flag['银行付款记录'] or tmp_label_flag['转账记录'] or tmp_label_flag['收据'])  # 判断是否和其他相关
        for label in evidence_labels:
            if label_flag[label] == False:
                label_flag[label] = tmp_label_flag[label]
    return_evidence_label = []
    for label in evidence_labels:
        if label_flag[label]:
            return_evidence_label.append(label)
    ret = {"应付劳务报酬和费用": return_fee_label, "已经支付工资的证明": return_evidence_label}
    return ret

if __name__=='__main__':
    string = "被告王玉龙辩称：对原告诉状中陈述的事实以及拖欠原告工资金额无异议，对原告主张的工资费用对"
    print(fee_and_evidence_output(string))

