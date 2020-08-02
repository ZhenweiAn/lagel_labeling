import os
import sys

# ============ basic setting =================
path_this_file = os.path.abspath(os.path.dirname(__file__))
path_proj_home = os.path.join(path_this_file, "..", "..")


# ============== data =================
path_data_dir = os.path.join(path_proj_home, "data")

# 工具数据
path_stopwords = os.path.join(path_data_dir, "stopwords.txt")

# 原始数据
path_data_raw_dir = os.path.join(path_data_dir, "raw")
path_data_faxin_v0_dir = os.path.join(path_data_raw_dir, "faxin_v0") # 法信_v0
path_data_faxin_v1_dir = os.path.join(path_data_raw_dir, "faxin_v1") # 法信_v1
path_data_openlaw_v0_dir = os.path.join(path_data_raw_dir, "openlaw_v0") # openlaw v0
path_data_openlaw_v1_dir = os.path.join(path_data_raw_dir, "openlaw_v1") # openlaw v1
path_data_openlaw_dir = os.path.join(path_data_raw_dir, "openlaw") # openlaw
path_data_data0410_dir = os.path.join(path_data_raw_dir, "data0410") # 0410数据

path_faxin_laowu   = os.path.join(path_data_dir, "法信_船员劳务合同纠纷.json")
path_openlaw_laowu = os.path.join(path_data_dir, "openlaw_船员劳务合同报酬给付纠纷.json") 


# 临时
path_data_tmp_dir = os.path.join(path_data_dir, "tmp")

# 规则标注
path_data_rule_tag_dir = os.path.join(path_data_dir, "rule_tag")
path_data_rule_tag_faxin_1 = os.path.join(path_data_rule_tag_dir, "faxin_laowu.json")
path_data_rule_tag_faxin_2 = os.path.join(path_data_rule_tag_dir, "法信-船员劳务合同纠纷+应付劳务报酬和费用+已经支付工资的证明.json")
path_data_rule_tag_faxin_3 = os.path.join(path_data_rule_tag_dir, "法信-船员劳务合同纠纷v3.json")
path_data_rule_tag_faxin_4_1 = os.path.join(path_data_rule_tag_dir, "txc_法信_船员劳务合同纠纷标注_1.json")
path_data_rule_tag_faxin_4_2 = os.path.join(path_data_rule_tag_dir, "txc_法信_船员劳务合同纠纷标注_2.json")

path_data_rule_tag_openlaw_1 = os.path.join(path_data_rule_tag_dir, "openlaw_laowu.json")
path_data_rule_tag_openlaw_2 = os.path.join(path_data_rule_tag_dir, "openlaw_船员劳务合同报酬给付纠纷v3.json")
path_data_rule_tag_openlaw_3 = os.path.join(path_data_rule_tag_dir, "openlaw-船员劳务合同纠纷+应付劳务报酬和费用+已经支付工资的证明.json")
path_data_rule_tag_openlaw_4 = os.path.join(path_data_rule_tag_dir, "txc_openlaw_船员劳务合同报酬给付纠纷标注.json")


# ============== extract stage 1 ===============

path_extract_stage_1 = os.path.join(path_data_dir, "extract", "stage1")


# ============== analysis ===============

path_analysis_dir = os.path.join(path_proj_home, "analysis")