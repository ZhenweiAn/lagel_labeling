import pymysql
import os
import json
from LawSeaV2.src.util.data import Load_faxin_data,Load_openlaw_data


def createCaseTable(cursor):

    sql = """drop table if exists LawCase """
    cursor.execute(sql)

    '''建立表'''
    #ID  标题  案号  案由  来源   审理法院   审判员    书记员    当事人   庭审过程    法院意见  判决结果
    sql = '''
    create table LawCase(
            id varchar(255) not null primary key,
            title text,
            case_num text,
            classification text,
            source text,
            court text,
            judge text,
            clerk text,
            concerned  text,
            process  text,  
            court_opinion text,
            result text
            )engine=innodb default charset=utf8;
    '''
    cursor.execute(sql)
    print('成功创建LawCase数据库')

def createPlaintiffEvidence(cursor):
    sql = '''drop table if exists PlaintiffEvidence'''
    cursor.execute(sql)

    '''建立表'''
    sql = '''
        CREATE TABLE PlaintiffEvidence(
            num int not null auto_increment primary key,
            id varchar(255) not null,
            evi text
            )engine=innodb default charset=utf8;
        '''
    cursor.execute(sql)
    print('成功创建PlaintiffEvidence数据库')

def createDefendentEvidence(cursor):
    sql = '''drop table if exists DefendentEvidence'''
    cursor.execute(sql)

    '''建立表'''
    sql = '''
            create table DefendentEvidence (
            num int not null auto_increment primary key,
            id varchar(255) not null,
            def text
            )engine=innodb default charset=utf8;
            '''
    cursor.execute(sql)
    print('成功创建DefendentEvidence数据库')

def createAppeal(cursor):
    sql = '''drop table if exists Appeal'''
    cursor.execute(sql)

    #class是对诉求的分类,0 驳回，1部分驳回, 2 支持, -1未分类
    '''建立表'''
    sql ='''
        create table Appeal (
            num int not null auto_increment primary key,
            id varchar(255) not null,
            app text
            )engine=innodb default charset=utf8;
         '''
    cursor.execute(sql)
    print('成功创建Appeal数据库')


def createAppealLabel(cursor):
    sql = '''drop table if exists AppealLabel'''
    cursor.execute(sql)

    #class是对诉求的分类,0 驳回，1部分驳回, 2 支持, -1未分类
    '''建立表'''
    sql ='''
        create table AppealLabel (
            ap_num int not null,
            lb_id int not null
            )engine=innodb default charset=utf8;
         '''
    cursor.execute(sql)
    print('成功创建Appeal数据库')

def createArgue(cursor):
    sql = '''drop table if exists Argue'''
    cursor.execute(sql)

    '''建立表'''
    sql ='''
        create table Argue (
            num int not null auto_increment primary key,
            id varchar(255) not null,
            arg text
            )engine=innodb default charset=utf8;
         '''
    cursor.execute(sql)
    print('成功创建Argue数据库')

def createFocus(cursor):
    sql = '''drop table if exists Focus'''
    cursor.execute(sql)

    '''建立表'''
    sql = '''
            create table Focus (
                num int not null auto_increment primary key,
                id varchar(255) not null,
                plain_evi_num int,
                defen_evi_num int,
                app_num int,
                arg_num int,
                lb_id int
                )engine=innodb default charset=utf8;
             '''
    cursor.execute(sql)
    print('成功创建Focus数据库')


def createLabelEvent(cursor):

    sql = '''drop table if exists LabelEvent'''
    cursor.execute(sql)

    '''建立表'''
    sql = '''
            create table LabelEvent (
                num int not null auto_increment primary key,
                case_id varchar(255) not null,
                labeller_id varchar(255) not null
                )engine=innodb default charset=utf8;
             '''
    cursor.execute(sql)
    print('成功创建LabelEvent数据库')


def createLabelList(cursor):

    sql = '''drop table if exists LabelList'''
    cursor.execute(sql)

    '''建立表'''
    sql = '''
            create table LabelList (
                num int not null auto_increment primary key,
                id varchar(255) not null
                )engine=innodb default charset=utf8;
             '''
    cursor.execute(sql)
    print('成功创建LabelList数据库')


def createLabelCount(cursor):

    sql = '''drop view if exists LabelCount'''
    cursor.execute(sql)

    '''建立表'''
    sql = '''
            create view LabelCount as
            select LabelList.id, (case when cnt.label_sum is not null then cnt.label_sum else 0 end) as count
            from LabelList
            left join 
            (
                select case_id, count(*) as label_sum 
                from LabelEvent
                group by case_id
            ) cnt
            on LabelList.id = cnt.case_id
             '''
    cursor.execute(sql)
    print('成功创建LabelCount视图')


