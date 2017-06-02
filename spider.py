#!/usr/bin/env python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import json
from bs4 import BeautifulSoup
import util.request as myrequest
import requests
#import request
import redis
from lxml import html
import lxml.etree as etree
from multiprocessing.dummy import Pool
from mongodbs import Zhihu_User_Profile

import lxml.html.soupparser as soupparser
import lxml.etree as etree
import json
from db.RedisHelper import RedisHelper
from db.MongoHelper import MongoHelper
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
import traceback
'''
爬虫核心逻辑 
'''

class Spider():

    def __init__(self,url,option="print_data_out"):
        print('__init__ a new spider')
        self.url=url
        self.option=option
        self.header={}
        self.user_name= 'None'
        self.user_gender= -1
        self.user_location= 'None'
        self.user_be_agreed= -1
        self.user_be_thanked= -1
        self.user_followers= -1
        self.user_followees= []
        self.user_employment= 'None'
        self.user_employment_extra= 'None'
        self.user_education_school= 'None'
        self.user_education_subject= 'None'
        self.user_info= 'None'
        self.user_intro= 'None'

        self.cookies={
        "d_c0":"AEBCv9kp3wqPThX5-xvBlSRK_wv2n9FVluE=|1479554939",
        "q_c1":"fccdcdda878341bb90d9be8b6b85714c|1494056623000|1479554939000", "aliyungf_tc":"AQAAAE6t6ANgOQ0AImaKtphtJYkKrwP8", 
        "acw_tc":"AQAAAAVYWg7AjQ4AImaKtsvHBzK//Frf", 
        "_xsrf":"f77c02fe84166f3ed779323579da866e", 
        "r_cap_id":"NzljNDBlOTgzYzhjNGUwYWExZGI5OGZkOGI2OTc1ZWM=|1496281338|def57f9de2bbc3185f7e517e4eb3045cae353442", 
        "cap_id":"M2QzYzVlM2ZmZGZlNDA4MmIzYzYyMDdmNzkxMjExNmI=|1496281337|f9ae465ca93c81bf1f39df7bb33305565df72764", 
        "_zap":"4ccc31d7-7df3-4b2d-b319-03b4d7cf56bd", 
        "__utma":"51854390.356292377.1479554881.1494607910.1496281071.15", "__utmc":"51854390", 
        "__utmz":"51854390.1496281071.15.15.utmcsr=baidu|utmccn=(organic)|utmcmd=organic", 
        "__utmv":"51854390.000--|3=entry_date=20161119=1", 
        "z_c0":"Mi4wQUFCQUpyWVpBQUFBUUVLXzJTbmZDaGNBQUFCaEFsVk5BUDVXV1FCamdhUVBwb2RNUlZodHhPUklYN1AzbVlEMVVn|1496284713|1bf18422d3810bc5950b3257076522a408b32a65"
        }

    def get_user_data(self):

        print self.url
        followee_url=self.url+"/following"
        print('get_user_data.followee_url', followee_url)
        try:
            '''''
            不可以将verify 设置为 False会报错
            insecurerequestwarnning
            将网络访问修改为proxy+headers模式
            '''
            opener=myrequest.makeMyOpener()
            response=opener.open(followee_url, timeout=1000)
            get_html= response.read()
#            print(response)
#            print(get_html)
            #get_html=requests.get(followee_url,cookies=self.cookies,
#                                headers=self.header,verify=True)
        except:
            traceback.print_exc()
            print "requests get error!"
            return
