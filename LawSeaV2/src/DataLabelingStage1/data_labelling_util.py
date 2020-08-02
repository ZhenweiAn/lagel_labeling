from util.data import Faxin_ClassDict, Openlaw_ClassDict

def merge_data(faxin_datas, openlaw_datas):
    Datas = {}
    for name in Faxin_ClassDict:
        for key in faxin_datas[name]:
            Datas[key] = faxin_datas[name][key]
    for name in Openlaw_ClassDict:
        for key in openlaw_datas[name]:
            Datas[key] = openlaw_datas[name][key]
    return Datas