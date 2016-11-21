# coding=utf-8
__author__='hjb'
import time,random
import urllib2,cookielib,json
from ContentEncodingProcessor import ContentEncodingProcessor
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class Fetcher():
    """ 封装连续抓网页和解析的方法和变量"""

    def __init__(self,host_url,proxy=None,cookie=None):
        self.host=host_url
        self.opener=None
        self._setOpener(proxy,cookie)
        self.referer=''

    def _setOpener(self,proxy=None,cookie=None):
        self.proxy_support = urllib2.ProxyHandler(proxy)
        if cookie!=None:  #更换cookie
            self.cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        else:
            self.cookie_support=urllib2.HTTPCookieProcessor(None)
        encoding_support = ContentEncodingProcessor
        self.opener = urllib2.build_opener(self.proxy_support,self.cookie_support,
                                           encoding_support,urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)

    def setReferer(self,cityID,categoryID):
        self.referer='http://%s/shoplist/%s/d/1/c/%s/s/s_-1?from=m_nav_1_meishi' % (self.host,cityID,categoryID)

    def formUrl(self,start=0, regionid=0, categoryid=0,sortid=0, locatecityid=0, cityid=1):
        ''' 根据关键字组成搜索URL'''
        host = 'http://%s/searchshop.json' % self.host
        _time = int(time.time() * 1000)
        callback = 'jsonp%s' % (_time + int(random.random() * 100))
        url = '%s?start=%s&regionid=%s&categoryid=%s&sortid=%s&locatecityid=%s&cityid=%s&_=%s&callback=%s' % (
        host, start, regionid, categoryid, sortid, locatecityid, cityid, _time, callback)
        print 'Debug: formUrl->%s' % url
        return url

    #TODO: 添加被封时换代理or拨号
    def downLoadContent(self, url, times=1,timeout=5):
        ''' 获取URL的内容 '''
        req = urllib2.Request(url, None, self.getHeader())
        # self.referer=url  #更新referer
        for i in xrange(times):
            try:
                response = urllib2.urlopen(req,timeout=timeout)
                # response.encoding='utf-8'

                if response.code!=200:
                    if response.code==404:
                        print 'Warning:404,url=%s,times=%s' % (response.geturl(), i)
                    else:
                        print 'Warning:被封->%s url=%s,times=%s' % (response.response.read(),response.geturl(), i)
                    time.sleep(3)  # 暂停1s TODO:换IP
                    continue
                else:
                    content = response.read()
                    print response.info
                    # content=content.decode('gbk').encode('utf-8')
                    return content
            except urllib2.HTTPError, e:
                time.sleep(random.randint(10,25)/10.0)  # 暂停1s
                print 'HTTPError:code=%s,reason=%s,times=%s,%s' % (e.code, e.reason, i,url)
                continue
        return None


    def parseContent(self,content):
        data_list=[]
        content = content[content.find('(') + 1:content.rfind(')')]
        data=json.loads(content)  #utf-8
        isEnd=data['isEnd']
        shop_list=data['list']
        # nextStartIndex=data['nextStartIndex']  #下一个起始索引
        if isEnd==True :
            print 'Debug: json search is end'

        if len(shop_list)<=0:
            print 'Error: json search has not list'
            return data_list
        for shop in shop_list:
            shopName=shop['name']
            shopID=shop['id']
            data_list.append((shopName,shopID))
        if len(data_list) <=0:
            print 'Error: parseContent nothing!'

        return data_list,isEnd


    #把列表追加写入文件中,返回写入条目的数量
    def writeList2file(self,write_list,filename):
        if len(write_list)==0:
            print 'Debug:writeList2file :write_list is empty'
            return 0
        write_num=0
        try:
            fl = open(filename, 'a')
            for line in write_list:
                s='%s %s\n' % (self.getTime(),str(line))#时间 名称 url
                # s=s.strip().replace(u'\u2006','').encode('gbk')  #非GBK编码空格字符要去掉 从unicode专为gbk
                fl.write(s)
                write_num+=1
            fl.close()
        except:
            print 'Error write file fail'
        return write_num

    #伪造头文件,伪造referer指向上一个位置
    def getHeader(self):
        header = {}
        spider=['Sogou spider2','Sogou web spider','Googlebot','Sogou Orion spider','yisouspider']
        baidu='Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
        Safari='Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'
        Android='Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        header['User-Agent'] = Android
        header['Accept'] = '*/*'
        # header['Accept-Encoding']='gzip, deflate, sdch'
        header['Accept-Language'] = 'zh-CN,zh;q=0.8'
        header['Cache-Control'] = 'no-cache'
        header['Connection'] = 'keep-alive'
        header['Host'] =self.host
        header['Referer'] = self.referer
        return header

    #函数urlencode不会改变传入参数的原始编码，默认GBK
    def encodeChinese(self,str):
        str=str.decode('utf-8').encode('gbk')
        return str

    #获得当前的格式化时间
    def getTime(self):
        ISOTIMEFORMAT='%Y-%m-%d %X'
        return time.strftime(ISOTIMEFORMAT, time.localtime())

    #从本地代理文件中读取代理列表
    def getProxyList(self,g_ProxyFile):
        with open(g_ProxyFile) as f:
            lines = f.readlines()
            g_ProxyList = [{'http': 'http://' + line.strip()} for line in lines]
            # proxy_it=0
            return g_ProxyList



if __name__=='__main__':
    fet=Fetcher('mapi.dianping.com')
    url=fet.formUrl(start=1,categoryid=10,cityid=129)
    content=fet.downLoadContent(url,3)
    print isinstance(content,str)
    content=content.decode('utf-8')
    print content,isinstance(content,unicode)
    data_list, isEnd=fet.parseContent(content)
    print len(data_list),isEnd,data_list[0],data_list[24]