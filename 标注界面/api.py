import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))

from flask import Flask, request, render_template
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


class GetLawCase(Resource):
    def put(self):

        data = {
                  "文书详情":{
                      "ID": "12",
                      "标题": "标题",
                      "案号": "案号",
                      "案由": "案由",
                      "来源": "来源",
                      "审理法院": "审理法院",
                      "审判员": "审判员",
                      "书记员": "书记员",
                      "当事人": "当事人",
                      "庭审过程": "庭审过程\n庭审过程\n庭审过程",
                      "法院意见": "法院意见",
                      "判决结果": "判决结果"
                  },
                  "原告证据": ["原证1", "原证2"],
                  "被告证据": ["被证1", "被证2"],
                  "诉求": ["诉求1", "诉求2"],
                  "辩称": ["辩称1", "辩称2"]
              }

        return data

class SubmitTagging(Resource):
    def put(self):
        print(request.form)

        data = [[1,0,1,2], [2,1,1,2]]

        return data

class SubmitDispute(Resource):
    def put(self):
        print(request.form)
        data = {}
        return data

api.add_resource(GetLawCase, "/get")
api.add_resource(SubmitTagging, "/submit")
api.add_resource(SubmitDispute, "/dispute")

@app.route('/tagging')
def web_search():
    return render_template("tagging.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)