#coding:utf-8
#encoding:utf-8
#获取知乎信息
import base64
import os
from subprocess import call
#from selenium import webdriver  
import urllib
import re
import sys
import subprocess
import chardet
from RedisHelper import RedisHelper
from MongoHelper import MongoHelper

import http
import cookielib
import urllib2
import json
import random
from bs4 import BeautifulSoup

DEBUG=True
FABU=False

base_url=('http://www.runoob.com')
index_url=('http://www.dytt8.net/index.htm')
#base_url=r'http://www.dytt8.net/html/gndy/dyzz/20170305/53401.html'
home_url = 'http://cd.lianjia.com/'
ershou_url = 'http://cd.lianjia.com/ershoufang/'
auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fcd.lianjia.com%2F'
chengjiao_url = 'http://cd.lianjia.com/chengjiao/'
input_urls_file = "G:\cnn-text-classification-tf-master\cnn-text-classification-tf-master\data\input_urls.txt"

#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]
  
def get_driver(url):
    print('get_driver')
    driver = webdriver.PhantomJS()
    print('webdriver')
    driver.get(url)
    print('get_url')
    return driver


def search_html(driver, html):
   # fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'a+')
    fhtml=open(r'./html_txt.txt', 'a+')
    print('search_html') 
    restrs = ('href="(.*?)">')
    resurl = ('href="(.*?).html"')
    html = str(html)
    lines = html.split('</a>')
    for line in lines:
            fhtml.writelines(line+'\n')
            #print(line+'\n')
#        try:
            results = re.search(restrs, line.strip())
            if results is None:
                continue
            for result in results.groups():
                if ('tutorial' in result and 'www' in result):
                    result = "http://"+result[2:]
                    print("result= %s" % result)
                    outmsg = subprocess.getoutput("wget -i %s"% result)
                    print("wget==>%s" % result)
                    driver = get_driver(result)
                    html2 = driver.page_source
                    html2 = str(html2)
                    lines2 = html2.split('</a>')
                    for line in lines2:
                        results = re.search(resurl, line.strip())
                        if results is None:
                            continue
                        for result in results.groups():
                            result = base_url+result+".html"
                            print("======2 level======")
                            print(result)
                            outmsg = subprocess.getoutput("wget -i %s"% result)
                            print("wget==>%s" % result)
                            driver = get_driver(result)
                            html3 = driver.page_source
                            html3 = str(html3)
                            lines3 = html3.split('</a>')
                            for line in lines3:
                                results = re.search(resurl, line.strip())
                                if results is None:
                                    continue
                                for result in results.groups():
                                    print("======3 level======")
                                    result = base_url+result+".html"
                                    outmsg = subprocess.getoutput("wget -i %s"% result)
                                    print("wget==>%s" % result)
    fhtml.close()
                #print (chardet.detect(result.encode(encoding='utf-8')))
                #urls = re.search(resurl, result.strip())
                #if urls is None:
                #    continue
                #for url in urls.groups():
                #     print(url)
                #     url = '/html%shtml\n' % url
                #     if repeatcheck(url, fout):
                #         fout.write(url)
                #         prepare_data(base_url+url)
#        except:
#            pass
#        try:
#            driver.close()
#        except:
#            pass

def repeatcheck(url, file):
    file.seek(0)
    #print url 
    #print file
    lines=file.readlines()
    for line in lines:
        #print line 
        #print url 
        if url.strip()==line.strip():
            #print 'REPEAT'
            return False
    print ('UNREPEAT')
    print (url) 
    return True 


def prepare_data(url):
#    fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'a+')
    print('main') 
    driver = get_driver(url)
 #   time.sleep(10)
    html = driver.page_source
    search_html(driver, html)
    driver.quit()
 #   fout.flush()
  #  fout.close()

def download_data():
    xpath = ('//*[@id="Zoom"]/span/table/tbody/tr/td/a')
    print('download_data') 
    fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'r')
    fsave=open(r'/scrapyredis/selephan/dytt_mv_url_save.txt', 'a+')
    print('open data') 
    lines = fout.readlines()
    print(lines) 
    for line in lines:
        url = base_url+line
        if 'index' in url:
            continue
        driver = get_driver(url)
        elements = driver.find_elements_by_xpath(xpath)
        if elements is not None:
            for element in elements:
                try:
                    strsele = str(element)
                    print ('call[]')
                    thunder = element.get_attribute('wmwalovz')
                    href    = element.get_attribute('href')
