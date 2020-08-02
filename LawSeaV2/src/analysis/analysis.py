import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

from collections import Counter

from util.data import *
from util.path import *

# ============= function ================

def select_keys():
    # 劳务
    datas_openlaw = load_openlaw_data0410()
    datas_faxin   = load_faxin_data0410()

    print("openlaw:", len(datas_openlaw))
    print("faxin:",   len(datas_faxin))
    print()

    keys_openlaw = get_keys(datas_openlaw)
    keys_faxin   = get_keys(datas_faxin)

    print("openlaw:")
    print(keys_openlaw)
    print()
    print("faxin:")
    print(keys_faxin)
    print("same:")
    print(keys_faxin & keys_openlaw)
    print("diff:")
    print((keys_faxin | keys_openlaw) - (keys_faxin & keys_openlaw))

    # 案由
    ay = Counter([data["案由"] for data in datas_openlaw+datas_faxin])
    for name, cnt in ay.most_common():
        print(name, cnt)

def get_keys(datas):
    keys = set()
    for data in datas:
        keys.update(data.keys())
    return keys

# =============== main ==================

def main():
    select_keys()

if __name__ == '__main__':
    main()