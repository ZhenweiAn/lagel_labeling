# 得先判断字典中有没有‘原告诉称’这个key，因为有些案件是原告撤销上诉申请庭外调解的。对于这些案件，目标字段的值为空列表。
# 如果有‘原告诉称’的话，再判断有没有被告辩称。因为有些案件的被告没有出席庭审。假如被告出席了，关键信息基本都在‘被告辩称’中。
# 只有‘原告诉称’的话，faxin_extract_*的输入就是‘原告诉称’。既有‘原告诉称’也有‘被告辩称’的话，faxin_extract_*的输入就是两者的拼接


def faxin_input(dict):
    if '原告诉称' not in dict.keys():
        return None
    if '被告辩称' in dict.keys():
        return dict['原告诉称']+dict['被告辩称']
    else:
        return dict['原告诉称']


def faxin_extract_1(str):
    if str is None:
        return {'劳务合同的形式':[]}
    n=str.find('口头')
    if n!=-1:
        return {'劳务合同的形式':['口头']}
    else:
        return {'劳务合同的形式':['书面']}


def faxin_extract_2(str):
    s=['船员服务簿','船员服务薄','船员服务资历簿','船员服务资历','船员证言','下船证明','上船证明']
    ans={'船员在船工作及工作时间的证明':[]}
    if str is None:
        return ans
    n1 = str.find('未')
    n2 = str.find('无')
    n3 = str.find('没')
    for i in s:
        n=str.find(i)
        if n!=-1 and abs(n-n1)>8 and abs(n-n2)>8 and abs(n-n3)>8:
            if i=='船员服务资历簿' or i=='船员服务薄' or i=='船员服务簿' or i=='船员服务资历':
                ans['船员在船工作及工作时间的证明'].append('船员服务簿')
            else:
                ans['船员在船工作及工作时间的证明'].append(i)
    if len(ans['船员在船工作及工作时间的证明'])==0:
        ans['船员在船工作及工作时间的证明'].append('其他')

    return ans

def faxin_extract_3(str):
    s=['劳务派遣协议','劳动合同','劳务合同','上船协议']
    ans = {'劳务关系存在的证明': []}
    if str is None:
        return ans

    n1 = str.find('未')
    n2 = str.find('无')
    n3 = str.find('没')
    if str.find('口头')!=-1:
        ans['劳务关系存在的证明'].append('微信、短信、电话等聊天记录')
        return ans

    for i in s:
        n=str.find(i)
        if n!=-1 and abs(n-n1)>8 and abs(n-n2)>8 and abs(n-n3)>8:
            ans['劳务关系存在的证明'].append(i)

    if len(ans['劳务关系存在的证明'])==0:
        ans['劳务关系存在的证明'].append('其他')

    return ans

def openlaw_extract_1(str):
    n=str.find('口头')
    if n!=-1:
        return {'劳务合同的形式':['口头']}
    else:
        return {'劳务合同的形式':['书面']}

def openlaw_extract_2(str):
    s=['船员服务簿','船员服务薄','船员服务资历簿','船员服务资历','船员证言','下船证明','上船证明']
    ans={'船员在船工作及工作时间的证明':[]}
    n1 = str.find('未')
    n2 = str.find('无')
    n3 = str.find('没')
    for i in s:
        n=str.find(i)
        if n!=-1 and abs(n-n1)>8 and abs(n-n2)>8 and abs(n-n3)>8:
            if i=='船员服务资历簿' or i=='船员服务薄' or i=='船员服务簿' or i=='船员服务资历':
                ans['船员在船工作及工作时间的证明'].append('船员服务簿')
            else:
                ans['船员在船工作及工作时间的证明'].append(i)
    if len(ans['船员在船工作及工作时间的证明'])==0:
        ans['船员在船工作及工作时间的证明'].append('其他')

    return ans

def openlaw_extract_3(str):
    s=['劳务派遣协议','劳动合同','劳务合同','上船协议']
    ans = {'劳务关系存在的证明': []}
    n1 = str.find('未')
    n2 = str.find('无')
    n3 = str.find('没')
    if str.find('口头')!=-1:
        ans['劳务关系存在的证明'].append('微信、短信、电话等聊天记录')
        return ans

    for i in s:
        n=str.find(i)
        if n!=-1 and abs(n-n1)>8 and abs(n-n2)>8 and abs(n-n3)>8:
            ans['劳务关系存在的证明'].append(i)

    if len(ans['劳务关系存在的证明'])==0:
        ans['劳务关系存在的证明'].append('其他')

    return ans