#                    call("echo | %s | base64 -d | echo" % thunder, shell=True)
#                    call("echo | %s | base64 -d | echo" % href, shell=True)
                    text = element.text
                    print ('text=%s' % text)
                    print ('thunder=%s' % thunder)
                    print ('href=%s' % href)
                except:
                    print ('except: ')
                    pass
    fout.close()
    fsave.close()

def download_data_2():
    print('download_data') 
    fout=open(r'/scrapyredis/selephan/temp_url.txt', 'r')
    fsave=open(r'/scrapyredis/selephan/temp_thunder.txt', 'a+')
    print('open data') 
    lines = fout.readlines()
    print(lines) 
    pat=('thunder://(.*?)">')
    for line in lines:
       try:
          url = base_url+line
          if 'index' in url:
              continue
          print ('downurl='+url)
          driver = get_driver(url)
          html = driver.page_source
          driver.quit()
          lines = html.split('\n')
          for line in lines:
              #print ('line='+line)
              urls = re.search(pat, line, flags=0)
              if urls is not None:
                  try:
                      for url in urls.groups():
                          fsave.write('thunder://'+url+'\n')
                          print ('thunder://'+url+'\n')
                  except:
                      print('except 9')
                      pass
       except:
          print('except key')
          pass
    fout.close()
    fsave.close()
    
def get_all_html_addr():   
    global fout
    fout=open(r'./html_url.txt', 'a+')
    prepare_data(base_url)
#    download_data_2()
    fout.flush()
    fout.close()

def getAllPic():   
    global fout
    fout=open(r'./html_url.txt', 'a+')
    prepare_data(base_url)
#    download_data_2()
    fout.flush()
    fout.close()
    
    
def get_all_thunder_addr():   
    prepare_data(base_url)
    download_data_2()

def get_all_rar_cont():
    print('get_all_rar_cont')
    fsave=open(r'/scrapyredis/selephan/dytt_mv_url_save.txt', 'r')
    lines=fsave.readlines()
    for line in lines:
        line = line[10:-1]
        b64c = base64.b64decode(line)
        b64c = b64c[2:-2]
        print (b64c)
        b64c = commands.getoutput(r'axel %s' % b64c)
        print (b64c)

    stderrinfo, stdoutinfo = s.communicate()
    print(('stderrinfo is -------> %s and stdoutinfo is -------> %s' % (stderrinfo, stdoutinfo)))
    print('finish executing cmd....')
    return s.returncode

# get the goods msg with phantomjs
def gethtmlwithspider(url):
    # temp int for placehold
    print("=== START TO GET THE AMAZON GOODS MSG")
    print("=== GET THE AMAZON_URLS")
    #driver = webdriver.PhantomJS(r'G:\ProgramData\Anaconda2\envs\tf\Lib\site-packages\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver = webdriver.PhantomJS(r'/root/anaconda3/envs/py36/lib/python3.6/site-packages/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    response=driver.get(url)
    print('=== response')
    slp(1,10)
    data = driver.page_source
    print('=== type(data)')
    print((type(data)))
    f = codecs.open('./%s.html'%(re.sub(r"[^A-Za-z0-9]", "", url)), 'w+', 'utf8')
    f.write(data)
    f.flush()
    slp(300,450)
    while(True):
        slp(1,8)
        if(False):
          url = ('http://cd.58.com/chuzu/pn%d/' % point_int)
          response=driver.get(url)
        else:
          driver.find_element_by_class_name("next").click()
        data = driver.page_source
        print('one page getted, turn to the next')
        slp(300,450)
        f = codecs.open('./%s.html'%(re.sub(r"[^A-Za-z0-9]", "", url)), 'w+', 'utf8')
        f.write(data)
        f.flush()
    driver.quit()
    driver.close()