#原告证据和诉求的关系
def create_rel_plainev_ap(cursor):
    sql = '''drop table if exists rel_plainev_ap'''
    cursor.execute(sql)
    sql = ''' 
            create table rel_plainev_ap (
            num int not null auto_increment primary key,
            ev_id int not null,
            ap_id int not null,
            lb_id int not null
            )engine=innodb default charset=utf8;
            '''
    cursor.execute(sql)
    print('成功创建rel_plainev_ap数据库')

#被告证据和诉求的关系
def create_rel_defenev_ap(cursor):
    sql = '''drop table if exists rel_defenev_ap'''
    cursor.execute(sql)
    sql = ''' 
            create table rel_defenev_ap (
            num int not null auto_increment primary key,
            ev_id int not null,
            ap_id int not null,
            lb_id int not null
            )engine=innodb default charset=utf8;
            '''
    cursor.execute(sql)
    print('成功创建rel_defenev_ap数据库')

#原告证据和辩称的关系
def create_rel_plainev_ar(cursor):
    sql = '''drop table if exists rel_plainev_ar'''
    cursor.execute(sql)
    sql = ''' 
            create table rel_plainev_ar (
            num int not null auto_increment primary key,
            ev_id int not null,
            ar_id int not null,
            lb_id int not null
            )engine=innodb default charset=utf8;
            '''
    cursor.execute(sql)
    print('成功创建plainev_ar数据库')

#被告证据和辩称的关系
def create_rel_defenev_ar(cursor):
    sql = '''drop table if exists rel_defenev_ar'''
    cursor.execute(sql)
    sql = ''' 
            create table rel_defenev_ar (
            num int not null auto_increment primary key,
            ev_id int not null,
            ar_id int not null,
            lb_id int not null
            )engine=innodb default charset=utf8;
            '''
    cursor.execute(sql)
    print('成功创建rel_defenev_ar数据库')

#原告证据与被告证据的关系
def create_rel_plain_defen(cursor):
    sql = '''drop table if exists rel_plain_defen'''
    cursor.execute(sql)
    sql = ''' 
            create table rel_plain_defen (
            num int not null auto_increment primary key,
            plain_ev_id int not null,
            defen_ev_id int not null,
            lb_id int not null
            )engine=innodb default charset=utf8;
            '''
    cursor.execute(sql)
    print('成功创建rel_plain_defen数据库')

#诉求和辩称
def create_rel_ap_ar(cursor):
    sql = '''drop table if exists rel_ap_ar'''
    cursor.execute(sql)
    sql = ''' 
            create table rel_ap_ar (
            num int not null auto_increment primary key,
            ap_id int not null,
            ar_id int not null,
            lb_id int not null
            )engine=innodb default charset=utf8;
            '''
    cursor.execute(sql)
    print('成功创建rel_ap_ar数据库')

