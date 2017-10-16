#encoding:utf-8

import requests
import urllib
import datetime 
import time
from lxml import etree
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
s=requests.Session()
from pymongo import MongoClient
mc=MongoClient("localhost",27017)
db=mc.check_v3
#获取MIS取数情况，并更新到数据库
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
def pa_newmis():
    #取出接入的所有平台id
    #光大分利宝 的id有问题  .limit(102)
    c=db.v3_para.find({"开业时间":{"$ne":""}},{"平台id":1,"平台名称":1,"_id":0})#.skip(100)

    for i in c:
        pt_id= str(int(i[u"平台id"]))
        #pt_id= str(i[u"平台id"])
        #pt_id= str(int(i[u"平台id"]))
        pt_name=i[u"平台名称"]
        print pt_name
        link="http://mis.rong360.com/mis/netloan/statisticsdetail?id="+pt_id
        
        
        r1=s.get(link,headers=header1,data=pt_id).content
        #print r1
        html1=etree.HTML(r1)
        v_mis_cjl=(html1.xpath("//tr//td[@class='cnt'][3]/text()"))
        v_mis_bs=html1.xpath("//tr//td[@class='cnt'][2]/text()")
        v_time=html1.xpath("//tr//td[@class='cnt'][1]/text()")
        
        
        try:
            for n in range(len(v_time)):
                db.newmis_bs.update({"date":v_time[n]},{"$set":{pt_name:v_mis_bs[n]}},True)
                #print u'标数','v_mis_bs[n]
                #print u'cjl','v_mis_cjl[n]
                db.newmis_cjl.update({"date":v_time[n]},{"$set":{pt_name:float(v_mis_cjl[n])/10000}},True)
            #result.matched_count
        except:
            print pt_id+u"没有数据"
            continue
        

        #需要解决更新数据的问题（更新日期 更新列值）


#pa_newmis()