#        content=get_html.text
        content=get_html
        #print(u'访问 get_html.status_code: ', response.status_code)
        if True:#response.status_code==200:
            self.analy_profile(content)
            return

    def get_xpath_source(self,source):
        if source:
            return source[0]
        else:
            return ''
            
    def bs4demo(self, soup):
        #print soup.prettify()  
        print soup.title   #输出<title>标签  
        print len(soup.title)  
        print soup.head    #输出<head>标签  
        print len(soup.head)  
        print soup.a       #输出<a>标签  
        print len(soup.a)  
        print type(soup.a) #输出<a>标签的类型  
        print soup.p       #输出<p>标签  
        try:
          print soup.p.attrs #把 p 标签的所有属性打印输出  
        except AttributeError:
          traceback.print_exc()

        print soup.name  
        print soup.head.name  
    #NavigableString  
        try:
          print soup.p.string  #用.string方法获取标签里面的内容  
        except AttributeError:
          traceback.print_exc()
        print type(soup.p.string)   #判断类型输出  
    #BeautifulSoup对象表示的是一个文档的全部内容  
        print type(soup.name)    #获取soup名字的类型  
        print soup.name  
        print soup.attrs  
    #Comment 对象是一个特殊类型的 NavigableString 对象，其实输出的内容仍然不包括注释符号  
        print soup.a  
        print soup.a.string  
        print type(soup.a.string)  
    #熟悉.contents.children属性，tag 的 .content 属性可以将tag的子节点以列表的方式输出  
        print soup.head.contents   
        print soup.head.children  
    #.contents 和 .children 属性仅包含tag的直接子节点，.descendants 属性可以对所有tag的子孙节点进行递归循环  
        for child in soup.descendants:  
            print child  
    #.strings获取多个内容，不过需要遍历获取  
        for string in soup.strings:  
            print(repr(string))  
    #.stripped_strings输出的字符串中可能包含了很多空格或空行,使用 .stripped_strings 可以去除多余空白内容  
        for string in soup.stripped_strings:  
            print(repr(string))  
    # .parent 属性  
        print soup.p.parent.name  
    #.next_sibling .previous_sibling 属性  
        for sibling in soup.a.next_siblings:  
            print(repr(sibling))  
    #.next_element .previous_element 属性,输出当前节点前一个节点或者下一个节点  
        print soup.head.next_element  
    #搜索文档树find_all( name , attrs , recursive , text , **kwargs )find_all() 方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件  
        print soup.find_all(['a','b'])  #查找所有的a标签  
        soup.find_all("a", limit=2)    #可以限制返回的数量  

        
    '''''
    获得所有 div 的 class:
    ['LoadingBar', 'AppHeader-inner', 'SearchBar', 'SearchBar-toolWrapper', 'Popover', 'SearchBar-input Input-wrapper Input-wrapper--grey', 'Input-after', 'AppHeader-userInfo', 'AppHeader-profile']
    
    '''
    '''''
    使用xpath解析html
    html解析
    http://blog.csdn.net/together_cz/article/details/56036978
    '''
    def analy_profile(self,html_text):
        if red.sismember('red_had_spider',self.url):
          print '已经爬取过的, ', self.url
          return
        print('analy_profile enter')
        import json
        #tree = soupparser.fromstring(html_text)
        #tree= etree.tostring(dom)
        soup= BeautifulSoup(html_text)
        #print tree.prettify()
        data= soup.find('div', {'id': 'data'})
        datastate= data['data-state']
        users= json.loads(data['data-state'])['entities']['users']
        #print datastate.encode('utf-8')
        self.user_name=self.url.split('/')[-1]
        print self.user_name
        try:
          self.user_followers= jsloads(data['data-state'])['entities']['users'][self.user_name]["followingCount"]
        except:
          pass
        try:
          self.user_education_school= jsloads(data['data-state'])['entities']['users'][self.user_name]["educations"][0]['school']['name']
        except:
          pass
        try:
          self.user_be_thanked= jsloads(data['data-state'])['entities'][ 'users'][self.user_name]["thankedCount"]
        except:
          pass

        try:
          self.user_location= jsloads(data['data-state'])['entities']['users'][self.user_name]["locations"][0]["name"]
        except:
          pass

        try:
          self.user_gender= jsloads(data['data-state'])['entities']['users'][self.user_name]["gender"]
        except:
          pass

        try:
          self.user_employment= jsloads(data['data-state'])['entities']['users'][self.user_name]["employments"][0]["company"]["name"]
        except:
          pass

        try:
          self.user_employment_extra= jsloads(data['data-state'])['entities']['users'][self.user_name]["employments"][0]["job"]["name"]
        except:
          pass

        try:
          self.user_be_agreed= jsloads(data['data-state'])['entities']['users'][self.user_name]["favoriteCount"]
        except:
          pass

        try:
          self.user_info= jsloads(data['data-state'])['entities']['users'][self.user_name]["description"]
        except:
          pass

          
        try:
          self.user_intro= jsloads(data['data-state'])['entities']['users'][self.user_name]["business"]["name"]
        except:
          pass

        self.user_followees= []
        try:
          allUsers= jsloads(data['data-state'])['entities']['users']
        except:
          pass

        for key in allUsers.keys():
          if not key==self.user_name:
            target_url = self.obtainUrl(jsloads(data['data-state'])['entities']['users'][key])

            red.lpush('red_to_spider',target_url)
            self.user_followees.append(jsloads(data['data-state'])['entities']['users'][key])
                
        for page in range(2,100):
          '''''
          ex. https://www.zhihu.com/people/libing/following?page=2
          '''
          followee_url=self.url+"/following?page=%d" % page
          print('followee_url', followee_url)
          opener=myrequest.makeMyOpener()
          try:
            response=opener.open(followee_url, timeout=1000)
          except:
            traceback.print_exc()
            print '没有下一页'
            break
          html_text= response.read()
          soup= BeautifulSoup(html_text)
          data= soup.find('div', {'id': 'data'})
          allUsers= json.loads(data['data-state'])['entities']['users']
          if (len(allUsers.keys())<2):# 页面没有关注者
            pass
            print('len(allUsers.keys()', len(allUsers.keys()))
            print '没有下一页'
            break
          else:  
            print('len(allUsers.keys()', len(allUsers.keys()))
            for key in allUsers.keys():
              print('key= ' , self.user_name)
              if not key==self.user_name:
                target_url = self.obtainUrl(json.loads(data['data-state'])['entities']['users'][key])
                self.user_followees.append(json.loads(data['data-state'])['entities']['users'][key])
        
        if self.option == "print_data_out":
            self.print_data_out()
        else:
            self.store_data_to_mongo()
            red.sadd('red_had_spider',self.url)
            
    def obtainUrl(self, user):
      url= ("https://www.zhihu.com/%s/%s"%(user['type'], user['urlToken']))
      print url 
      return url

    
    def print_data_out(self):

        print "*" * 60
        print '用户名:%s\n' % (self.user_name)
        print "用户性别:%s\n" % (self.user_gender)
        print '用户地址:%s\n' % (self.user_location.encode('utf-8'))
        print "被同意:%s\n" % (self.user_be_agreed)
        print "被感谢:%s\n" % (self.user_be_thanked)
        print "被关注:%s\n" % (self.user_followers)
        print "关注了:%s\n" % (self.user_followees)
        print "工作:%s/%s" % ((self.user_employment, self.user_employment_extra))
        print "教育:%s/%s" % ((self.user_education_school, self.user_education_subject))
        print "用户信息:%s" % (self.user_info)
        print "*" * 60


    def store_data_to_mongo(self):
        mongohelper=MongoHelper("zhihu_db", "zhihu_coll")
        mongohelper.select_colletion("zhihu_coll")
        itemdict={}
        itemdict['user_name']= self.user_name
        itemdict['user_be_agreed']= self.user_be_agreed
        itemdict['user_be_thanked']=self.user_be_thanked
        itemdict['user_followees']=self.user_followees
        itemdict['user_followers']=self.user_followers
        itemdict['user_education_school']=self.user_education_school
        itemdict['user_education_subject']=self.user_education_subject
        itemdict['user_employment']=self.user_employment
        itemdict['user_employment_extra']=self.user_employment_extra
        itemdict['user_location']=self.user_location
        itemdict['user_gender']=self.user_gender
        itemdict['user_info']=self.user_info
        itemdict['user_intro']=self.user_intro
        itemdict['user_url']=self.url
        mongohelper.insert(itemdict)
        print "saved: %s \n" %self.user_name

