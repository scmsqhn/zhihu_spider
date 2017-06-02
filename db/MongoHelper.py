#coding:utf-8
#encoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo

from config import DB_CONFIG, DEFAULT_SCORE
from ISqlHelper import ISqlHelper
import traceback
import json
import time
import re
import traceback
import math
import codecs
import random

def wash(string):
  string = re.sub(r"[\'\`\{\}\"\[\]\.\-\;\*\/\=]", " ", string)
  string = re.sub(r"[%\~\^\_\\]", " ", string)
#  string = re.sub(r"  ", " ", string)
#  string = re.sub("[、？，。！～]", " ", string)
#  string = re.sub(r"\'s", " \'s", string)
  string = re.sub(r"\r", "", string)
  string = re.sub(r"\n", "", string)
  string = re.sub(r"\'ve", " \'ve", string)
  string = re.sub(r"n\'t", " n\'t", string)
  string = re.sub(r"\'re", " \'re", string)
  string = re.sub(r"\'d", " \'d", string)
  string = re.sub(r"\'ll", " \'ll", string)
  string = re.sub(r",", " , ", string)
  string = re.sub(r"!", " ! ", string)
  string = re.sub(r"\(", " \( ", string)
  string = re.sub(r"\)", " \) ", string)
  string = re.sub(r"\?", " \? ", string)
  string = re.sub(r"\s{2,}", " ", string)
  string = re.sub(r" ", "", string)
  return string

class MongoHelper(ISqlHelper):
    '''''初始化MongoHelper
    '''
    def __init__(self, db, coll):
      self.connection = pymongo.MongoClient('localhost:27017', connect=False)
      self.db=self.connection.get_database(db)
      self.collection=self.db.get_collection(coll)
      #print(self.connection)
      #print(self.db)
      #print(self.collection)

    '''''初始化MongoHelper 数据库
    '''
    def init_db(self,arg0):
      print('====')
      print("init_db")
      self.db=self.connection[arg0]
