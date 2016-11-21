# encoding=utf-8

import urllib2
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import random
import xlrd
import os, sys, string,time
reload(sys)
import MySQLdb
# �������ݿ⡡
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='companyinfo',charset="utf8")
except Exception, e:
    print e
    sys.exit()

# ��ȡcursor���������в���
cursor = conn.cursor()
# ��ձ�
# cursor.execute("truncate table companyhomepage;")
# conn.commit()


#����agent
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
        sql = 'CREATE TABLE `company_specific_info` (`No` INT(11) NOT NULL AUTO_INCREMENT,`name` VARCHAR(100) NULL DEFAULT NULL,`homepage` VARCHAR(100) NULL DEFAULT NULL,`products` VARCHAR(300) NULL DEFAULT NULL,' \
              '`main_field` VARCHAR(100) NULL DEFAULT NULL,`business_type` VARCHAR(100) NULL DEFAULT NULL,`business_mode` VARCHAR(100) NULL DEFAULT NULL,`registered_address` VARCHAR(100) NULL DEFAULT NULL,' \
              '`business_address` VARCHAR(100) NULL DEFAULT NULL,`established_time` VARCHAR(100) NULL DEFAULT NULL,`legal_person` VARCHAR(100) NULL DEFAULT NULL,' \
              '`employee_num` VARCHAR(100) NULL DEFAULT NULL,`annual_turnover` VARCHAR(100) NULL DEFAULT NULL,`brand` VARCHAR(100) NULL DEFAULT NULL,`registered_money` VARCHAR(100) NULL DEFAULT NULL,' \
              '`main_customer` VARCHAR(100) NULL DEFAULT NULL,`main_market` VARCHAR(100) NULL DEFAULT NULL,`annual_exports` VARCHAR(100) NULL DEFAULT NULL,`annual_imports` VARCHAR(100) NULL DEFAULT NULL,' \
              '`bank` VARCHAR(100) NULL DEFAULT NULL,`bank_account` VARCHAR(100) NULL DEFAULT NULL,`oem` VARCHAR(100) NULL DEFAULT NULL,`r_n_d` VARCHAR(100) NULL DEFAULT NULL,`outputs` VARCHAR(100) NULL DEFAULT NULL,' \
              '`plant_area` VARCHAR(100) NULL DEFAULT NULL,`quality_control` VARCHAR(100) NULL DEFAULT NULL,`manage_certification` VARCHAR(100) NULL DEFAULT NULL,`acquiredtime` VARCHAR(100) NULL DEFAULT NULL,' \
              'PRIMARY KEY (`No`))COLLATE=utf8_general_ci,ENGINE=MyISAM,AUTO_INCREMENT=1'
        cursor.execute(sql)

        sql2 = 'CREATE TABLE `commodity_info` (`No` INT(11) NOT NULL AUTO_INCREMENT,`companyname` VARCHAR(100) NOT NULL,`commodity_name` VARCHAR(100) NULL,`commodity_price` VARCHAR(100) NOT NULL,' \
               '`commodity_picUrl` VARCHAR(100) NULL DEFAULT NULL,`acquiredtime` VARCHAR(100) NOT NULL,PRIMARY KEY (`No`))COLLATE=utf8_general_ci,ENGINE=MyISAM,AUTO_INCREMENT=1'
        cursor.execute(sql2)
    except Exception, e:
        print e


def get_data():
    data_path = 'D:/needfile/workspace/part4_backup.txt'
    f = open(data_path, "r")
    a = []
    # i = 1
    while True:
        line = f.readline()
        if line:
            a.append(line.split())
            # i+=1
        else:
            break
    f.close()
    return a


