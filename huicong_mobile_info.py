# encoding=utf-8

import requests
import urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import random
import xlrd
import os, sys, string, time

reload(sys)
import MySQLdb

# 连接数据库　
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='companyinfo', charset="utf8")
except Exception, e:
    print e
    sys.exit()

# 获取cursor对象来进行操作
cursor = conn.cursor()
# 清空表
# cursor.execute("truncate table companyhomepage;")
# conn.commit()


# 更换agent
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


def create_table():
    try:
        sql = 'CREATE TABLE `mobile_specific_info` (`No` INT(11) NOT NULL AUTO_INCREMENT,`name` VARCHAR(100) NULL DEFAULT NULL,`homepage` VARCHAR(100) NULL DEFAULT NULL,`products` VARCHAR(300) NULL DEFAULT NULL,' \
              '`main_field` VARCHAR(100) NULL DEFAULT NULL,`business_type` VARCHAR(100) NULL DEFAULT NULL,`business_mode` VARCHAR(100) NULL DEFAULT NULL,`registered_address` VARCHAR(100) NULL DEFAULT NULL,' \
              '`business_address` VARCHAR(100) NULL DEFAULT NULL,`established_time` VARCHAR(100) NULL DEFAULT NULL,`legal_person` VARCHAR(100) NULL DEFAULT NULL,' \
              '`employee_num` VARCHAR(100) NULL DEFAULT NULL,`annual_turnover` VARCHAR(100) NULL DEFAULT NULL,`brand` VARCHAR(100) NULL DEFAULT NULL,`registered_money` VARCHAR(100) NULL DEFAULT NULL,' \
              '`main_customer` VARCHAR(100) NULL DEFAULT NULL,`main_market` VARCHAR(100) NULL DEFAULT NULL,`annual_exports` VARCHAR(100) NULL DEFAULT NULL,`annual_imports` VARCHAR(100) NULL DEFAULT NULL,' \
              '`bank` VARCHAR(100) NULL DEFAULT NULL,`bank_account` VARCHAR(100) NULL DEFAULT NULL,`oem` VARCHAR(100) NULL DEFAULT NULL,`r_n_d` VARCHAR(100) NULL DEFAULT NULL,`outputs` VARCHAR(100) NULL DEFAULT NULL,' \
              '`plant_area` VARCHAR(100) NULL DEFAULT NULL,`quality_control` VARCHAR(100) NULL DEFAULT NULL,`manage_certification` VARCHAR(100) NULL DEFAULT NULL,`acquiredtime` VARCHAR(100) NULL DEFAULT NULL,' \
              'PRIMARY KEY (`No`))COLLATE=utf8_general_ci,ENGINE=MyISAM,AUTO_INCREMENT=1'
        cursor.execute(sql)

        sql2 = 'CREATE TABLE `mobile_commodity_info` (`No` INT(11) NOT NULL AUTO_INCREMENT,`companyname` VARCHAR(100) NOT NULL,`commodity_name` VARCHAR(100) NULL,`commodity_price` VARCHAR(100) NOT NULL,' \
               '`commodity_picUrl` VARCHAR(100) NULL DEFAULT NULL,`acquiredtime` VARCHAR(100) NOT NULL,PRIMARY KEY (`No`))COLLATE=utf8_general_ci,ENGINE=MyISAM,AUTO_INCREMENT=1'
        cursor.execute(sql2)
    except Exception, e:
        print e

def get_data():
    data_path = 'D:/needfile/workspace/part5_backup.txt'
    f = open(data_path, "r")
    a = []
    while True:
        line = f.readline()
        if line:
            a.append(line.split())
        else:
            break
    f.close()
    return a



def get_info():

    #driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    create_table()
    dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (random.choice(agents))
    # count = 1
    a = get_data()
    for elem in a:
        companyname = elem[1]
        try:
            #最后一列是地址信息
            url = elem[-1]
            a = url[7:]
            index = a.index('.b2b')
            b = a[:index]
            print b
            info_url = 'http://js.hc360.com/cn/gd/company-' + str(b)
        except:
            f = open("D:/needfile/workspace/error/fail_url.txt", 'ab')
            f.write(str(info_url))
            f.write('\r\n')
            f.close()

        print info_url
        time.sleep(1)
        driver.get(info_url)
        html = driver.page_source
        try:
            getcompanyinfo(html, companyname)
        except Exception, e:
            print e
            print '没有找到公司信息'
            f = open("D:/needfile/workspace/error/info_error.txt", 'ab')
            f.write(str(info_url))
            f.write('\r\n')
            f.close()
        # 获取商品信息
        commodity_url = str(info_url) + '/product.html'
        print commodity_url
        time.sleep(1)
        driver.get(commodity_url)
        commodity_html = driver.page_source
        try:
            get_commodity(commodity_html, companyname)
        except Exception, e:
            print e
            print '没有找到商品信息'
            f = open("D:/needfile/workspace/error/commodity_error.txt", 'ab')
            f.write(str(commodity_url))
            f.write('\r\n')
            f.close()
        #处理完一行删除一行
        delete_firstline()



