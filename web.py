from flask import request, Flask,render_template
from flask_restful import Api, Resource
import pymysql
import json

#encode
app = Flask(__name__)
api = Api(app)


def Get_Case(cursor,id):
    file_num = int(id[5])
    case_num = int(id[9:])
    case_id = 'class' + str(file_num) + '_id' + str(case_num + 1)

    sql = '''select * from LawCase where id = '%s' ''' % (case_id)
    cursor.execute(sql)
    Case = cursor.fetchall()
    if len(Case) == 0:
        case_id = 'class' + str(file_num + 1) + '_id0'
        sql = '''select * from LawCase where id = '%s' ''' % (case_id)
        cursor.execute(sql)
        Case = cursor.fetchall()
    return Case,case_id

def Get_Res(cursor,random):
    if random:
        sql = '''select id from LabelLog where labeled = 0 order by rand() limit 1'''
    else:
        sql = '''select id from LabelLog where labeled = 0 limit 1'''
    cursor.execute(sql)
    case_id = cursor.fetchall()
    print(case_id)
    if len(case_id) == 0:
        print('标注结束')
        return '结束页面'
    else:
        case_id = case_id[0]
        sql = '''select * from LawCase where id = '%s' ''' % (case_id)
        cursor.execute(sql)
        Case = cursor.fetchall()[0]
        sql_plaintiffevi = '''select evi from PlaintiffEvidence where id = '%s' ''' % (case_id)
        #print(sql_plaintiffevi)
        cursor.execute(sql_plaintiffevi)
        evis = cursor.fetchall()
        plaintiff_evis = [evi[0] for evi in evis]

        sql_defendentevi = '''select def from DefendentEvidence where id = '%s' ''' % (case_id)
        cursor.execute(sql_defendentevi)
        evis = cursor.fetchall()
        Defendent_evis = [evi[0] for evi in evis]

        sql_appeal = '''select app from Appeal where id = '%s' ''' % (case_id)
        cursor.execute(sql_appeal)
        apps = cursor.fetchall()
        apps = [app[0] for app in apps]

        sql_arg = '''select arg from Argue where id = '%s' ''' % (case_id)
        cursor.execute(sql_arg)
        args = cursor.fetchall()
        args = [arg[0] for arg in args]
        #print(Case[0])
        res = {
            '文书详情':
                {
                    'ID': Case[0],
                    '标题': Case[1],
                    '案号': Case[2],
                    '案由': Case[3],
                    '来源': Case[4],
                    '审理法院': Case[5],
                    '审判员': Case[6],
                    '书记员': Case[7],
                    '当事人': Case[8],
                    '庭审过程': Case[9],
                    '法院意见': Case[10],
                    '判决结果': Case[11]
                },
            '原告证据': plaintiff_evis,
            '被告证据': Defendent_evis,
            '诉求': apps,
            '辩称': args
        }
        return res

def judge_new_chain(chain, tup):
    inchain = 0
    #print("chain: ",chain,"tup: ",tup)
    for i in range(len(chain)):
        if tup[i] == -1:
            continue
        if chain[i] == tup[i]:
            inchain += 1

    return inchain

def get_new_chain(chain,tup):
    newchain = []
    for i in range(len(chain)):
        if chain[i] == -1:
            newchain.append(tup[i])
        else:
            newchain.append(chain[i])
    return newchain

def add_tuple(chains, tups):
    ini_chains = []
    remove_chains = []
    append_chains = []
    for chain in chains:
        ini_chains.append(chain)
    for tup in tups:
        add = True
        for chain in ini_chains:
            inchain = judge_new_chain(chain,tup)
            if inchain == 1:
                if chain not in remove_chains:
                    remove_chains.append(chain)
                new_chain = get_new_chain(chain,tup)
                if new_chain not in append_chains:
                    append_chains.append(new_chain)
                add = False
            elif inchain == 2:
                add = False
        if add:
            append_chains.append(tup)
    for chain in remove_chains:
        chains.remove(chain)
    for chain in append_chains:
        chains.append(chain)    
    return chains

#rel_plain_defen,rel_defenev_ap,rel_ap_ar,rel_plainev_ar
def find_chain(pair1,pair2,pair3,pair4,pair5,pair6):
    chains = []
    chains = add_tuple(chains,pair1)
    chains = add_tuple(chains,pair2)
    chains = add_tuple(chains,pair3)
    chains = add_tuple(chains,pair4)
    chains = add_tuple(chains,pair5)
    chains = add_tuple(chains,pair6)

    for chain in chains:
        if chain[0] == -1 and chain[1] != -1 and chain[2] == -1 and chain[3] != -1:
            chains.remove(chain)
        if chain[0] != -1 and chain[1] == -1 and chain[2] != -1 and chain[3] == -1:
            chains.append(chain)
    print(chains)
    return chains
     
