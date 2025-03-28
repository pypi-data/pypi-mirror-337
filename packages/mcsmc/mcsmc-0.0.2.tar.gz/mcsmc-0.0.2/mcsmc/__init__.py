'''
author:xiaoliang
copyright (c) 2025 by xiaoliang
This is a mcsm control library.
help part one(import):
import mcsmc.Mcsm as Mcsm
help part two(initialization):
mcsm=Mcsm.Mcsm_ctrl(url="your mcsm panel url",token="your mcsm panel token")
help part three(functions):
mcsm.get_server_list(de_id="node id",page=1,page_size=10) #get server list(page default 1,page_size default 10) return:tuple(execution successful?,return result->dict)
mcsm.start(server_id="instance id", de_id="node id") #start server return:tuple(execution successful?,return result->dict)
mcsm.q_restart(server_id="instance id", de_id="node id") #force restart server return:tuple(execution successful?,return result->dict)
mcsm.get_log(self, server_id="instance id", de_id="node id", size=200) #get log(size default 200) return:tuple(execution successful?,return result->str(execution successful)|err or dict(execution failed))
----分界线----
作者:xiaoliang
版权所有 (c) 2025 由 xiaoliang 保留
这是一个mcsm的控制库
help第一部分(导入):
import mcsmc.Mcsm as Mcsm
help第二部分(初始化):
mcsm=Mcsm.Mcsm_ctrl(url="你的mcsm面板url",token="你的mcsm面板token")
help第三部分(函数):
mcsm.get_server_list(de_id="节点id",page=1,page_size=10) #获取服务器列表(page默认1,page_size默认10) return:tuple(执行成功?,返回结果->dict)
mcsm.start(server_id="实例id", de_id="节点id") #启动服务器 return:tuple(执行成功?,返回结果->dict)
mcsm.q_restart(server_id="实例id", de_id="节点id") #强制重启服务器 return:tuple(执行成功?,返回结果->dict)
mcsm.get_log(self, server_id="实例id", de_id="节点id", size=200) #获取日志(size默认200) return:tuple(执行成功?,返回结果->str(执行成功)|err or dict(执行失败))
'''