def delete_firstline():
    with open('D:/needfile/workspace/part5_backup.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('D:/needfile/workspace/part5_backup.txt', 'w') as fout:
        fout.writelines(data[1:])

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


def getcompanyinfo(html, companyname):
    bs = BeautifulSoup(html)
    companyinfo = bs.select('span[class="c-right"]')
    companyinfos = []
    print len(companyinfo)
    for elem in companyinfo:
        companyinfos.append(elem.get_text().encode('utf-8'))
        # print companyinfos
    updata_companyinfo(companyinfos, companyname)


def updata_companyinfo(companyinfos, companyname):
    # sql_tranform = 'SET NAMES utf8'
    # cursor.execute(sql_tranform)
    # 获取当前的时间
    acquiredtime = str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))
    # 主要产品
    products = companyinfos[0]
    # 主营行业
    field = companyinfos[1]
    # 企业类型
    type = companyinfos[2]
    # 经营模式
    business_mode = companyinfos[3]
    # 注册地址
    registered_address = companyinfos[4]
    # 经营地址
    business_address = companyinfos[5]
    # 公司成立时间
    established_time = companyinfos[6]
    # 法人
    legal_person = companyinfos[7]
    # 员工人数
    employee_num = companyinfos[8]
    # 经营品牌
    brand = companyinfos[9]
    # 注册资本
    registered_money = companyinfos[10]
    # 主要客户群
    main_customer = companyinfos[11]
    # 开户银行
    bank = companyinfos[12]
    # 银行帐号
    bank_account = companyinfos[13]
    # OEM服务
    oem = companyinfos[14]
    # 研发部门人数：
    r_n_d = companyinfos[15]
    # #月产量
    # outputs =companyinfos[20]
    # 厂房面积
    plant_area = companyinfos[16]
    # 质量控制
    quality_control = companyinfos[17]
    # 管理体系认证
    manage_certification = companyinfos[18]

    sql = "insert into mobile_specific_info(name,products,main_field,business_type,business_mode,registered_address,business_address,established_time,legal_person,employee_num,brand,registered_money,main_customer,bank,bank_account,oem,r_n_d,plant_area,quality_control,manage_certification,acquiredtime) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
        str(companyname), str(products), str(field), str(type), str(business_mode), str(registered_address),
        str(business_address), str(established_time), str(legal_person), str(employee_num),
        str(brand), str(registered_money), str(main_customer), str(bank), str(bank_account), str(oem),
        str(r_n_d), str(plant_area), str(quality_control), str(manage_certification), str(acquiredtime))

    # print sql
    try:
        cursor.execute(sql)
    except Exception, e:
        print e


def get_commodity(commodity_html, companyname):
    commodity_bs = BeautifulSoup(commodity_html)
    commodity_prices = commodity_bs.select('div.A-right div.A-box p.A-num span')
    commodity_names = commodity_bs.select('div.A-right div.A-box p.A-name a')
    commodity_pics = commodity_bs.select('article.A-list ul li div.A-img a img')
    print len(commodity_prices), len(commodity_names), len(commodity_pics)
    a = []
    b = []
    c = []
    for each in commodity_prices:
        # 商品价格
        commodity_price = each.get_text().encode('utf-8')
        a.append(commodity_price)
        # print commodity_price

    for each in commodity_names:
        # 商品名称
        commodity_name = each.get_text().encode('utf-8')
        b.append(commodity_name)
        # print commodity_name

    for each in commodity_pics:
        commodity_pic = each.attrs['src']
        c.append(commodity_pic)
        # print commodity_pic

    # 有商品则更新商品信息插入数据库
    if len(a) > 0:
        for i in range(len(a)):
            commodity_name = b[i]
            commodity_price = a[i]
            commodity_picUrl = c[i]
            print commodity_name, commodity_price, commodity_picUrl
            updata_commodityInfo(companyname, commodity_name, commodity_price, commodity_picUrl)


def updata_commodityInfo(companyname, commodity_name, commodity_price, commodity_picUrl):
    # sql_tranform = 'SET NAMES utf8'
    # cursor.execute(sql_tranform)
    # 获取当前的时间
    acquiredtime = str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))

    sql = "insert into mobile_commodity_info(companyname,commodity_name,commodity_price,commodity_picUrl,acquiredtime) values ('%s','%s','%s','%s','%s')" % (
        str(companyname), str(commodity_name), str(commodity_price), str(commodity_picUrl), str(acquiredtime))
    # print sql
    try:
        cursor.execute(sql)
    except Exception, e:
        print e


if __name__ == "__main__":
    flag = True
    while flag:
        try:
            get_info()
            flag = False
        except Exception, e:
            #
            print e
            f = open("D:/needfile/workspace/error/debug_log.txt", 'ab')
            f.write(str(e))
            f.write('\r\n')
            f.close()