def str2list(s):
    intlis = []
    print(s)
    if len(s) == 2:
        return intlis
    
    #将传输进来的字符串转化为二维列表
    s = s[2:-2]
    lis = s.split(']')
    lis = [i[2:] if i[0] == ',' else i for i in lis]
    for tup in lis:
        tup = tup.split(',')
        intlis.append([int(i) for i in tup])
    final_lis = []
    for i in range(len(intlis)):
        for num in intlis[i]:
            if num == 0:
                break
            final_lis.append([i,num - 1])
    return final_lis 

def str2list_v1(s):
    intlis = []
    if len(s) == 2:
        return intlis
    s = s[1:-1]
    lis = s.split(',')
    intlis = [-1 if i == 'null' else int(i) for i in lis]
    return intlis

def str2list_chain(s):
    #print(s)
    intlis = []
    if len(s) == 2:
        return intlis
    s = s[2:-2]
    lis = s.split(']')
    lis = [i[2:] if i[0] == ',' else i for i in lis]
    for chain in lis:
        chain = chain.split(',')
        intlis.append([int(i) - 1 if int(i) > 0 else -1 for i in chain])
    return intlis

def inverse(lis):
    newlis = []
    for tup in lis:
        newlis.append([tup[1],tup[0]])
    return newlis

class NextPage(Resource):
    def put(self):
        conn = pymysql.connect(host="localhost",port = 3306, user='root',passwd='icstwip',db='Label',charset='utf8')
        cursor = conn.cursor()
        res = Get_Res(cursor,True)
        sql = '''select count(*) from LabelLog where labeled = 1'''
        cursor.execute(sql)
        cnt = cursor.fetchall()[0][0] + 1
        return res

class Get_Chain(Resource):
    def put(self):
        conn = pymysql.connect(host="localhost",port = 3306, user='root',passwd='icstwip',db='Label',charset='utf8')
        cursor = conn.cursor()
        id = request.form.get('ID')

        rel_plainev_ap = str2list(request.form.get("rel_plainev_ap"))
        rel_plainev_ap = inverse(rel_plainev_ap)

        rel_defenev_ap = str2list(request.form.get("rel_defenev_ap"))

        rel_plainev_ar = str2list(request.form.get("rel_plainev_ar"))
        rel_plainev_ar = inverse(rel_plainev_ar)

        rel_defenev_ar = str2list(request.form.get("rel_defenev_ar"))
        rel_defenev_ar = inverse(rel_defenev_ar)


        rel_plain_defen = str2list(request.form.get("rel_plain_defen"))
        rel_plain_defen = inverse(rel_plain_defen)

        rel_ap_ar = str2list(request.form.get("rel_ap_ar"))
        rel_ap_ar = inverse(rel_ap_ar)

        ap_class = str2list_v1(request.form.get("appeal_class"))

        tups1 = []
        tups2 = []
        tups3 = []
        tups4 = []
        tups5 = []
        tups6 = []
        for p in rel_plain_defen:
            tups1.append([p[0] + 1,p[1] + 1,-1,-1])
        for p in rel_defenev_ap:
            tups2.append([-1,p[0] + 1,p[1] + 1,-1])
        for p in rel_ap_ar:
            tups3.append([-1,-1,p[0] + 1,p[1] + 1])
        for p in rel_plainev_ar:
            tups4.append([p[0] + 1,-1,-1,p[1] + 1])
        for p in rel_plainev_ap:
            tups5.append([p[0] + 1,-1,p[1] + 1,-1])
        for p in rel_defenev_ar:
            tups6.append([-1,p[0] + 1,-1,p[1] + 1])

        chains = find_chain(tups1,tups2,tups3,tups4,tups5,tups6)

        sql = '''select num from PlaintiffEvidence where id = '%s' ''' %(id)
        cursor.execute(sql)
        plainevi = cursor.fetchall()
        plainevi = [i[0] for i in plainevi]

        sql = '''select num from DefendentEvidence where id = '%s' ''' %(id)
        cursor.execute(sql)
        defenevi = cursor.fetchall()
        defenevi = [i[0] for i in defenevi]
        #print(defenevi)

        sql = '''select num from Appeal where id = '%s' ''' %(id)
        cursor.execute(sql)
        app = cursor.fetchall()
        app = [i[0] for i in app]

        sql = '''select num from Argue where id = '%s' ''' %(id)
        cursor.execute(sql)
        arg = cursor.fetchall()
        arg = [i[0] for i in arg]

        tmp = []

        for pair in rel_plainev_ap:
            tmp.append([plainevi[pair[0]],app[pair[1]]])
        rel_plainev_ap = tmp

        tmp = []
        for pair in rel_defenev_ap:
            tmp.append([defenevi[pair[0]],app[pair[1]]])
        rel_defenev_ap = tmp

        tmp = []
        for pair in rel_plainev_ar:
            tmp.append([plainevi[pair[0]],arg[pair[1]]])
        rel_plainev_ar = tmp

        tmp = []
        print(defenevi)
        print(arg)
        print(rel_defenev_ar)
        for pair in rel_defenev_ar:
            print(pair)
            tmp.append([defenevi[pair[0]],arg[pair[1]]])
        rel_defenev_ar = tmp

        tmp = []
        for pair in rel_plain_defen:
            tmp.append([plainevi[pair[0]],defenevi[pair[1]]])
        rel_plain_defen = tmp

        tmp = []
        for pair in rel_ap_ar:
            tmp.append([app[pair[0]],arg[pair[1]]])
        rel_ap_ar = tmp

        tmp = []
        for i in range(len(ap_class)):
            sql =  '''update Appeal SET class = %s where num = %s ''' % (ap_class[i],app[i])
            cursor.execute(sql)
        print('update end')


        sql = 'insert into rel_plainev_ap(ev_id,ap_id) values(%s,%s)'
        cursor.executemany(sql,rel_plainev_ap)

        sql = 'insert into rel_defenev_ap(ev_id,ap_id) values(%s,%s)'
        cursor.executemany(sql, rel_defenev_ap)

        sql = 'insert into rel_plainev_ar(ev_id,ar_id) values(%s,%s)'
        cursor.executemany(sql, rel_plainev_ar)

        sql = 'insert into rel_defenev_ar(ev_id,ar_id) values(%s,%s)'
        cursor.executemany(sql, rel_defenev_ar)

        sql = 'insert into rel_plain_defen(plain_ev_id,defen_ev_id) values(%s,%s)'
        cursor.executemany(sql, rel_plain_defen)

        sql = 'insert into rel_ap_ar(ap_id,ar_id) values(%s,%s)'
        cursor.executemany(sql, rel_ap_ar)
        
        
        conn.commit()
        return chains