# get the goods msg with w3m
def getamazongoodsmsg2():
    print("=== START TO GET THE AMAZON GOODS MSG")
    print("=== GET THE AMAZON_URLS")
    for goodsitem in urls_amazon:
        print(("=== url = %s"% goodsitem))
        s=execute_command("w3m %s"%goodsitem)
        print(s)
        s=execute_command('v')
        print(s)
        s=execute_command('S')
        print(s)

        slp(1,3)
        data = driver.page_source
        print('=== type(data)')
        print((type(data)))
        pagecount=0
        while(True):
            s=execute_command('page_source_%d_%d.html'%(urlcount,pagecount))
            slp(1,3)
            print('one page getted, turn to the next')
            slp(5,10)
        urlcount=urlcount+1
    driver.quit()
    driver.close()

def pinglun():
    # get the goods msg with urllib2
    print("=== START TO GET THE AMAZON GOODS MSG")
    print("=== GET THE AMAZON_URLS")
    for goodsitem in urls_amazon:
#        response=driver.get(u'https://www.baidu.com/')
#        response=driver.get(u'https://www.amazon.com/')
        global urlcount,pagecount
        size = getpagesize(converturls(goodsitem, 1), getfilename(urlcount, pagecount))
        print((type(size)))
        slp(3,10)
        if(type(size)==int):
          for i in range(2,size):
              requestserver(converturls(goodsitem, i),getfilename(urlcount, pagecount))
          pagecount=0
#        break
      #  global urlcount
        urlcount=urlcount+1
    urlcount=0

def converturls(baseurl, i):
    # 0 is not useable
    # the first goods
    url=""
    if (i==1):
        url='ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=avp_only_reviews'
        #'http://www.amazon.com/SYLVANIA-LIGHTIFY-Osram-Smart-Tunable/product-reviews/B00R3ID2BG/ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=avp_only_reviews'
    else:
        url='ref=cm_cr_arp_d_paging_btm_%d?ie=UTF8&reviewerType=avp_only_reviews&pageNumber=%d'% (i,i)
        #'http://www.amazon.com/SYLVANIA-LIGHTIFY-Osram-Smart-Tunable/product-reviews/B00R3ID2BG/ref=cm_cr_arp_d_paging_btm_%d?ie=UTF8&reviewerType=avp_only_reviews&pageNumber=%d'% (i,i)
    print(("===after url = %s%s\n"% (baseurl,url)))
    return baseurl+url

def prt(x):
    print(("=== ",str(x)))
    print((time.localtime()))
    print(x)
    print((type(x)))
    if (isinstance(x, bytes)):
        print((chardet.detect(x)))
    print("\n")

def p(x):
    print(("=== ",str(x)))
    print((time.localtime()))
    print(x)
    print((type(x)))
    if (isinstance(x, bytes)):
        print((chardet.detect(x)))
    print("\n")

def getpagesize(url, name):
    # get the 1 page
    f=codecs.open(name, "w+", "utf8")
    req = urllib2.Request(url,headers=hds[random.randint(0,len(hds)-1)])
    print("=== request")
    prt(req)
    source_code = urllib2.urlopen(req,timeout=25).read()
    print("=== source_code")
#    prt(source_code)
    slp(10,20)
    print((chardet.detect(source_code)))
#    print(type(source_code))
    plain_text=source_code.decode('utf8')
#    plain_text=str(source_code)#,errors='ignore')
    f.write(plain_text)
    prt("write plain_text")
    f.flush()
    f.close()
    soup = BeautifulSoup(plain_text)
    print((type(soup)))
    t0=0
    for tags in soup.findAll("a", href=re.compile("pageNumber")):
        try:
            pass
#            prt(tags['href'])
        except:
            prt("continue")
            continue
        ts = re.compile("=(.)&").findall(tags['href'])
        for t in ts:
            print((type(t)))
            print((type(t)))
            if isinstance(t,str):
                print("t is a int")
                if(int(t)-t0>0):
                    print("t is a bigger num")
                    t0=int(t)
    prt(t0)
    return(t0)

def requestserver(url, name):
    # get the 2+ page, cause in amzon the 1st page is differnt with the second ones
    f=codecs.open(name, "w+", "utf8")
    req = urllib2.Request(url,headers=hds[random.randint(0,len(hds)-1)])
    source_code = urllib2.urlopen(req,timeout=25).read()
    slp(10,20)
    plain_text=source_code.decode('utf8')
