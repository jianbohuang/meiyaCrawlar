#encoding= utf-8
__author__ = 'hjb'
import urllib2,sqlite3,time
from lxml import etree


class GetProxy():
    """ 从www.xicidaili.com下载免费代理保存到本地,封装更换代理的接口. """

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.header={'User-Agent':self.user_agent}
        self.dbname="../proxy.db"  #代理数路径
        self.txt_path='../proxy.txt'  #代理路径
        self.now = time.strftime("%Y-%m-%d")
        self.timeout=2  #延时上限设置
        self.proxyList=[]
        self.proxyID = 0

    #执行抓取验证后保存数据到proxy.txt
    def getContent(self,num):
        # 国内高匿地址 host/nn/页数
        nn_url = "http://www.xicidaili.com/nn/" + str(num)
        req = urllib2.Request(nn_url, headers=self.header)
        resp = urllib2.urlopen(req, timeout=10)
        content = resp.read()
        et = etree.HTML(content)
        result_even = et.xpath('//tr[@class=""]')
        result_odd = et.xpath('//tr[@class="odd"]')

        for i in result_even:
            t1 = i.xpath("./td/text()")[:2]
            print "dul,IP:%s\tPort:%s" % (t1[0], t1[1])
            if self.isAlive(t1[0], t1[1]):
                self.insert_txt(self.now,t1[0],t1[1])
        for i in result_odd:
            t2 = i.xpath("./td/text()")[:2]
            print "odd,IP:%s\tPort:%s" % (t2[0], t2[1])
            if self.isAlive(t2[0], t2[1]):
                self.insert_txt(self.now,t2[0],t2[1])

    def insert_db(self,date,ip,port):
        dbname=self.dbname
        try:
            conn=sqlite3.connect(dbname)
        except:
            print 'open %s db fail' %self.dbname
        create_tb='''
        CREATE TABLE IF NOT EXISTS PROXY
        (DATE TEXT,
        IP TEXT,
        PORT TEXT
        );
        '''
        conn.execute(create_tb)
        insert_db_cmd='''
        INSERT INTO PROXY (DATE,IP,PORT) VALUES ('%s','%s','%s');
        ''' %(date,ip,port)
        conn.execute(insert_db_cmd)
        conn.commit()
        conn.close()

    def insert_txt(self,data,ip,port):
        txt_path=self.txt_path
        f=open(txt_path,'a')  #追加内容
        f.write('%s,%s:%s\n'%(data,ip,port))
        f.close()

    #下载多少页
    def loop(self,page=5):
        for i in range(1,page):
            self.getContent(i)

    #查看爬到的代理IP是否还能用
    def isAlive(self,ip,port):
        proxy={'http':ip+':'+port}
        print proxy

        proxy_support=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        #使用代理访问慧聪网，进行验证代理是否有效
        test_url="http://www.hc360.com"
        req=urllib2.Request(test_url,headers=self.header)
        try:
            #timeout设置延迟
            resp=urllib2.urlopen(req,timeout=self.timeout)

            if resp.code==200:
                print "work"
                return True
            else:
                print "not work"
                return False
        except :
            print "Not work"
            return False

    #检查数据库里面的数据时候还有效，没有的话将其纪录删除
    def check_db_pool(self):
        conn=sqlite3.connect(self.dbname)
        query_cmd='''
        select IP,PORT from PROXY;
        '''
        cursor=conn.execute(query_cmd)
        for row in cursor:
            if not self.isAlive(row[0],row[1]):
                #代理失效，从数据库从删除
                delete_cmd='''
                delete from PROXY where IP='%s'
                ''' %row[0]
                print "delete IP %s in db" %row[0]
                conn.execute(delete_cmd)
                conn.commit()

        conn.close()

    #检查代理数据
    def check_proxy_txt(self):
        f=open(self.txt_path,'r+')
        try:
            txt=f.read()
        finally:
            f.close()
            print 'open txt fail'

        for line in f:
            ls=line.split(',')
            if not self.isAlive(ls[1],ls[2]):
                # 代理失效，删掉
                txt.replace(line,'')
                print 'delete ' +line
        f.seek(0)
        f.write(txt)
        f.close()

    #加载代理数据
    def loadProxyFile(self,proxyfile):
        with open(proxyfile) as f:
            lines = f.readlines()
            self.proxyList = [{'http': 'http://' + line.strip().split(',')[1]} for line in lines]

    #获取下一个代理，返回None表示无代理可用
    def getProxy(self):
        print 'Usg:handler = urllib2.ProxyHandler({"http": "http://211.167.112.16:82"})'
        global g_ProxyIt
        if self.proxyID >= len(self.proxyList):
            print 'Error:None proxy leave'
            return None
        self.proxyID += 1
        print self.proxyList[g_ProxyIt - 1]
        return self.proxyList[g_ProxyIt - 1]



if __name__ == "__main__":
    now = time.strftime('%Y-%m-%d %X', time.localtime())
    pn=5
    print "Start at %s ,craw %s page" % now,pn
    obj=GetProxy()
    open(obj.txt_path,'w+').close()  #清空proxy.txt
    obj.loop(pn)
    #obj.check_db_pool()