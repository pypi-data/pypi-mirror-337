# MCSM-C
---------
## 这是什么库
这是一个用来控制mcsm面板(主要针对我的世界服务器)的库
## 安装
```bash
pip install mcsmc
```
## 使用
```python
from mcsmc import Mcsmc
mcsm=Mcsm_ctrl(url="你的mcsm面板url",token="你的mcsm面板token")
#接下来:功能介绍
mcsm.get_server_list(de_id="节点id",page=1,page_size=10) #获取服务器列表(page默认1,page_size默认10) return:tuple(执行成功?,返回结果->dict)
mcsm.start(server_id="实例id", de_id="节点id") #启动服务器 return:tuple(执行成功?,返回结果->dict)
mcsm.q_restart(server_id="实例id", de_id="节点id") #强制重启服务器 return:tuple(执行成功?,返回结果->dict)
mcsm.get_log(self, server_id="实例id", de_id="节点id", size=200) #获取日志(size默认200) return:tuple(执行成功?,返回结果->str(执行成功)|err or dict(执行失败))
```
## 注意
- 这是一个测试版,可能会有bug,请自行测试
- 这是一个测试版,可能会有bug,请自行测试
- 这是一个测试版,可能会有bug,请自行测试
！！重要的话说3遍！！