#    plain_text=(source_code)#,errors='ignore')
#    print(plain_text)
    f.write(plain_text)
    soup = BeautifulSoup(plain_text)
#    print(soup)
    f.flush()
    f.close()

def getfilename(i,j):
    global pagecount
    pagecount=pagecount+1
    print((".\page_source_%d_%d.html"%(i, j)))
    return ".\page_source_%d_%d.html"%(i, j)

def clean_the_data(addrs):
    soup = BeautifulSoup(codecs.open(addrs, 'r', "utf8"))
    row=(addrs.split('_')[2])
    col=(addrs.split('_')[3].split('.')[0])
    i=0
    for tags in soup.findAll(("div"), attrs={"class": "a-section celwidget"}):
        for tag in tags:
          try:
            for t in tag.findAll(("a"), attrs={"class": "a-link-normal"}):
                tt=t.get('title')
                if isinstance(tt, str):
                    if 'stars' in t.get('title'):
                        prt("title")
                        print((t.get('title')))
                        dict["title%s%s%s"%(row,col,i)]=t.get('title')
          except:
            continue
        for tag in tags:
          try:
            for t in tag.findAll(("a"), attrs={"data-hook": "review-title"}):
                if isinstance(t.getText(), str):
                  prt("review-title")
                  print((t.getText()))
                  dict["review%s%s%s"%(row,col,i)]=t.getText()
          except:
            continue
        for tag in tags:
          try:
            for t in tag.findAll(("span"), attrs={"data-hook": "review-body"}):
                prt("review-body")
                dict["content%s%s%s"%(row,col,i)]=t.getText()
                print((t.getText()))
          except:
            continue

        i=i+1
        prt('TOTAL NUM:')
        print(i)


#    for tag in soup.findAll(("span"), attrs={"class": "a-icon-alt"}):
#        print(tag)
#    for tag in soup.findAll(("a"), attrs={"data-hook": "review-title"}):
#        print(tag)

def xlshandle():
    # write all the data into the xls
    print("xlshandle")
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
        num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    print("style set")
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    print("sheet set")

    for filenames in os.walk(rootdir):
      for filename in filenames:
        if(isinstance(filename, list)):
            for f in filename:
                if("page_source" in f):
                    clean_the_data(rootdir+"\\"+f)
 #   return
    keyslist=list(dict.keys())
    point=1
    wrflags=True
    for key in keyslist:
        prt(key)
#        point=calthepoint(key)
        prt(point)
        ws.write(point, 0, key)
        if 'title' in key:
          ws.write(point, 1, dict[key])
        elif 'review' in key:
          ws.write(point, 2, dict[key])
        elif 'content' in key:
          ws.write(point, 3, dict[key])
        else:
          ws.write(point, 4, dict[key])
#        dictlens=len(dict)
        point=point+1
    ws.write(point+1, 0, datetime.now(), style1)
    wb.save('example.xls')



#    ws.write(0, 0, converturls(urls_amazon(), 1), style0)

def calthepoint(name):
  keyitem=re.search('(\d+)', name)
  num = int(keyitem.group(0))
  h = int(num/100)+1
  t = int(num%100/10)+1
  g = int(num%10)+1
  prt(h)
  prt(t)
  prt(g)
  print((h*t+g))
  return(h*t+g)

def showvocab():
#show the vocab
    pass

def pushindict(dict, key):
  if(key in dict):
    dict[key]=dict[key]+1
  else:
    dict[key]=1
  p((key,dict[key]))