#      print(self.db)

    '''''初始化 数据库内 集合
    '''
    def select_colletion(self,coll):
      self.collection=self.db.get_collection(coll)

    '''''丢弃 数据库内 集合
    '''
    def drop_db(self,arg0):
        self.connection.drop_database(arg0)

    '''''插入 数据
    '''
    def insert(self, value=None):
      if value:
        try:
          print(value)
          r = self.collection.insert_one(value)
          print(r)
          return(r)
        except:
          print("====")
          print(value)
          traceback.print_exc()
          time.sleep(3)

    '''''获得 数据
    '''
    def findOne(self, value=None):
      if value:
        try:
          print(value)
          print(self.collection)
          r = self.collection.find_one()
          print(r)
          return(r)
        except:
          print("====")
          print(value)
          traceback.print_exc()
          time.sleep(3)

    '''''获得任意数据
    '''
    def findAnyOne(self, value=None):
      if value:
        try:
          try:
            count = random.randint(1,30)
          except:
            count = random.randint(1,30)
          items = self.collection.find({}, limit=count).sort(
            [("_id", pymongo.ASCENDING)])
          results = []
          for item in items:
            result = item
            results.append(result)
          print count,  len(results)
          return results[random.randint(0, count-1)]
          print results[random.randint(0, count-1)]
        except:
          print("====")
          print(value)
          traceback.print_exc()
          time.sleep(3)

    '''''删除 数据
    '''
    def delete(self, conditions=None):
      if conditions:
        self.proxys.remove(conditions)
        return ('deleteNum', 'ok')
      else:
        return ('deleteNum', 'None')

    def update(self, conditions=None, value=None):
        # update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
        if conditions and value:
            self.proxys.update(conditions, {"$set": value})
            return {'updateNum': 'ok'}
        else:
            return {'updateNum': 'fail'}

    def select(self, count=None, conditions=None):
        print('select')
        if count:
            count = int(count)
            print(count)
        else:
            count = 0
            print(count)
        if conditions:
            print(conditions)
            conditions = dict(conditions)
            conditions_name = ['types', 'protocol']
            for condition_name in conditions_name:
                value = conditions.get(condition_name, None)
                if value:
                    conditions[condition_name] = int(value)
        else:
            print(conditions)
            conditions = {}
        items = self.collection.find(conditions, limit=count).sort(
            [("_id", pymongo.ASCENDING)])

        results = []
        for item in items:
            result = item
            results.append(result)
        return results

    def get_ip_req_addr(self):
        mongohelper.select_colletion("ip_addr_req")
        with open('../ip2locate/output_ip_addr2.txt','r') as f:
          lines=f.readlines()
          for line in lines:
            #print(line)
            wds=line.split(',')
            #[print(wd) for wd in wds]
            dict={}
            dict['req_ip']=wds[0]
            dict['start']=wds[1]
            dict['stop']=wds[2]
            dict['country']=wds[3]
            dict['prov']=wds[4]
            dict['city']=wds[5]
            dict['net']=wds[6]
            mongohelper.insert(dict)    

    def push_lianjia_ershoufang_msg(self):
        with open('/zhicheng/cdesf.json','r') as f:
          lines=f.readlines()
          #print(type(lines))
          dict={}
          for line in lines:
            #print(type(line))
            line=json.loads(line)
            #print(type(line))
            for li in line:
              dict[li]=line[li]
            a=self.insert(dict)
            
    def push_58_zufang_msg(self):
      with open('/disk200g/hn/yunying/db/58data2.txt','r') as f:
        lines=f.readlines()
        for line in lines:
          try:
  #          line=re.sub("\D","",line)
            line=re.sub("元/月","",line)
            line=re.sub("-","",line)
            line=re.sub(r"[(,),\\,\,|]","",line)
            line=re.sub(r"[\r\n,\n]","",line)
            words=line.split(" ")
            cccc=0
            dict={}
            list=[]
            for word in words:
              word=re.sub(r" ","",word)
              word=re.sub(r"\r\n","",word)
              word=re.sub(r"\n","",word)
              if(word!=""):
                list.append(word)
                print('====')
                print(cccc)
                print(word)
                cccc=cccc+1
            dict['isdivded']=list[0]
            dict['area']=list[1]
            dict['name']=list[2]
            dict['struct']=list[3]
            dict['sqr']=list[4]
            dict['areaname']=list[5]
            dict['subway']=list[6]
            string=re.sub("\d","",list[7])
            string=re.sub("今天","",string)
  #          #print(string)
            string=re.sub("\D","",list[7])
            dict['price']=string
          except:
#            print(line)
            traceback.print_exc()
            continue
          a=self.insert(dict)

          
    def get_file_from_db(self):
        getall=self.collection.find()
        out_dict={}
        mongohelper.select_colletion("cdlj_data_divide")
        for getone in getall:
          try:
            dict={}
#            print(getone)
            try:
              mipri=int(getone['mipri'].split('价')[1].split('元')[0])
            except:
              traceback.print_exc()
              print(getone)
            try:
              hiorlo=(getone['build'].split('(')[0])
            except:
              pass
            price=getone['price']
            apartment=getone['house'].split('|')[0].strip()
            struct=getone['house'].split('|')[1].strip()
            sqr=getone['house'].split('|')[2].split('平')[0].strip()
            direction=getone['house'].split('|')[3].strip()
            try:
              state=getone['house'].split('|')[4].strip()
            except:
              state="其他"
            try:
              lift=getone['house'].split('|')[5].strip()
            except:
              lift="其他"
            eyeson=getone['buyer'].split('/')[0].split('人')[0].strip()
            visit=getone['buyer'].split('/')[1].split('共')[1].split('次')[0].strip()
            try:
              area=getone['build'].split(' ')[2].strip()
            except:
              print(getone)
              area="其他"
            dict['mipri']=mipri
            dict['hiorlo']=hiorlo
            dict['price']=price.split(r"\.")[0]
            dict['apartment']=apartment
            dict['struct']=struct
            try:
              dict['sqr']=math.floor(float(sqr))
            except:
              dict['sqr']=0
            dict['direction']=direction
            dict['state']=state
            dict['lift']=lift
            dict['eyeson']=eyeson
            dict['visit']=visit
            dict['area']=area
            for item in dict.keys():
              item=item.split("\..*")[0]