def rely(cursor):
    sql = '''
            alter table rel_plainev_ap add foreign key(ev_id) references PlaintiffEvidence(num);
            alter table rel_plainev_ap add foreign key(ap_id) references Appeal(num);
            alter table rel_defenev_ap add foreign key(ev_id) references DefendentEvidence(num);
            alter table rel_defenev_ap add foreign key(ap_id) references Appeal(num);
            
            
            alter table rel_plainev_ar add foreign key(ev_id) references PlaintiffEvidence(num);
            alter table rel_plainev_ar add foreign key(ar_id) references Argue(num);                      
            alter table rel_defenev_ar add foreign key(ev_id) references DefendentEvidence(num);
            alter table rel_defenev_ar add foreign key(ar_id) references Argue(num);   
            
            alter table rel_plain_defen add foreign key(plain_id) references PlaintiffEvidence(num);
            alter table rel_plain_defen add foreign key(defen_id) references DefendentEvidence(num);
            
            alter table rel_ap_ar add foreign key(ap_id) references Appeal(num);
            alter table rel_ap_ar add foreign key(ar_id) references Argue(num);
        '''
    cursor.execute(''' alter table rel_plainev_ap add foreign key(ev_id) references PlaintiffEvidence(num)''')
    cursor.execute('''  alter table rel_plainev_ap add foreign key(ap_id) references Appeal(num)''')
    cursor.execute('''  alter table rel_plainev_ap add foreign key(lb_id) references LabelEvent(num)''')
    cursor.execute('''alter table rel_defenev_ap add foreign key(ev_id) references DefendentEvidence(num)''')
    cursor.execute('''  alter table rel_defenev_ap add foreign key(ap_id) references Appeal(num)''')
    cursor.execute('''  alter table rel_defenev_ap add foreign key(lb_id) references LabelEvent(num)''')
    cursor.execute('''alter table rel_plainev_ar add foreign key(ev_id) references PlaintiffEvidence(num)''')
    cursor.execute(''' alter table rel_plainev_ar add foreign key(ar_id) references Argue(num); ''')
    cursor.execute('''  alter table rel_plainev_ar add foreign key(lb_id) references LabelEvent(num)''')
    cursor.execute(''' alter table rel_defenev_ar add foreign key(ev_id) references DefendentEvidence(num)''')
    cursor.execute('''  alter table rel_defenev_ar add foreign key(ar_id) references Argue(num)''')
    cursor.execute('''  alter table rel_defenev_ar add foreign key(lb_id) references LabelEvent(num)''')
    cursor.execute(''' alter table rel_plain_defen add foreign key(plain_ev_id) references PlaintiffEvidence(num);''')
    cursor.execute('''   alter table rel_plain_defen add foreign key(defen_ev_id) references DefendentEvidence(num);''')
    cursor.execute('''  alter table rel_plain_defen add foreign key(lb_id) references LabelEvent(num)''')
    cursor.execute('''   alter table rel_ap_ar add foreign key(ap_id) references Appeal(num);''')
    cursor.execute(''' alter table rel_ap_ar add foreign key(ar_id) references Argue(num);''')
    cursor.execute('''  alter table rel_ap_ar add foreign key(lb_id) references LabelEvent(num)''')

    cursor.execute('''  alter table AppealLabel add foreign key(ap_num) references Appeal(num)''')
    cursor.execute('''  alter table AppealLabel add foreign key(lb_id) references LabelEvent(num)''')
    return

def init(cursor):
    createCaseTable(cursor)
    createPlaintiffEvidence(cursor)
    createDefendentEvidence(cursor)
    createAppeal(cursor)
    createArgue(cursor)
    createFocus(cursor)
    createLabelList(cursor)
    createLabelEvent(cursor)
    createLabelCount(cursor)
    createAppealLabel(cursor)
    create_rel_plainev_ap(cursor)
    create_rel_defenev_ap(cursor)
    create_rel_plainev_ar(cursor)
    create_rel_defenev_ar(cursor)
    create_rel_plain_defen(cursor)
    create_rel_ap_ar(cursor)
    rely(cursor)

def process(str):
    if len(str) > 10000:
        str = str[:10000]
    return str

def Insert_LawCase(cursor): 
    sql = 'insert into LawCase(id,title,case_num,classification, source,court,judge,clerk,concerned,process,court_opinion,result)' \
          'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for Cases in Load_faxin_data('LawSeaV2/data/raw/faxin_v1').values():
        Case_List = []
        for case in Cases.items():
            lis = []
            lis.append(case[1]['ID'])
            lis.append(case[1]['标题'])
            if '案号' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(case[1]['案号'])
            lis.append(case[1]['案由'])
            lis.append('法信')
            lis.append(case[1]['审理法院'])
            if '审判人员' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(case[1]['审判人员'])
            if '书记员' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(case[1]['书记员'])
            if '当事人' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(case[1]['当事人'])
            if '审理经过' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(process(case[1]['审理经过']))

            if '本院认为' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(process(case[1]['本院认为']))
            if '裁判结果' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(process(case[1]['裁判结果']))
            Case_List.append(lis)
        cursor.executemany(sql,Case_List)
    for Cases in Load_openlaw_data('LawSeaV2/data/raw/openlaw_v1').values():
        Case_List = []
        for case in Cases.items():
            lis = []
            lis.append(case[1]['ID'])
            lis.append(case[1]['标题'])
            if '案号' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(case[1]['案号'])
            lis.append(case[1]['案由'])
            lis.append('OpenLaw')
            lis.append(case[1]['法院'])
            if '审判人员' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(case[1]['审判人员'])
            if '书记员' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(case[1]['书记员'])
            if '当事人' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(case[1]['当事人'])
            if '审理经过' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(process(case[1]['审理经过']))

            if '本院认为' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(process(case[1]['本院认为']))
            if '裁判结果' not in case[1].keys():
                lis.append('None')
            else:
                lis.append(process(case[1]['裁判结果']))
            Case_List.append(lis)
        cursor.executemany(sql,Case_List)

