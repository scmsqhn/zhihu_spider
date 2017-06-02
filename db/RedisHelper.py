# coding:utf-8
from __future__ import unicode_literals
import time

#from redis import Redis
import redis
#import config
from ISqlHelper import ISqlHelper
from SqlHelper import Proxy

import codecs
import chardet

class RedisHelper(ISqlHelper):

    ''''' 初始化redis数据库，建立链接
    arg0：localhost ip地址 本地主机 
    arg1：6379 端口号 默认值 
    arg2：0 数据库 编号
    '''
    def __init__(self, arg0='0', arg1='localhost', arg2='6379'):
      
      self.r = redis.StrictRedis(db=arg0,host=arg1,port=arg2)
      
    ''''' HASHSET 散裂添加操作
    arg0：HASHSET 名称
    arg1：KEY 键
    arg2：VALUE 值
    '''
    def hset(self,arg0,arg1,arg2):
      self.r.hset(arg0,arg1,arg2)
      
    def srandmember(self,arg0):
      return self.r.srandmember(arg0, arg1)

    def sismember(self,arg0,arg1):
      return self.r.sismember(arg0,arg1)
  
    def hexists(self, arg0, arg1):
      return self.r.hexists(arg0, arg1)

    ''''' LIST 列表 左侧 添加操作
    arg0：LIST 名称
    arg1：VALUE 值
    '''
    def lpush(self,arg0='test',arg1='1'):
      self.r.lpush(arg0,arg1)

    ''''' LIST 列表 左侧 添加操作
    arg0：LIST 名称
    '''
    def lpull(self,arg0='test'):
      self.r.lpull(arg0)
          
    ''''' LIST 列表 右侧 添加操作
    arg0：LIST 名称
    arg1：VALUE 值
    '''
    def rpush(self,arg0,arg1):
      self.r.rpush(self,arg0,arg1)

    def drop_db(self):
      return self.r.flushdb()

    ''''' 获得所有的 KEYS
    '''
    def get_all_keys(self):
      return self.r.keys()
      
    def type(self,key):
      return self.r.type(key)

    def get(self,key):
#      print('key=', key)
      typeflag = self.r.type(key)
      typeflag = str(typeflag)
#      print('typeflag=', typeflag)
      if(typeflag=='hash'):
#        print('self.r.hgetall(key)', self.r.hgetall('linkstarget'))
#        print('self.r.hgetall(key)', self.r.hgetall(key))
        return self.r.hgetall(key)
      if(typeflag=="b'list'"):
        size=self.r.llen(key)
        return self.r.lrange(key,0,size)
        

    def simple_show(self):
      sqlhelper = RedisHelper()
      sqlhelper.init_db('redis://localhost:6379/9')
      proxy = {'ip': '192.168.1.1', \
      'port': 80, \
      'type': 0, \
      'protocol': 0, \
      'country': u'中国','area': u'广州', \
      'speed': 11.123,\
      'types': 1}
      
      proxy2 = {'ip': 'localhost', \
      'port': 433, \
      'type': 1, \
      'protocol': 1,'country': u'中国','area': u'广州', \
      'speed': 123,\
      'types': 0, \
      'score': 100}
      assert sqlhelper.insert(proxy) == True
      assert sqlhelper.insert(proxy2) == True
      assert sqlhelper.get_keys({'types': 1}) == ['proxy::192.168.1.1:80:0', ],sqlhelper.get_keys({'types': 1})
      assert sqlhelper.select(conditions={'protocol': 0})==[('192.168.1.1', '80', '0')]
      assert sqlhelper.update({'types': 1}, {'score': 888}) == 1
      assert sqlhelper.select() == [('192.168.1.1', '80', '888'), ('localhost', '433', '100')]
      # assert sqlhelper.delete({'types': 1}) == 1
      # sqlhelper.drop_db()
      print('All pass.')

if __name__ == '__main__': 
  redishelper=RedisHelper()
  redishelper.lpush('test')
  for key in redishelper.get_all_keys():
    print(redishelper.get(key))