#              print(dict[item])
              if dict[item] in out_dict:
                out_dict[str(dict[item])]=out_dict[str(dict[item])]+1
              else:
                out_dict[str(dict[item])]=1
#              print(out_dict[str(dict[item])])
#            mongohelper.insert(dict)
 #           print('mongohelper.insert(dict)')
          except KeyError:
            print("continue")
            continue
            
    def cal_the_data(self):
      mongohelper.select_colletion("cdlj_data_divide")
      getall=self.collection.find()
      out_dict={}
      mongohelper.select_colletion("cdlj_analaysis")
      for getone in getall:
        for item in getone:
#          print(item)
 #         print(type(item))
  #        print(getone[item])
          item = str(getone[item]).split(r".")[0]
   #       print(item)
          if item in out_dict.keys():
            out_dict[item]=+1
          else:
            out_dict[item]=1
      for key in out_dict.keys():
          if "58f9d" in key:
            continue
          kv={}
          kv[key]=out_dict[key]
          mongohelper.insert(kv)
      
    def insert_file_2_db(self,db,collections,file,encode,dividechar):
      once=True
      print("new mongohelper")
      mongohelper.init_db(db)
      mongohelper.select_colletion(collections)
      f=codecs.open(file,'r',encode)
      lines=f.readlines()
      name,value="",""
      for line in lines:
        if(once):
          once=False
          _li1=line.split(dividechar)
          name = wash(_li1[0])
          value = wash(_li1[1])
          continue
        dict={}
        _li2=line.split(dividechar)
        dict[name] = wash(_li2[0])
        dict[value] = int(wash(_li2[1]))
        mongohelper.insert(dict)
    
    def MongoExport(self,count,condition):
      print("MongoExport")
      result= self.select(count,condition)
      targetItems=[]
      targetItem={}
      for item in result:
        if(item.has_key('Num')):
          targetItem['Num']=item['Num']
        elif(item.has_key('ProvAndCity')):
          targetItem['ProvAndCity']=item['ProvAndCity']
        elif(item.has_key('net')):
          targetItem['net']=item['net']
        elif(item.has_key('CityNum')):
          targetItem['CityNum']=item['CityNum']
        elif(item.has_key('MailNum')):
          targetItem['MailNum']=item['MailNum']
        if(len(targetItem.keys())==5):
          print('targetItem', targetItem)
          targetItems.append(targetItem)
          targetItem={}
      print('MongoExport.result', result)
      print('MongoExport.targetItems', targetItems)
      return targetItems
      


if __name__ == '__main__':
  '''''
  将phoneNum.phone2addr 中的14万号段数据,保存至'./phone2addr.txt'
  ex: '13247623805,广东 深圳,广东联通 GSM卡,0755,518000'
  '''
  mongohelper=MongoHelper("phoneNum", "phone2addr")
  results= mongohelper.select(None, None)
  with open('./phone2addr.txt','w+') as f:
    for result in results:
      resultstr = result['Num'] + ',' +result['ProvAndCity'] + ',' + result['net'] +  ',' + result['CityNum'] +  ',' + result['MailNum'] + '\n'
      print(type(resultstr))
      f.write(resultstr)
      print(resultstr.encode('utf-8'))

'''''
  mongohelper=MongoHelper("phoneNum", "phone2addr")
  results=mongohelper.MongoExport(None,None)
  mongohelper.select_colletion("phone2addr")
  for result in results:
    mongohelper.insert(result)
'''   