def get_info():

    # driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    # driver.maximize_window()
    dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (random.choice(agents))
    a = get_data()
    count = 1
    for elem in a:
        try:
            companyname = elem[1]
            url = elem[-1]
        except:
            f = open("D:/needfile/workspace/error/fail_url.txt", 'ab')
            f.write(str(url))
            f.write('\r\n')
            f.close()
            # break
        print url,companyname
        #��˾���ܵ�ַ
        companyinfo = str(url)+'/shop/show.html'
        #��˾��Ʒ��ַ
        companyinfo_commodity = str(url)+ '/shop/businwindow.html'
        driver.get(companyinfo)
        #time.sleep(1)

        try:
            nav1 = driver.find_elements_by_class_name('mainnav')
            nav2 = driver.find_elements_by_class_name('b-blue')
            yellowpage = driver.find_elements_by_class_name('rBox3Con')
            print nav1,nav2,yellowpage

            # time.sleep(1)

            # �淶�ĵ�����
            if nav1 or yellowpage:
                html = driver.page_source
                getcompanyinfo(html, companyname)
                # print '��ȡ��˾��Ϣ'
                print '��һ�ֺ͵ڶ���'
                #����ǵ�һ�֣�����Ҫ����ץ��Ӧ����Ʒ
                if nav1:
                    print '��һ�๫˾��ҳ��Ϣ'
                    driver.get(companyinfo_commodity)
                    commodity_html = driver.page_source
                    get_commodity(commodity_html, companyname)
                    #time.sleep(1)
                    try:
                        totalpage = driver.find_element_by_class_name('total').text
                        print totalpage
                        a = totalpage[1:]
                        b = a[:-1]
                        print b
                        index = companyinfo_commodity.index('.html')
                        newurl = companyinfo_commodity[:index]
                        if int(b)>1:
                            for i in range(1, int(b)):
                                xurl = newurl + '-%d' % (i + 1) + '.html'
                                print xurl
                                # print '��ֹһҳ��Ʒ'
                                driver.get(xurl)
                                html = driver.page_source
                                get_commodity(html, companyname)

                    except:
                        print 'û����Ʒ'

            elif nav2:
                print '����������ҳ��'
                driver.get(companyinfo)
                html2 = driver.page_source
                #���¹�˾��Ϣ���뵽���ݿ�,������������ִ����һ�ֽ���
                try:
                    getcompanyinfo2(html2)
                except:
                    print '����ʧ�ܣ���������б�'
                    f = open("D:/needfile/workspace/error/fail_companyinfo.txt", 'ab')
                    f.write(str(companyinfo))
                    f.write('\r\n')
                    f.close()

                driver.get(companyinfo_commodity)
                commodity_html2 = driver.page_source
                #���²�Ʒ��Ϣ���뵽���ݿ�
                get_commodityinfo2(commodity_html2, companyname)
                try:
                    totalpage = driver.find_element_by_class_name('total').text
                    print totalpage
                    a = totalpage[1:]
                    b = a[:-1]
                    print b
                    index = companyinfo_commodity.index('.html')
                    newurl = companyinfo_commodity[:index]
                    for i in range(1, int(b)):
                        xurl = newurl + '-%d' % (i + 1) + '.html'
                        print xurl
                        driver.get(xurl)
                        html = driver.page_source
                        get_commodityinfo2(html, companyname)

                except:
                    print 'û����Ʒ��û����һҳ��Ʒ'

            else:
                print '404����ҳ�������쳣�����浱ǰ��������'
                f = open("D:/needfile/workspace/error/fail_companyinfo.txt", 'ab')
                f.write(str(companyinfo))
                f.write('\r\n')
                f.close()

        except:
            print 'û���ҵ������Ϣ'
            f = open("D:/needfile/workspace/error/error.txt", 'ab')
            f.write(str(companyinfo))
            f.write('\r\n')
            f.close()

        delete_firstline()
        time.sleep(2)
        if count % 1000 == 0:
            reconnect()
        count += 1

#���²���
def reconnect():
    print '���²��Ż�IP'
    command = 'C:/Users/xmu/Desktop/recon.bat'
    os.system(command)
    url = 'https://www.baidu.com/'
    rep = urllib2.urlopen(url)
    print rep.code
    while rep.code != 200:
        time.sleep(3)
        reconnect()
    print '���������ɹ�'