'''
    for file in os.listdir('faxin_v1'):
        path = os.path.join('faxin_v1/',file)
        Case_List = []
        f = open(path,'r',encoding='utf-8')
        Cases = json.load(f)
'''

def Insert_LabelList(cursor,filename):
    f = open(filename,'r',encoding='utf-8')
    ids = json.load(f)[:300]
    sql = 'insert into LabelList(id) values(%s)' 
    cursor.executemany(sql,ids)

def Insert_PlaintiffEvidence(cursor,filename):
    sql = 'insert into PlaintiffEvidence(id,evi) ' \
          'values(%s,%s)'
    file = open(filename,'r',encoding='utf-8')
    f = json.load(file)
    evi_list = []
    for Cases in f.values():
        for case in Cases.items():
            id = case[1]['ID']
            plaintiff_evidences = case[1]['原告']['原告证据']
            for evi in plaintiff_evidences:
                evi_list.append([id,pymysql.escape_string(evi)])
    cursor.executemany(sql,evi_list)

def Insert_DefendentEvidence(cursor,filename):
    sql = 'insert into DefendentEvidence(id,def) values(%s, %s)'

    file = open(filename,'r',encoding='utf-8')
    f = json.load(file)
    def_list = []
    for Cases in f.values():
        for case in Cases.items():
            id = case[1]['ID']
            Defendent_evidences = case[1]['被告']['被告证据']
            for defe in Defendent_evidences:
                def_list.append([id,defe])
    cursor.executemany(sql,def_list)

def Insert_Appeal(cursor,filename):
    sql = 'insert into Appeal(id,app) values(%s ,%s)'

    file = open(filename,'r',encoding='utf-8')
    f = json.load(file)
    app_list = []
    for Cases in f.values():
        for case in Cases.items():
            id = case[1]['ID']
            apps = case[1]['原告']['原告诉求']
            for app in apps:
                app_list.append([id, app])
    cursor.executemany(sql,app_list)

def Insert_Argue(cursor,filename):
    sql = 'insert into Argue(id,arg) values(%s ,%s)'

    file = open(filename,'r',encoding='utf-8')
    f = json.load(file)
    arg_list = []
    for Cases in f.values():
        for case in Cases.items():
            id = case[1]['ID']
            args = case[1]['被告']['被告辩称']
            for arg in args:
                arg_list.append([id, arg])
    cursor.executemany(sql,arg_list)

def Insert(cursor):
    Insert_LawCase(cursor)
    Insert_LabelList(cursor,'LawSeaV2/src/DataLabelingStage1/result_list.json')
    Insert_PlaintiffEvidence(cursor,'LawSeaV2/data/extract/stage1/法信_抽取.json')
    Insert_PlaintiffEvidence(cursor,'LawSeaV2/data/extract/stage1/Openlaw_抽取.json')

    Insert_DefendentEvidence(cursor,'LawSeaV2/data/extract/stage1/法信_抽取.json')
    Insert_DefendentEvidence(cursor,'LawSeaV2/data/extract/stage1/Openlaw_抽取.json')

    Insert_Appeal(cursor,'LawSeaV2/data/extract/stage1/法信_抽取.json')
    Insert_Appeal(cursor,'LawSeaV2/data/extract/stage1/Openlaw_抽取.json')

    Insert_Argue(cursor,'LawSeaV2/data/extract/stage1/法信_抽取.json')
    Insert_Argue(cursor,'LawSeaV2/data/extract/stage1/Openlaw_抽取.json')



if __name__ == '__main__':
    # 创建数据表
    # 创建连接
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='icstwip')

    # 创建游标
    cursor = conn.cursor()
    # cursor.execute('''use Label_multiple''')

    
    cursor.execute('''drop database if exists Label_multiple''')
    cursor.execute('''create database if not exists Label_multiple''')
    cursor.execute('''use Label_multiple''')
    
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')

    init(cursor)
    Insert(cursor)
    conn.commit()
    
    sql = '''select num from PlaintiffEvidence where id ='FaxinClass1_id5' '''
    cursor.execute(sql)
    data = cursor.fetchall()
    print(len(data))
    print(data)
    sql = '''select count(*) from LabelCount where count > 0'''
    cursor.execute(sql)
    print(cursor.fetchall()[0][0])
