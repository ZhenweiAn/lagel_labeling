import re

# 诉讼请求:

def get_law(text):
    content = []

    if '工资' in text:
        content.append('支付工资')
    if '遣返费用' in text:
        content.append('支付遣返费用')
    if '利息' in text:
        content.append('支付利息')
    if '合同' in text and ('解除' in text or '终止' in text):
        content.append('解除劳务合同')
    if '船舶优先' in text:
        content.append('船舶优先权')

    return content

# 对于openlaw，输入的字符串为庭审过程。对于法信，输入的字符串为非id，相关法条，法律依据的拼接字符串
def request(text):
    item = dict()
    results = re.findall(r'(请求|诉请|判令|要求)(.*?)。、', text)
    item['诉讼请求'] = set()

    for result in results:
        item['诉讼请求'].update(get_law(result[1]))

    item['诉讼请求'] = list(item['诉讼请求'])
    return item

# 相关法条：
# 法信：
# item为一个样例，需要检测相关法条对应的list，如果不存在这个list，再从字符串里抽
def faxin_items(item):
    d = {'法律依据':set()}

    if '相关法条' in item:
        for law in item['相关法条']:
            mark = 0

            if '船员条例' in law:
                d['法律依据'].add('《船员条例》')
                mark = 1
            if '海商法' in law:
                d['法律依据'].add('《海商法》')
                mark = 1
            if '劳动合同法' in law:
                d['法律依据'].add('《劳动合同法》')
                mark = 1
            if '民事诉讼法' in law:
                d['法律依据'].add('《民事诉讼法》')
                mark = 1
            if mark == 0 and '法' in law:
                d['法律依据'].add('其他')
    else:
        for key, value in item.items():
            if key != 'ID' and key != '法律依据':
                laws = re.findall(r'《.+?》', value)

                for law in laws:
                    mark = 0

                    if '船员条例' in law:
                        d['法律依据'].add('《船员条例》')
                        mark = 1
                    if '海商法' in law:
                        d['法律依据'].add('《海商法》')
                        mark = 1
                    if '劳动合同法' in law:
                        d['法律依据'].add('《劳动合同法》')
                        mark = 1
                    if '民事诉讼法' in law:
                        d['法律依据'].add('《民事诉讼法》')
                        mark = 1
                    if mark == 0 and '法' in law:
                        d['法律依据'].add('其他')

    d['法律依据'] = list(d['法律依据'])
    return d

# openlaw:
# 输入字符串为所有拼接的字符串
def openlaw_items(text):
    d = {'法律依据':set()}
    laws = re.findall(r'《.+?》', text)

    for law in laws:
        mark = 0

        if '船员条例' in law:
            d['法律依据'].add('《船员条例》')
            mark = 1
        if '海商法' in law:
            d['法律依据'].add('《海商法》')
            mark = 1
        if '劳动合同法' in law:
            d['法律依据'].add('《劳动合同法》')
            mark = 1
        if '民事诉讼法' in law:
            d['法律依据'].add('《民事诉讼法》')
            mark = 1
        if mark == 0 and '法' in law:
           	d['法律依据'].add('其他')

    d['法律依据'] = list(d['法律依据'])
    return d