def delete_firstline():
    with open('D:/needfile/workspace/part4_backup.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('D:/needfile/workspace/part4_backup.txt', 'w') as fout:
        fout.writelines(data[1:])


def getcompanyinfo(html,companyname):
    bs = BeautifulSoup(html)
    td = bs.select('div[class="detailsinfo"]')[0].find_all('td')
    print len(td)
    # field = bs.find_all("td", class_="cNameBgcolor")
    companyinfos = []
    for i in range(len(td)):
        if i % 2 == 1:
            elem = td[i].get_text().encode('utf-8')
            # print elem
            companyinfos.append(elem)
    #companyinfos����28�˾��Ϣ
    # print companyinfos
    updata_companyhomepage(companyinfos, companyname)


def updata_companyhomepage(companyinfos, companyname):

    # sql_tranform = 'SET NAMES utf8'
    # cursor.execute(sql_tranform)
    # ��ȡ��ǰ��ʱ��
    acquiredtime = str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))
    #��Ҫ��Ʒ
    products = companyinfos[0]
    #��Ӫ��ҵ
    field = companyinfos[1]
    #��ҵ����
    type = companyinfos[2]
    #��Ӫģʽ
    business_mode = companyinfos[3]
    #ע���ַ
    registered_address = companyinfos[4]
    #��Ӫ��ַ
    business_address =companyinfos[5]
    #��˾����ʱ��
    established_time =companyinfos[6]
    #����
    legal_person =companyinfos[7]
    #Ա������
    employee_num =companyinfos[8]
    #��Ӫҵ��
    annual_turnover =companyinfos[9]
    #��ӪƷ��
    brand =companyinfos[10]
    #ע���ʱ�
    registered_money =companyinfos[11]
    #��Ҫ�ͻ�Ⱥ
    main_customer =companyinfos[12]
    #��Ҫ�г�
    main_market =companyinfos[13]
    #����ڶ�
    annual_exports =companyinfos[14]
    #����ڶ
    annual_imports =companyinfos[15]
    #��������
    bank =companyinfos[16]
    #�����ʺ�
    bank_account =companyinfos[17]
    #OEM����
    oem =companyinfos[18]
    #�з�����������
    r_n_d =companyinfos[19]
    #�²���
    outputs =companyinfos[20]
    #�������
    plant_area=companyinfos[21]
    #��������
    quality_control =companyinfos[22]
    #������ϵ��֤
    manage_certification =companyinfos[23]
    #��˾��ҳ
    try:
        homepage = companyinfos[28]
        print '������ҳ'
    except:
        homepage = ''

    sql = "insert into company_specific_info(name,homepage,products,main_field,business_type,business_mode,registered_address,business_address,established_time,legal_person,employee_num,annual_turnover,brand,registered_money,main_customer,main_market,annual_exports,annual_imports,bank,bank_account,oem,r_n_d,outputs,plant_area,quality_control,manage_certification,acquiredtime) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
    str(companyname),str(homepage),str(products),str(field),str(type),str(business_mode),str(registered_address),
    str(business_address),str(established_time),str(legal_person),str(employee_num),str(annual_turnover),
    str(brand),str(registered_money),str(main_customer),str(main_market),str(annual_exports),str(annual_imports),
    str(bank),str(bank_account),str(oem),str(r_n_d),str(outputs),str(plant_area),str(quality_control),
    str(manage_certification),str(acquiredtime))

    # print sql
    try:
        cursor.execute(sql)
    except Exception, e:
        print e


def get_commodity(commodity_html,companyname):
    bs = BeautifulSoup(commodity_html)
    itemlist = bs.select('li[class="itemList-li"]')
    # print len(itemlist)
    for elem in itemlist:
        # ��Ʒ�۸�
        commodity_price = elem.select('dd[class="itemPrice"]')[0].get_text().encode('utf-8')
        print commodity_price

        # ��Ʒ����
        commodity_name = elem.select('dd[class="itemModTit"]')[0].get_text().encode('utf-8')
        print commodity_name

        # pic = elem.select('img')
        # print pic
        # ��ƷͼƬ��ַ
        # ��ȡ��ǩ�ڵ�����
        commodity_picUrl = elem.select('img')[0].attrs['data-original']
        print commodity_picUrl
        updata_commodityInfo(companyname,commodity_name,commodity_price,commodity_picUrl)


