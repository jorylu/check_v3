#coding=utf-8
import requests
import urllib
import datetime 
import time
import json
import re
import sys
import xlrd
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from lxml import etree
import codecs
s=requests.Session()
from pymongo import MongoClient
mc=MongoClient("localhost",27017)
db=mc.check_v3
db2=mc.linshi
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
def paa_v(l,name,d,tk):
    time.sleep(5)
    link1=l+d+tk
    header1={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    #"Cookie":"pgv_pvi=5196879920; gr_user_id=c2355eca-d077-4924-af82-38ad50a49107; tma=167058877.34795974.1458027381462.1463965948748.1464061114140.4; bfd_g=8a7bc81f66bd068d00004ddc00358fee55aba738; __jsluid=2ff76f0ab9598e7f3a5f209f1d78bb31; RONGID=b4165ebe1977bd9b109c8df5988a57ad; zc=310001-1584e_410001-156d0_42-38664_; b_loan_limit=3.0; b_loan_term=12; b_car_price=20; historyCardIds=31aacc26f95766d90c5b0eb846846f9a%2Cbb09b2d35d7ca0d79ab79caec973b2a1%2C72fc94e19a37d11f8a2688e1b3cefa2a%2Cee6c310e0f21288e4a79dc9ffae552ce%2C0035f97d7acdf2b0417bc4882b13610a; city_id=2; abclass=1489992106_3; PHPSESSID=5eskghkifh896695jl4u1tncs6; cityDomain=beijing; __utmz=1502952049.utmcsr=(direct)|utmcmd=(direct)",
    "Host":"www.rong360.com",
    "Upgrade-Insecure-Requests":1,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    }
    #print link1
    r1=s.get(link1,headers=header1).content
    html1=etree.HTML(r1)
    t1="".join(html1.xpath("//div[@id='js_body_container']/text()"))
    try:
        #print r2
        v_jk=json.loads(t1)
        v_biaoshu=float(v_jk['totalCount'])
        #v_biaoshu=float(re.sub("\D", "", v_biaoshu))
        print v_biaoshu,name#,d,link1
        v_chengjiaoliang=float(v_jk['totalAmount'])
        #print v_chengjiaoliang
        #v_chengjiaoliang=float(re.sub("\D", "", v_chengjiaoliang))
        db.pa_v3_bs.update({"date":d},{"$set":{name:v_biaoshu}},True)
        db.pa_v3_cjl.update({"date":d},{"$set":{name:v_chengjiaoliang}},True)
    except:
        print link1
        print name
        db.pa_v3_bs.update({"date":d},{"$set":{name:""}},True)
        db.pa_v3_cjl.update({"date":d},{"$set":{name:""}},True)
        db.v3_para.update({"平台名称":name},{"$set":{"接口失灵":"是"}},True)


def paa_v3():
    c=db.v3_para.find({"开业时间":{"$ne":""}},{"平台id":1,"平台名称":1,"满标接口地址":1,"开业时间":1,"token_url":1,"账户":1,"密码":1,"_id":0}).skip(90)
    for i in c:
        pt_id=str(int(i[u"平台id"]))
        p_mb=i[u"满标接口地址"]
        #print p_mb
        #lis=list(pd.date_range(start=i[u'开业时间'],end='2017-05-01'))
        lis=list(pd.date_range(start='20171001',end='20171014'))
        p_date=[datetime.strftime(x,"%Y-%m-%d") for x in lis[::-1]]
        hea1=u"http://www.rong360.com/licai-p2p/fulldataverify/request?baseUrl="
        hea2=u"&page=1&pageSize=1&date="   
        hea3=u"&page=1&tokenUrl="
        #print i['token_url']
        #确定link——没有token
        if i['token_url']=="":
            link=hea1+p_mb+hea2#+d#+hea3
            tk="&header=1&body=1&verifyToken=0"
        else:
            link=hea1+p_mb+hea3+i['token_url']+"&password="+i[u'密码']+"&userName="+i[u'账户']+'&date='#+d#"&header=1&body=1&verifyToken=1"
            tk="&header=1&body=1&verifyToken=1"
        [paa_v(link,i[u'平台名称'],d,tk) for d in p_date]
#li=['信广立诚贷','理财范','易通贷','分利宝','麻袋理财','壹佰金融','有利网','翼龙贷','信融财富','升值空间','奇乐融','联金所','拓道金服','一点钱','首金网','洋葱先生','钱贷网','金桥梁','邦帮堂','民贷天下','向上金服','合力贷','爱钱进','易港金融','今日捷财','人人贷','三益宝','银豆网','和信贷','融金所','德众金融','金开贷','掌中财富','万家贷','海星宝理财','互贷网','口袋理财','信和大金融','农泰金融','汉金所','乐享宝','渝金所','量子金融','合众e贷','紫马财行','金银猫','玺鉴','新富金融','点融网','钱来网','宝点网','丁丁金服','小油菜','广富宝','杉易贷','口贷网','钱盆网','联连理财','智佳金服','信和贷','51帮你','新新贷','海金所','人人聚财']
#[paa_v3(n) for n in li]
paa_v3()

