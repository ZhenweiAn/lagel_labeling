# legal_labeling

#### 2020/8/3

+ 修改了/chain死循环的问题，加入了对于IndexError的异常处理，即直接返回"IndexError"的字符串。

+ 记录标注者信息
  + 为了方便不同的用户标同一个数据，数据库加了一个表labelevent, 每条记录了标注者id和案子id，标注的各项内容都加了一列eventid(其中原来的appeal表中同时包含文本和label，没法标记多个标签，现在拆开成两个表了)
  + web中的REQUIRE_NUM表示一个案件需要被几个人标注。分配案件时选择没有被足够人标注过，且当前标注者没有标过的案件。
  + 在/next, /chain, /commit三个地方都接收了一个“labeller_id”的字段，用来确定标注者身份

#### 2020/8/4

+ /chain的返回格式改为

  ```
  {
  	'status': 'success'
  	'chains': chains
  }
  {
  	'status': 'IndexError'
  	'chains': []
  }
  ```




+ update:

  将前端用到的服务器上的资源下载到本地，方便本地调试。

  注意：为了当前版本能正常运行，\chain的返回格式还是一个列表，请在js中做出对应修改后(接受dict)将`web.py`第385行`res = chains`注释掉
  
  

#### 本地运行此项目：

  1. 将LawSeaV2文件夹用海事法律项目-v2.0替换
  2. 把`dataset.py`和`web.py`中的连接数据库中的MySQL数据库密码改成本地的密码
  3. 安装依赖库，依次执行`python database.py`，`python web.py`
  4. 访问`http://localhost:8080/tagging#