class CommitPage(Resource):
    def put(self):
        conn = pymysql.connect(host="localhost",port = 3306, user='root',passwd='icstwip',db='Label',charset='utf8')
        cursor = conn.cursor()
        id = request.form.get('id')
        sql = '''select num from PlaintiffEvidence where id = '%s' ''' %(id)
        cursor.execute(sql)
        plainevi = cursor.fetchall()
        print(plainevi)
        plainevi = [i[0] for i in plainevi]

        sql = '''select num from DefendentEvidence where id = '%s' ''' %(id)
        cursor.execute(sql)
        defenevi = cursor.fetchall()
        defenevi = [i[0] for i in defenevi]

        sql = '''select num from Appeal where id = '%s' ''' %(id)
        cursor.execute(sql)
        app = cursor.fetchall()
        app = [i[0] for i in app]

        sql = '''select num from Argue where id = '%s' ''' %(id)
        cursor.execute(sql)
        arg = cursor.fetchall()
        arg = [i[0] for i in arg]
        chains = str2list_chain(request.form.get("chains"))
        insert_chains = []
        for chain in chains:
            plain_ele = -1
            defen_ele = -1
            app_ele = -1
            arg_ele = -1
            if chain[0] != -1:
                plain_ele = plainevi[chain[0]-1]
            if chain[1] != -1:
                defen_ele = defenevi[chain[1]-1]
            if chain[2] != -1:
                app_ele = app[chain[2]-1]
            if chain[3] != -1:
                arg_ele = arg[chain[3]-1]    
            insert_chains.append([id,plain_ele,defen_ele,app_ele,arg_ele])
        
        sql = 'insert into Focus(id,plain_evi_num,defen_evi_num,app_num,arg_num) values(%s,%s,%s,%s,%s)'
        cursor.executemany(sql,insert_chains)

        sql = '''update LabelLog SET labeled = 1 where id = '%s' ''' %(id)
        cursor.execute(sql)
        sql = '''select * from LabelLog where labeled = 1'''
        cursor.execute(sql)
        print(cursor.fetchall())
        res = Get_Res(cursor,False)
        conn.commit()
        return res       

api.add_resource(NextPage, "/next")
api.add_resource(Get_Chain, "/chain")
api.add_resource(CommitPage, "/commit")

@app.route('/tagging')
def web_search():
    return render_template("tagging.html")

if __name__ == '__main__':
    #print(str2list("[[1,2],[3,4],[16,25]]"))
    #app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0',port= 8080,debug=True)