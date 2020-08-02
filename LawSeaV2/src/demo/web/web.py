import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))

from flask import Flask, request, render_template
from flask_restful import Api, Resource

import demo.es_api_wrapper as es
import tag.rules_lzc as lzc
import tag.rules_tjz as tjz
import tag.rules_txc as txc
import tag.rules_yy  as yy


app = Flask(__name__)
api = Api(app)

# ============= api =============

class AllDocs(Resource):
    ''' 获取所有文档 '''
    def put(self):
        result = es.search_all("law")
        res = []
        for hit in result["hits"]["hits"]:
            data  = hit["_source"]
            res.append(data)
        print("reslen:", len(res))
        return res

class Query(Resource):
    ''' 进行类案匹配 '''
    def put(self):
        dict_field_query = {}

        keywords  = request.form.get("keywords")
        if keywords:
            dict_field_query["庭审过程"] = keywords
            dict_field_query["法院意见"] = keywords
            dict_field_query["判决结果"] = keywords

        ay = request.form.getlist("ay[]")
        if ay:
            dict_field_query["案由"] = "\n".join(ay)

        cygzjbsx = request.form.getlist("cygzjbsx[]")
        if cygzjbsx:
            dict_field_query["船员雇主基本属性"] = "\n".join(cygzjbsx)

        lwhtdxs = request.form.getlist("lwhtdxs[]")
        if lwhtdxs:
            dict_field_query["劳务合同的形式"] = "\n".join(lwhtdxs)

        lwgxczdzm = request.form.getlist("lwgxczdzm[]")
        if lwgxczdzm:
            dict_field_query["劳务关系存在的证明"] = "\n".join(lwgxczdzm)

        gzbzdyd = request.form.getlist("gzbzdyd[]")
        if gzbzdyd:
            dict_field_query["工资标准的约定"] = "\n".join(gzbzdyd)

        yflwbchfy = request.form.getlist("yflwbchfy[]")
        if yflwbchfy:
            dict_field_query["应付劳务报酬和费用"] = "\n".join(yflwbchfy)

        yjzfdgzdzm = request.form.getlist("yjzfdgzdzm[]")
        if yjzfdgzdzm:
            dict_field_query["已经支付的工资的证明"] = "\n".join(yjzfdgzdzm)

        cyzcgzjgzsjdzm = request.form.getlist("cyzcgzjgzsjdzm[]")
        if cyzcgzjgzsjdzm:
            dict_field_query["船员在船工作及工作时间的证明"] = "\n".join(cyzcgzjgzsjdzm)

        zyjjfsdyd = request.form.getlist("zyjjfsdyd[]")
        if zyjjfsdyd:
            dict_field_query["争议解决方式的约定"] = "\n".join(zyjjfsdyd)

        ssqq = request.form.getlist("ssqq[]")
        if ssqq:
            dict_field_query["诉讼请求"] = "\n".join(ssqq)

        flyj = request.form.getlist("flyj[]")
        if flyj:
            dict_field_query["法律依据"] = "\n".join(flyj)


        print(dict_field_query)
        result = es.search_multi_fields("law", dict_field_query)
        res = []
        for hit in result["hits"]["hits"]:
            score = hit["_score"]
            data  = hit["_source"]
            data["score"] = score
            res.append(data)

        return res

class ExtractDescription(Resource):
    ''' 对案情描述进行抽取 '''
    def put(self):
        description = request.form.get("description")
        dict_attributes = {}

        # tjz 船员雇主基本属性 工资标准的约定
        d = tjz.CYGZJBSX(description)                     # 船员雇主基本属性
        dict_attributes.update(d) 
        d = tjz.GZBZDYD(description)                      # 工资标准的约定
        dict_attributes.update(d)

        # lzc 诉讼请求 法律依据
        d = lzc.request(description)                      # 诉讼请求
        dict_attributes.update(d)
        d = lzc.openlaw_items(description)                # 法律依据
        dict_attributes.update(d)

        # txc 劳务合同的形式 船员在船工作及工作时间的证明 劳务关系存在的证明
        d = txc.faxin_extract_1(description)              # 劳务合同的形式
        dict_attributes.update(d)
        d = txc.faxin_extract_2(description)              # 船员在船工作及工作时间的证明
        dict_attributes.update(d)
        d = txc.faxin_extract_3(description)              # 劳务关系存在的证明
        dict_attributes.update(d)

        # yy  应付劳务报酬和费用 已经支付工资的证明
        d = yy.fee_and_evidence_output(description)       # 应付劳务报酬和费用 已经支付工资的证明
        dict_attributes.update(d)

        # 对key做转换，和html匹配
        key_dict = {
            "船员雇主基本属性": "cygzjbsx",
            "工资标准的约定": "gzbzdyd",
            "诉讼请求": "ssqq",
            "法律依据": "flyj",
            "劳务合同的形式": "lwhtdxs",
            "船员在船工作及工作时间的证明": "cyzcgzjgzsjdzm",
            "劳务关系存在的证明": "lwgxczdzm",
            "应付劳务报酬和费用": "yflwbchfy",
            "已经支付工资的证明": "yjzfgzdzm"
        }
        dict_attributes = {key_dict[k]: v for k, v in dict_attributes.items()}

        return dict_attributes

api.add_resource(AllDocs, "/all_docs")
api.add_resource(Query, "/query")
api.add_resource(ExtractDescription, "/extract")

# ============= web =============
@app.route('/search')
def web_search():
    return render_template("search.html")

@app.route('/library')
def web_library():
    return render_template("library.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8060, debug=True)