def calculatortheword():
#show the word frequency
  FLAGS = tf.flags.FLAGS
  pos_path="G:\\cnn-text-classification-tf-master\\cnn-text-classification-tf-master\\data\\rt-polaritydata\\rt-polarity.pos"
  neg_path="G:\\cnn-text-classification-tf-master\\cnn-text-classification-tf-master\\data\\rt-polaritydata\\rt-polarity.neg"
  check_dir="C:\\Users\\Administrator.WIN7U-20160924F\\runs\\1491619599\\checkpoints"
  tf.flags.DEFINE_string("positive_data_file", pos_path, "Data source for the positive data.")
  tf.flags.DEFINE_string("negative_data_file", neg_path, "Data source for the positive data.")
  x_raw, y_test = data_helpers.load_data_and_labels(FLAGS.positive_data_file, FLAGS.negative_data_file)
  y_test = np.argmax(y_test, axis=1)
  x_raw = [data_helpers.clean_str(sent) for sent in x_raw]
  dictobj={}
  for x in x_raw:
    for y in x.split(' '):
      for w in y.split('('):
        for z in w.split(')'):
          for h in z.split('"'):
             for i in h.split(','):
               for j in i.split("'"):
                 dd = [pushindict(dictobj,j)]
#  wrdictojson("jsonFile.json", dictobj)
  wrdictoxls("G:\\cnn-text-classification-tf-master\\cnn-text-classification-tf-master\\data\\wordfreq.xls", dictobj)



def wrdictojson(str, dictobj):
    jsobj = json.dumps(dictobj)
    fileObject = open("jsonFile.json", "w+")
    fileObject.write(jsobj)
    fileObject.close()

def wrdictoxls(strin, dictobj):
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
        num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    print("style set")
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    print("sheet set")
    point=0
    for i in list(dictobj.keys()):
      ws.write(point, 1, dictobj[i])
      ws.write(point, 0, i)
# trans en 2 ch
#      ws.write(point, 2, transen2ch(i))
      point=point+1
    wb.save(strin)

def transen2ch(src):
    ApiKey = "hEo3DwbzUA3HXbFOrlYM7Ptq4vGqmW6d"
    turl = "http://openapi.baidu.com/public/2.0/bmt/translate?client_id="+\
ApiKey+"&q="+src+"&from=auto&to=zh"
    try:
      req = urllib2.Request(turl)
      con = urllib2.urlopen(req).read()
    except Exception:
      pass
    decoded = json.loads(con)
    dst = str(decoded["trans_result"][0]["dst"])
    p(dst)
    return dst

def tingyongjudgy(input):
    with open("G:\cnn-text-classification-tf-master\cnn-text-classification-tf-master\data\stopwords.txt") as sw:
        for line in sw.readlines():
            if(input in line):
#        p(input+"True")
                return True
#    p(input+"False")
    return False


def passtingyong(list):
#  p(list)
  outlist=[]
  for item in list:
#    p(item)
    if (tingyongjudgy(item)):
      continue
    outlist.append(item)
  return outlist

def drawpicxls():
  wb = xlsxwriter.Workbook('G:\cnn-text-classification-tf-master\cnn-text-classification-tf-master\data\example.xlsx')
  ws = wb.Worksheet('Sheet1')
  chart1 = wb.add_chart({'type': 'column'})
  chart1.add_series({'name':'=Sheet1!$A$1','categories':'=Sheet1!$A$1:$A$791','values':'=Sheet1!$B$1:$B$791',})
  chart1.set_title ({'name': 'Results of sample analysis'})
  chart1.set_x_axis({'name': 'Oula dist'})
  chart1.set_y_axis({'name': 'Sample'})
  ws.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
  wb.close()

def drawxy():
  f=open('G:\cnn-text-classification-tf-master\cnn-text-classification-tf-master\data\word2xy.txt','r')
  lines=f.readlines()
  for line in lines:
    print(line)
    wgs=line.strip().split(',')
    x=(wgs[1])
    y=(wgs[0])
    fx=decimal.Decimal("%.1f" % float(x))
    fy=decimal.Decimal("%.1f" % float(y))
    print((fx,fy))
#    plt.plot(fx,fy)
    plt.plot(fx,fy,'ro',label="point")
#    plt.legend()
  print('show')
  plt.show()

def get_words(file):
    with open (file) as f:
        words_box=[]
        for line in f:
            if re.match(r'[a-zA-Z0-9]*',line):
                list1 = line.strip().split()
                list2=[]
                for item in list1:
                    if tingyongjudgy(item):
                        continue
                    list2.append(item)
                   # p("add"+item)
#                p(list1)
                words_box.extend(list2)
    return collections.Counter(words_box)


