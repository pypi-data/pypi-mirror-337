'''
author: xiaoliang(pen name)
QQ: 2700858939
updata_time: 2025/03/27
----分界线----
作者: xiaoliang(笔名)
QQ: 2700858939
更新时间: 2025/03/27
'''
import requests,json
had = {
    "Content-Type":"application/json; charset=utf-8",
    "X-Requested-With":"XMLHttpRequest"
}
class Mcsm_ctrl():
    def __init__(self, url, token):
        '''
        mcsm控制初始化
        url:mcsm地址
        token:mcsm的token
        :param url:
        :param token:
        '''
        self.url = url
        self.token = token
    def get_server_list(self,de_id,page=1,page_size=10)->tuple:
        '''
        获取实例列表
        de_id:节点id
        page:页码
        page_size:每页数量
        :param de_id:
        :param page:
        :param page_size:
        :return:->tuple
        '''
        #/api/service/remote_service_instances
        url = self.url + "/api/service/remote_service_instances?apikey="+self.token+"&daemonId="+de_id+"&page="+str(page)+"&pageSize="+str(page_size)
        data = {
            "daemonId":de_id,
            "page":page,
            "pageSize":page_size
        }
        res = requests.get(url, data=json.dumps(data), headers=had)
        if res.json()["status"] == 200:
            return (True,res.json()["data"])
        else:
            return (False,res.text)
    def start(self, server_id, de_id)->tuple:
        '''
        启动
        server_id:实例id
        de_id:节点id
        :param server_id:
        :param de_id:
        :return:->tuple
        '''
        #GET /api/protected_instance/open
        url = self.url + "/api/protected_instance/open?apikey="+self.token+"&uuid="+server_id+"&daemonId="+de_id
        data = {
            "uuid":server_id,
            "daemonId":de_id
        }
        res = requests.get(url, data=json.dumps(data), headers=had)
        if res.json()["status"] == 200:
            return (True,res.json()["data"])
        else:
            return (False,res.text)
    def q_restart(self, server_id, de_id)->tuple:
        '''
        强制重启
        server_id:实例id
        de_id:节点id
        :param server_id:
        :param de_id:
        :return:->tuple
        '''
        url = self.url + "/api/protected_instance/kill?apikey="+self.token+"&uuid="+server_id+"&daemonId="+de_id
        data = {
            "uuid":server_id,
            "daemonId":de_id
        }
        res = requests.get(url, data=json.dumps(data), headers=had)
        if res.json()["status"] == 200:
            #启动
            #GET /api/protected_instance/open
            url = self.url + "/api/protected_instance/open?apikey="+self.token+"&uuid="+server_id+"&daemonId="+de_id
            data = {
                "uuid":server_id,
                "daemonId":de_id
            }
            res = requests.get(url, data=json.dumps(data), headers=had)
            if res.json()["status"] == 200:
                return (True,res.json()["data"])
            else:
                return (False,res.json()["data"])
        else:
            return (False,res.json()["data"])
    def get_log(self, server_id, de_id, size=200)->tuple:
        '''
        获取日志
        server_id:实例id
        de_id:节点id
        :param server_id:
        :param de_id:
        :return:->tuple
        '''
        url = self.url + "/api/protected_instance/outputlog?apikey="+self.token+"&uuid="+server_id+"&daemonId="+de_id+"&size=100"
        data = {
            "uuid":server_id,
            "daemonId":de_id,
            "size":200
        }
        res = requests.get(url, data=json.dumps(data), headers=had)
        if res.json()["status"] == 200:
            return (True,res.json()["data"])
        else:
            return (False,res.json()["data"])