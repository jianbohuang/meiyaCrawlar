# encoding=utf-8
import json
import base64
import os
import requests
import urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import random
import xlrd
import xlwt as ExcelWrite
import os, sys, string,time
reload(sys)
import MySQLdb
# 连接数据库　
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='companyinfo',charset="utf8")
except Exception, e:
    print e
    sys.exit()

# 获取cursor对象来进行操作
cursor = conn.cursor()
# 清空表
# cursor.execute("truncate table companyhomepage;")
# conn.commit()

myAccount = [
    {'no': 'maclab10', 'psw': 'maclab0'},
    #{'no': 'maclab20', 'psw': 'maclab'},
]

#更换agent
agents = [
    # "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    'Baiduspider',
    'Baiduspider-ads',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]

fail_url = []

def create_table():
    try:
        sql = 'CREATE TABLE `huicong_company_list` (`No` INT(11) NOT NULL AUTO_INCREMENT,`name` VARCHAR(100) NOT NULL,`url` VARCHAR(100) NULL DEFAULT NULL,' \
              '`belong` VARCHAR(100) NULL DEFAULT NULL,`acquiredtime` VARCHAR(100) NOT NULL,PRIMARY KEY (`No`))COLLATE=utf8_general_ci,ENGINE=MyISAM,AUTO_INCREMENT=1'
        cursor.execute(sql)
    except Exception, e:
        print e

#获取关键字地址
def get_url():
    data = xlrd.open_workbook('D:/needfile/workspace/key_list.xlsx')  # 打开xlsx文件
    table = data.sheets()[0]  # 打开第一张表
    nrows = table.nrows  # 获取表的行数
    a = []
    for i in range(230,450):  # 循环逐行读取
        a.append(table.row_values(i)[0].encode('utf-8'))  # 第一列是关键词搜索url地址
    print a
    # 先获取所有需要查找的页面
    zones = ['中国:北京', '中国:天津', '中国:河北省', '山西省', '中国:内蒙古自治区', '中国:辽宁省', '中国:吉林省',
             '中国:黑龙江省', '中国:上海', '中国:江苏省', '中国:浙江省', '中国:安徽省', '中国:福建省', '中国:江西省',
             '中国:山东省', '中国:河南省', '中国:湖北省', '中国:湖南省', '中国:广东省', '中国:广西省', '中国:海南省',
             '中国:重庆', '中国:四川省', '中国:贵州省', '中国:云南省', '中国:西藏自治区', '中国:陕西省', '中国:甘肃省',
             '中国:青海省', '中国:宁夏回族自治区', '中国:新疆维吾尔自治区', 'Korea(republic of)']
    # b存储的是带有关键字查询且带有地区的url
    b = []
    for elem in a:
        for zone in zones:
            zone_url = str(elem) + '&z=' + str(zone)
            b.append(zone_url)
    print b
    # start_url为最终拼接的url
    start_urls = []
    for elem in b:
        # 获取当前页的所有请求列表
        url = str(elem) + '&af=9'
        start_urls.append(url)
    #print start_urls
    return start_urls


def getcompanyinfoByDriver(account):
    cookies = []
    for elem in account:
        driver = webdriver.Firefox()
        #driver.maximize_window()
        dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (random.choice(agents))
        #帐号密码模拟登录
        account = elem['no']
        password = elem['psw']
        driver.get("https://sso.hc360.com/ssologin?ReturnURL=http%3A%2F%2Fwww.hc360.com%2F&")
        elem_user = driver.find_element_by_name("LoginID")
        elem_user.send_keys(account)  # 用户名
        elem_pwd = driver.find_element_by_xpath('//input[@id="password"]')
        elem_pwd.send_keys(password)  # 密码
        time.sleep(2)
        elem_sub = driver.find_element_by_class_name("btm_submit")
        elem_sub.click()  # 点击登陆
        time.sleep(2)
        huicong_cookies = driver.get_cookies()
        cookies.append(huicong_cookies)

        #
        a= get_url()
        for elem in a:
            print elem
            index = elem.index('&z=')
            #拿到所属地区
            address = elem[index+3:]
            index2 = address.index('&af=')
            belong = address[:index2]
            print '所属地区'
            print belong
            flag = True
            #yanzheng = False
            x = 1
            while flag:
                url = str(elem) + '&ee=%s' % x
                x += 1
                #driver.get(str(url))
                #如果是验证码则连续访问5次，连续失败后返回到失败列表
                try:
                    for i in xrange(3):
                        driver.get(str(url))
                        time.sleep(1)
                        # 断网重连
                        if i == 2:
                            reconnect()
                        print '第%d次尝试'%i
                        #找到是否包含了验证码图片
                        if not driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td[2]/form/img'):
                            break
                    else:
                        print '加入失败列表'
                        fail_url.append(str(url))
                        #追加模式打开把失败连接加入文本文件
                        f = open("D:/needfile/workspace/fail_url.txt", 'ab')
                        f.write(str(url))
                        f.write('\r\n')
                        f.close()
                except:
                    pass

                time.sleep(1)
                infopage = driver.find_elements_by_class_name('s-listbox')
                #print infopage

                if infopage:
                    html = driver.page_source
                    getcompanyinfo(html,belong)

                if not infopage:
                    flag = False

        print fail_url

        #保存失败的链接列表
        # file_name='G:/Data/failurl.xlsx'
        # writeXLS(file_name, fail_url)

        driver.close()
    return cookies

#重新拨号
def reconnect():
    print '重新拨号换IP'
    command = 'C:/Users/xmu/Desktop/recon.bat'
    os.system(command)
    url = 'https://www.baidu.com/'
    rep = urllib2.urlopen(url)
    print rep.code
    while rep.code != 200:
        time.sleep(3)
        reconnect()
    print '断网重连成功'


def getcompanyinfo(html,belong):
    bs = BeautifulSoup(html)
    companyinfos = bs.find_all("a", href=re.compile('b2b.hc360.com'))
    for elem in companyinfos:
        companyname = elem.get_text().encode('utf-8')
        companyurl = elem['href']
        #print '输出公司信息'
        updata_companyhomepage(companyname, companyurl,belong)


def updata_companyhomepage(companyname, companyurl,belong):

    # sql_tranform = 'SET NAMES utf8'
    # cursor.execute(sql_tranform)
    # 获取当前的时间
    acquiredtime = str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))
    sql = "insert into huicong_company_list(name, url, belong, acquiredtime) values ('%s', '%s', '%s', '%s')" % (
    str(companyname), str(companyurl), str(belong), str(acquiredtime))
    try:
        cursor.execute(sql)
    except Exception, e:
        print e


#获取cookies
cookies = getcompanyinfoByDriver(myAccount)
print cookies
print "Get Cookies Finish!( Num:%d)" % len(cookies)







