#encoding:utf-8

import requests
import urllib
import datetime 
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import codecs
s=requests.Session()
from pymongo import MongoClient
mc=MongoClient("localhost",27017)
db=mc.check_v3
#抓取页面上上线按钮是 disabled=true 
#http://mis.rong360.com/mis/netloaninterface/list.html?page=1
header1={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection":"keep-alive",
    "Cookie":"pgv_pvi=5196879920; gr_user_id=c2355eca-d077-4924-af82-38ad50a49107; tma=167058877.34795974.1458027381462.1463965948748.1464061114140.4; bfd_g=8a7bc81f66bd068d00004ddc00358fee55aba738; RONGID=b4165ebe1977bd9b109c8df5988a57ad; zc=310001-1584e_410001-156d0_42-38664_; b_loan_limit=3.0; b_loan_term=12; b_car_price=20; historyCardIds=31aacc26f95766d90c5b0eb846846f9a%2Cbb09b2d35d7ca0d79ab79caec973b2a1%2C72fc94e19a37d11f8a2688e1b3cefa2a%2Cee6c310e0f21288e4a79dc9ffae552ce%2C0035f97d7acdf2b0417bc4882b13610a; city_id=2; abclass=1489992106_3; cityDomain=beijing; __utmz=1507701594.utmcsr=(direct)|utmcmd=(direct); PHPSESSID=3dqq9g3lhgjjcdprev1322mlf2; RONG360_CSRF_TOKEN=33245bf39a3e9d5dd7808a16e20d4ecbe103e2c5s%3A40%3A%22e636977727c7e9b1fb94d763215809b1f38e14bf%22%3B",
    "Host":"mis.rong360.com",
    "Referer":"mis.rong360.com",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}

def get_newPara():
    link1="http://mis.rong360.com/mis/netloaninterface/list.html?page=1"
    r1=s.get(link1,headers=header1).content
    html1=etree.HTML(r1)
    pg="".join(html1.xpath("//div[@class='page']//a[last()-1]/text()"))
    list_idl=[]
    for i in range(1,int(pg)+1):
        link_i="http://mis.rong360.com/mis/netloaninterface/list.html?page="+str(i)
        r2=s.get(link_i,headers=header1).content
        html2=etree.HTML(r2)
        #list_bh=html2.xpath(u"//tr//button[[@disabled='true'] and [contains(text(),'上线')]]/parent::*/parent::*/td[@class='cnt'][1]/text()")
        list_bh=html2.xpath("//tr/td[@class='cnt'][1]/text()")
        list_ptid=html2.xpath(u"//tr/td[@class='cnt'][2]/text()")
        list_ptmc=html2.xpath(u"//td[@class='lft']/text()")
        print list_bh
        for x in range(0,len(list_bh)):
            bianhao=list_bh[x]
            pt_id=list_ptid[x]
            ptName=list_ptmc[x]
            print bianhao,ptName,pt_id
            #更新token信息
            data1={
            "id":bianhao
            }
            link1="http://mis.rong360.com/mis/netloaninterface/edit?id="+str(bianhao)
            r1=s.get(link1,headers=header1,data=data1).content
            #print r1
            html1=etree.HTML(r1)
            manbiao_url="".join(html1.xpath("//input[@id='basefullUrl4']/@value"))
            #mb_url2="".join(html1.xpath(u"//input[@placeholder="+u"请输入满标数据请求地址"+u"]/@value"))
            #need_token="".join(html1.xpath(u"//span[contains(text(),'获取token')]/parent::*//input[@checked='checked']/@value"))
            need_token="".join(html1.xpath(u"//input[@name='js_has_token4']/../text()")).strip()
            print need_token
            url_token="".join(html1.xpath(u"//input[@id='tokenUrl4']/@value"))
            name_token="".join(html1.xpath(u"//input[@id='userName4']/@value"))
            pass_token="".join(html1.xpath(u"//input[@id='password4']/@value"))
            print manbiao_url,need_token,url_token,name_token,pass_token
            #更新平台上线日期
            link3="http://mis.rong360.com/mis/netloan/statisticsdetail?id="+str(pt_id)
            r3=s.get(link3,headers=header1,data=pt_id).content
            html3=etree.HTML(r3)
            opening_time="".join(html3.xpath("//div[@class='main']//text()[3]")).strip().split("：")[1]
            print opening_time


            
            db.v3_para.update({"平台id":int(pt_id)},
                {"$set":
                    {"平台名称":ptName,
                    "编号":bianhao,
                    "是否要token":need_token,
                    "token_url":url_token,
                    "账户":name_token,
                    "密码":pass_token,
                    "满标接口地址":manbiao_url,
                    "开业时间":opening_time
                    }
                },True)
    #更新参数数据