#　核心模块,bfs宽度优先搜索
def BFS_Search(option):
    global red
    while True:
        temp=red.rpop('red_to_spider')
        print('BFS_Search.temp= ', temp)
        if type(temp)==None:
            print 'SCANNING OVER 所有URL读取完毕'
            break
        result=Spider(temp,option)
        result.get_user_data()

    return "ok"
    
def jsloads(input):
  try:
    return json.loads(input)
  except:
    traceback.print_exc()
    return ''

def list_all_dict(dict_a):
    #print(u'dict_a type is, ' , type(dict_a))
    if isinstance(dict_a,dict) : #使用isinstance检测数据类型
        for x in range(len(dict_a)):
            temp_key = dict_a.keys()[x]
            temp_value = dict_a[temp_key]
            try:
              print("%s : %s " %(temp_key,temp_value))
              #print("%s \n" % temp_key)
            except UnicodeEncodeError:
              print('UnicodeEncodeError')
            list_all_dict(temp_value) #自我调用实现无限遍
            
            
    
    
if __name__=='__main__':
    try:
        '''''
        sys.argv[1]的用法
        传参
        '''
        option=sys.argv[1]
    except:
        traceback.print_exc()
        print 'argv is not accepted'
        sys.exit()
    red=redis.Redis(host='127.0.0.1',port=6379,db=0)
    print('链接redis数据库\n')
    red.lpush('red_to_spider',"https://www.zhihu.com/people/tan-hai-ning")
    print('将数据写入list red_to_spider 左侧压入\n')
    BFS_Search(option)

    #使用多进程，注意，实际测试出来，并没有明显速度的提升,瓶颈在IO写;如果直接输出的话,速度会明显加快
    '''
    res=[]
    process_Pool=Pool(4)
    for i in range(4):
        res.append(process_Pool.apply_async(BFS_Search,(option, )))

    process_Pool.close()
    process_Pool.join()

    for num in res:
        print ":::",num.get()
    print 'Work had done!'
    '''