def cal_oula_distance():
  # sentense to 10 words , then calcu the distance of oula
  x_raw, y_test = data_helpers.load_data_and_labels(FLAGS.positive_data_file, FLAGS.negative_data_file)
  y_test = np.argmax(y_test, axis=1)
  vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
  vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
  x_test = np.array(list(vocab_processor.transform(x_raw)))

  ibase = x_test[0]
  ybase = x_test[53]
  fout=open("G:\cnn-text-classification-tf-master\cnn-text-classification-tf-master\data\dist_oula.txt", 'w')
  counter=0
  for i in x_test:
    dist = np.linalg.norm(i - ibase)
    disty = np.linalg.norm(i - ybase)
    counter=counter+1
    fout.write("{%s:(%f,%f)},\n"%(str(counter),dist,disty))
  fout.flush()
  fout.close()

def wr2file(file, content):
    f=open(file,'w+')
    f.write(content)
    f.flush()
    f.close()
    p("wr2file SUCC")

# get the goods msg with phantomjs
def get58city(url):
    print("=== GET 58 CITY")
    driver = webdriver.PhantomJS()
    f=open(input_urls_file,'r')
    for line in f.readlines():
        response=driver.get(line)
#        response=driver.get(u'https://www.amazon.com/')
#        response=driver.get(goodsitem)
        print('=== response')
        print(response)
        slp(1,5)
        data = driver.page_source
        print('=== type(data)')
        print((type(data)))
        pagecount=0
        while(True):
            f = codecs.open('./58city%d_%d.html'%(urlcount, pagecount), 'w+', 'utf8')
            f.write(data)
            slp(1,3)
            f.flush()
            f.close()
            list=driver.find_elements_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[8]/a')
            if(list==[]):
                print('list is none,this goods msg is over')
                break;
            for a in list:
                print('item obtained href')
                print((a.xpath('@href')))
                a.click()
                pagecount=pagecount+1
                print(('pages %d'%pagecount))
                slp(3,4)
                data = driver.page_source
                slp(3,4)
            print('one page getted, turn to the next')
            slp(5,9)
        urlcount=urlcount+1
    driver.quit()
    driver.close()

def saveHtml(file_name,file_content):
    with open (file_name,"wb") as f:
        f.write(file_content)

def getIp():
    opener = urllib2.build_opener()
    mongohelper=MongoHelper()
    dicts= mongohelper.findOne(True)
    #response= opener.open("http://127.0.0.1:8080", timeout=1000)
    #dicts=(json.loads(response.read().decode()))
    #i=random.randint(0,len(dicts))
    ip=str(dicts['ip'])+':'+str(dicts['port'])
    print(ip)
    return ip



def makeMyOpener():
    cj = cookielib.CookieJar()
    #cj = http.cookiejar.CookieJar()
    proxy = urllib2.ProxyHandler({'http': getIp()})  # 设置proxy
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),proxy)
    myheader = hds[random.randint(0,len(hds)-1)]
    opener.addheader=myheader
    return opener

def trans_url_bd(net,word):
  if False:
    baseurls='https://www.baidu.com/s?q1='
    q1=urllib.parse.quote(word)
    baseurl2='&q2=&q3=&q4=&gpc=stf&ft=&q5=&q6='
    q2=urllib.parse.quote(net)
    baseurl3='&tn=baiduadv'
    url=baseurls+q1+baseurl2+q2+baseurl3
    print(url)
    print((urllib.parse.quote(url)))
    return (url)
  else:
    url='http://www.baidu.com/s'
    print(word)
    values={
      'ie':'UTF-8',
      'wd':word
    }
    data=urllib.parse.urlencode(values)
    #req=urllib2.Request(url,data)
    url=url+'?'+data
    print(url)
    return url
    #response = urllib2.urlopen(req)
        
import os,re,urllib,uuid  
  
#首先定义云端的网页,以及本地保存的文件夹地址  
urlPath='http://www.nipic.com/index.html/'  
localPath='./images'
baseurlPath='http://www.nipic.com'  
  