get_newPara()







def miswd():
    #n=[25,151,153,149,4,148,147,108,144,146,143,142,141,140,137,129,138,134,126,125,124,3,123,120,119,114,112,111,109,107,106,105,102,101,100,97,92,90,91,89,88,87,86,85,84,82,83,80,77,76,72,69,68,62,64,61,60,56,55,51,48,47,46,45,44,40,43,41,39,34,33,27,24,23,20,18,16,17,14,12,11,10,9,8,7,6,5,2,1]
    header2={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Cookie":"_jzqa=1.2465022424565217000.1436750972.1438070209.1438135157.13; __gads=ID=ef16f2a10f89ca0c:T=1438590304:S=ALNI_MbSBI_ocVPpsXhE8FrbgcrRRf_s1A; pgv_pvi=5196879920; gr_user_id=c2355eca-d077-4924-af82-38ad50a49107; tma=167058877.34795974.1458027381462.1463965948748.1464061114140.4; bfd_g=8a7bc81f66bd068d00004ddc00358fee55aba738; m_credit_city=2; RONGID=b4165ebe1977bd9b109c8df5988a57ad; zc=310001-1584e_410001-156d0_42-38664_; b_loan_limit=3.0; b_loan_term=12; b_car_price=20; historyCardIds=31aacc26f95766d90c5b0eb846846f9a2Cbb09b2d35d7ca0d79ab79caec973b2a12C72fc94e19a37d11f8a2688e1b3cefa2a2Cee6c310e0f21288e4a79dc9ffae552ce2C0035f97d7acdf2b0417bc4882b13610a; city_id=2; abclass=1489992106_3; cityDomain=beijing; __utmz=1498528538.utmcsr=(direct)|utmcmd=(direct); PHPSESSID=jd0ouo6k100k5ve88onrg3b7q1; RONG360_CSRF_TOKEN=fbb2f1d936333923543a7855ddf23cefd940128cs3A403A22b3f9dfae20a46368c4f289379961b4250aeca3ba223B",
    "Host":"mis.rong360.com",
    "Referer":"http://mis.rong360.com/mis/netloaninterface/list.html?page=1",
    "Upgrade-Insecure-Requests":1,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    for n in ['172', '169', '171', '48', '170', '168', '167', '163', '162', '45', '161', '160', '159', '157', '156', '155', '25', '151', '153', '149']:
        data={
        "id":n
        }
        link1="http://mis.rong360.com/mis/netloaninterface/edit?id="+str(n)
        r1=s.get(link1,headers=header1,data=data).content
        #print r1
        html1=etree.HTML(r1)
        manbiao_url="".join(html1.xpath("//input[@id='basefullUrl4']/@value"))
        #mb_url2="".join(html1.xpath(u"//input[@placeholder="+u"请输入满标数据请求地址"+u"]/@value"))
        need_token="".join(html1.xpath(u"//input[@name='js_has_token4']/../text()")).strip()
        url_token="".join(html1.xpath(u"//input[@id='tokenUrl4']/@value"))
        name_token="".join(html1.xpath(u"//input[@id='userName4']/@value"))
        pass_token="".join(html1.xpath(u"//input[@id='password4']/@value"))
        print manbiao_url,need_token,url_token,name_token,pass_token

        #print pass_token
#miswd()