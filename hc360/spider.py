# coding=gbk
import sys,re,time
import urllib2,urllib,cookielib
from lxml import etree
from ContentEncodingProcessor import ContentEncodingProcessor

class Fetcher():
    """ 封装连续抓网页和解析的方法和变量"""

    def __init__(self,host_url,proxy=None,cookie=None):
        self.host=host_url
        if self.host[-1]!='/':
           self.host='%s/' % self.host
        self.user_agent=('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
        # self.headers = {'User-Agent': self.user_agent}
        self.proxy_support=None
        self.opener=None
        self._setOpener(proxy,cookie)

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

    #组合s.hc360.com的搜索url
    def getSearchUrl(self,word,page_num,type='enterprise'):
        word = urllib.quote(word)  #字符串URL编码
        url_keyword = 'w=%s&mc=%s&ee=%s&af=9' % (word, type, page_num)
        nn_url = '%s?%s' %(self.host, url_keyword)
        return nn_url

    #组合js.hc360.com/cn/的省份名录url
    def getAreaUrl(self,area,pageNum):
        if pageNum<=1:
            return '%s%s/' % (self.host,area)
        else:
            return '%s%s/%s/' % (self.host,area,pageNum)

    #下载页面，如果失败返回None
    def downLoadPage(self,url,times=1):
        req = urllib2.Request(url, None, self.getHeader())
        for i in xrange(times):
            try:
                response = urllib2.urlopen(req, timeout=5)
                if response.geturl() != req.get_full_url():
                    # if response.code==302:
                    print 'Warning:重定向到验证码,url=%s,times=%s' % (req.get_full_url(), i)
                    continue
                else:
                    content = response.read()
                    # content=content.decode('gbk').encode('utf-8')
                    return content
            except urllib2.HTTPError, e:
                time.sleep(1)  # 暂停1s
                print 'Error:HTTPError:code=%s,reason=%s,times=%s' % (e.code, e.reason, i)
                continue
        return None

    #TODO: 添加被封时换代理or拨号
    # 下载js.hc360.com/cn/
    def downLoadCN(self, url, times=1):
        req = urllib2.Request(url, None, self.getHeader())
        for i in xrange(times):
            try:
                response = urllib2.urlopen(req)
                if response.code!=200:
                    if response.code==404:
                        print 'Warning:网站正在建设中,url=%s,times=%s' % (response.geturl(), i)
                    else:
                        print 'Warning:被封->%s url=%s,times=%s' % (response.response.read(),response.geturl(), i)
                    continue
                else:
                    content = response.read()
                    # content=content.decode('gbk').encode('utf-8')
                    return content
            except urllib2.HTTPError, e:
                time.sleep(1)  # 暂停1s
                print 'HTTPError:code=%s,reason=%s,times=%s,%s' % (e.code, e.reason, i,url)
                continue
        return None

    #根据关键词去搜索
    def getSearchContent(self,word,page_num,times,type='enterprise'):
        # word=self.encodeChinese(word)
        url=self.getSearchUrl(word,page_num,type)
        content=self.downLoadPage(url,times)
        return content

    #解析搜索结果返回（公司，url)列表
    def parseSearch(self,content):
        et=etree.HTML(content, parser=etree.HTMLParser(encoding='gbk'))  #默认用utf-8
        p_list=et.xpath('//p[@class="tilcomp"]')
        company_list=[]
        for p in p_list:
            name=p.xpath('./a/text()')[0]
            href=p.xpath('./a/@href')[0]
            company_list.append((name,href))
        if len(company_list)<=0:
            print 'Error:parseSearch:prase nothing!'
        else:
            print 'Debug:parseSearch: %s company,[1]= %s, %s' % (
                len(company_list),company_list[0][0].encode('GB18030'),company_list[0][1])
        return  company_list

    #解析极速版的企业目录
    def parseCN(self,content):
        et=etree.HTML(content, parser=etree.HTMLParser(encoding='gbk'))  #默认用utf-8
        c_name=et.xpath('//div[@class="c-name"]')
        company_list=[]
        for div in c_name:
            name = div.xpath('./a/text()')[0]
            href=div.xpath('./a/@href')[0]
            company_list.append((name, href))
        if len(company_list) <= 0:
            print 'Error: parseCN:prase nothing!'
        return  company_list


    #把列表追加写入文件中
    def writeList2file(self,companys,filename):
        if len(companys)==0:
            print 'Error:writeList2file :companys is empty'
            return 0
        write_num=0
        try:
            f = open(filename, 'a')
            for line in companys:
                str='%s,%s,%s\n' % (self.getTime(),line[0],line[1])#时间 名称 url
                f.write(str.encode('gbk'))  #从unicode专为gbk
                write_num+=1
        finally:
            f.close()
        #print 'writeList2file:open fail'
        return write_num

    #伪造头文件
    def getHeader(self):
        """ 冒充百度spider的UserAgent"""
        header = {}
        spider=['Sogou spider2','Sogou web spider','Googlebot','Sogou Orion spider','yisouspider']
        baidu='Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
        Safari='Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'
        Android='Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        header['User-Agent'] = Android
        header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        header['Accept-Encoding']='gzip, deflate, sdch'
        header['Accept-Language'] = 'zh-CN,zh;q=0.8'
        # header['Cache-Control'] = 'max-age=0'
        header['Connection'] = 'keep-alive'
        header['Host'] = 'js.hc360.com'
        header['Referer'] = 'http://js.hc360.com/cn/sh/'
        # header['Origin'] = 'Origin:http://s.hc360.com'
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


#在s.hc360.com搜索单个关键词
def crawOneKeyword(fetcher,word,savefile):
    print '---start crawling word=%s,%s---' % (word, fetcher.getTime())
    for page_num in xrange(1,101):
        page_content = fetcher.getSearchContent(word, page_num,3)
        time.sleep(2)
        if page_content==None:
            continue
        company_list = fetcher.parseSearch(page_content)
        if len(company_list)<=0:
            print 'Warning:company_list<=0'
            continue
        write_num=fetcher.writeList2file(company_list,savefile)
        if write_num<40:
            print 'Debug: end crawl word=%s,page=%s,%s' % (word,page_num,fetcher.getTime())
            break
    else:  #大于100页或者刚好完整100页
        print 'Warning: log:page_num>=100,end crawl word=%s,'%(word)

#从急速版里下载一个省份，从第一页中获得总页数
def crawOneArea(fetcher,province,saveFile):
    print '---start crawling province=%s,%s---' % (province, fetcher.getTime())
    url=fetcher.getAreaUrl(province,1)
    content=fetcher.downLoadCN(url,5)
    pLeft = '</s>页/共'
    start = content.find(pLeft)
    if start==-1:
        print 'Error: can not download fist page:%s' % url
        return
    start += len(pLeft)
    page_con = content[start:pLeft.find('页', start)].strip()
    fail_con=0
    for page_num in xrange(2,len(page_con)+1):  #do-while形式
        time.sleep(1)
        company_list=fetcher.parseCN(content)
        if len(company_list) <= 0:
            fail_con+=1
            print 'Error:parseCN company_list<=0,fail_con=%s' % fail_con
            continue
        write_num = fetcher.writeList2file(company_list, saveFile)
        print 'Debug:province=%s page=%s write_num=%s' % (province,page_num,write_num)
        url=fetcher.getAreaUrl(province,page_num)
        content = fetcher.downLoadCN(url, 5)

    print '---end crawling province=%s,%s---' % (province, fetcher.getTime())



if __name__=='__main__':
    print '---start js.hc360.com spider---%s' %time.strftime('%Y-%m-%d %X', time.localtime())
    search_host='http://js.hc360.com/cn/'

    import cityUtil
    provinces=cityUtil.getProvince()
    if provinces==None or len(provinces)<1:
        print '---getProvince fail.----'
        sys.exit()
    else:
        print '---get %s province---' % len(provinces)

    fetcher=Fetcher(search_host)
    for p in provinces:
        file_path='%s_companys.txt' % p
        crawOneArea(fetcher,p,file_path)

    print '---end js.hc360.com spider%s' %time.strftime('%Y-%m-%d %X', time.localtime())