#从一个网页url中获取图片的地址，保存在  
#一个list中返回  
def getUrlList2(urlParam):  
    urlStream=urllib.urlopen(urlParam)  
    htmlString=urlStream.read()  
    if( len(htmlString)!=0 ):  
        patternString=r'http://.{0,500}\.jpg'  
        searchPattern=re.compile(patternString)  
        imgUrlList=searchPattern.findall(htmlString)  
        return imgUrlList  
  
          
#生成一个文件名字符串   
def generateFileName():  
    return str(uuid.uuid1())  
  
      
#根据文件名创建文件    
def createFileWithFileName(localPathParam,fileName):  
    totalPath=localPathParam+'\\'+fileName  
    if not os.path.exists(totalPath):  
        file=open(totalPath,'a+')  
        file.close()  
        return totalPath  
      
  
#根据图片的地址，下载图片并保存在本地   
def getAndSaveImg(imgUrl):  
    if( len(imgUrl)!= 0 ):  
        fileName=generateFileName()+'.jpg'  
        urllib.urlretrieve(imgUrl,createFileWithFileName(localPath,fileName))  
  
#下载函数  
def downloadImg(url): 
    print('开始访问网站', url) 
    getUrlList(url)  
    for urlString in urlList:  
        getAndSaveImg(urlString)  
import traceback

def getUrlList():
    print('开始获得网页链接: ')
    redishelper= RedisHelper()
    urls= redishelper.get('linkstarget')
 #   print(urls)
    for url in urls:
 #     print('\nurl: ', url)
      bFlag= redishelper.hexists('urlhandled', url)
      if(bFlag):
        print('linkstarget 已经在 imghandled 中处理过,返回获取新的链接地址')
        continue
      opener=makeMyOpener()
      try:
        response=opener.open(url, timeout=1000)
      except urllib2.HTTPError:
        traceback.print_exc()
        continue
      except ValueError:
        traceback.print_exc()
        continue        
      data=response.read()
      soup = BeautifulSoup(data, 'lxml')
      for links in soup.findAll("a"):
#        print(u"获得本页所有链接", links)
#        print(u"获得本页所有链接 links.href", links.get('href'))
        try:
          hrefheader= links.get('href').split('/')[0]
        except AttributeError:
          traceback.print_exc()
          continue
        if (not(hrefheader == 'http:')):
          href= baseurlPath+links.get('href')
        else:
          href= links.get('href')
        try:
          redishelper.hset('linkstarget', href, href)
        except:
          print('except')
      redishelper.hset('urlhandled', url, url)

def getImgFromUrl():
    print('开始获得网页链接: ')
    redishelper= RedisHelper()
    print(keys)
    urls= redishelper.get('linkstarget')
    print(urls)
    for url in urls:
      bFlag= redishelper.sismember('imghandled', url)
      if bFlag:
        continue
      opener=makeMyOpener()
      response=opener.open(url, timeout=1000)
      data=response.read()
      soup = BeautifulSoup(data, 'lxml')
#    f=codecs.open(name, "w+", "utf8")
      req = urllib2.Request(url,headers=hds[random.randint(0,len(hds)-1)])
      source_code = urllib2.urlopen(req,timeout=25).read()
      plain_text=source_code.decode('utf8')
#    f.write(plain_text)
      soup = BeautifulSoup(plain_text)
      for links in soup.findAll("img"):
        print("获得本页所有图片", links.src)
        getAndSaveImg(links)
    redishelper.hset('imghandled', url)
      
def getAllImg():    
    redishelper= RedisHelper()
    urlstr=("设计模式之禅")
    url=trans_url_bd("csdn.net", "site:(zhihu.com)  "+ urlstr)
    opener=makeMyOpener()
    response=opener.open(url, timeout=1000)
    data=response.read()
    soup = BeautifulSoup(data, 'lxml')
    for div in soup.findAll('a'):
      print('获得所有的链接 a', a.href)
      for a in div.findAll('a'):
        try:
          print("=====")
          hrefname = a['href']
          if(hrefname[0:2]=='/s'):
                hrefname=hrefname+a['href']
          urls = '[link](%s)'%hrefname
          print(urls)
          f.write(urls+"\n")
        except:
          traceback.print_exc()
          print('except')
    f.flush()
    f.close()

if __name__=="__main__":
  while(True):
    getUrlList()