def updata_commodityInfo(companyname,commodity_name,commodity_price,commodity_picUrl):
    # sql_tranform = 'SET NAMES utf8'
    # cursor.execute(sql_tranform)
    # ��ȡ��ǰ��ʱ��
    acquiredtime = str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))

    sql = "insert into commodity_info(companyname,commodity_name,commodity_price,commodity_picUrl,acquiredtime) values ('%s','%s','%s','%s','%s')" % (
        str(companyname), str(commodity_name), str(commodity_price), str(commodity_picUrl), str(acquiredtime))

    # print sql
    try:
        cursor.execute(sql)
    except Exception, e:
        print e


def getcompanyinfo2(html2):
    bs = BeautifulSoup(html2)
    companyinfo = bs.select('div[class="company-words"]')[1].find_all('span')
    # print '12321'
    print len(companyinfo)
    companyinfos = []
    for i in range(len(companyinfo)):
        elem = companyinfo[i].get_text().encode('utf-8')
        # print elem
        companyinfos.append(elem)
    print companyinfos
    updata_companyinfos2(companyinfos)


def updata_companyinfos2(companyinfos):

    # sql_tranform = 'SET NAMES utf8'
    # cursor.execute(sql_tranform)
    # ��ȡ��ǰ��ʱ��
    acquiredtime = str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))
    #��˾����
    companyname = companyinfos[0]
    #��Ҫ��Ʒ
    products = companyinfos[2]
    #��Ӫ��ҵ
    main_field = companyinfos[1]
    #��Ӫ��ַ
    business_address =companyinfos[3]
    #��˾����ʱ��
    established_time =companyinfos[4]
    #ע���ʱ�
    registered_money =companyinfos[5]


    sql = "insert into company_specific_info(name,products,main_field,business_address,established_time,registered_money,acquiredtime) values ('%s','%s','%s','%s','%s','%s','%s')" % (
    str(companyname),str(products),str(main_field),str(business_address),str(established_time),str(registered_money),str(acquiredtime))

    # print sql
    try:
        cursor.execute(sql)
    except Exception, e:
        print e



#��ȡ��������ҳ����Ʒ��Ϣ��selector��ʽ����
def get_commodityinfo2(commodity_html2,companyname):
    bs = BeautifulSoup(commodity_html2)
    #
    # itemlist = bs.select('div.product-every div.goods ul li')
    commodity_prices = bs.select('div.product-every div.goods ul li div.price')
    commodity_names = bs.select('div.product-every div.goods ul li div.A-title a')
    #���ַ�ʽ��ô���Ҳ���
    # commodity_name = bs.select('div.product-every div.goods ul li div:nth-of-type(1)')
    commodity_pics = bs.select('div.product-every div.goods ul li a img')
    print len(commodity_prices),len(commodity_names),len(commodity_pics)
    a= []
    b=[]
    c=[]
    for each in commodity_prices:
        #��Ʒ�۸�
        commodity_price = each.get_text().encode('utf-8')
        a.append(commodity_price)
        # print commodity_price

    for each in commodity_names:
        # ��Ʒ����
        commodity_name = each.get_text().encode('utf-8')
        b.append(commodity_name)
        # print commodity_name

    for each in commodity_pics:
        commodity_pic = each.attrs['src']
        c.append(commodity_pic)
        # print commodity_pic

    #������Ʒ��Ϣ�������ݿ�
    for i in range(len(a)):
        commodity_name = b[i]
        commodity_price = a[i]
        commodity_picUrl = c[i]
        # print '���µ�������վ��Ʒ'
        updata_commodityInfo(companyname, commodity_name, commodity_price, commodity_picUrl)



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

