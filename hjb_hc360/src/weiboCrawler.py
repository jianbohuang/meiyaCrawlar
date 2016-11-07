# coding=utf-8
__author__='hjb'
import urllib2,os
import urllib
import cookielib
import sys
import re
import lxml.html as HTML
import socket
import demjson
import time
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
class Fetcher(object):
    def __init__(self, username=None, pwd=None, cookie_filename=None):
        #获取一个保存cookie的对象
        self.cj = cookielib.LWPCookieJar()
        if cookie_filename is not None:
            self.cj.load(cookie_filename)
        #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        self.cookie_processor = urllib2.HTTPCookieProcessor(self.cj)
        #创建一个opener,将保存了cookie的http处理器，还有设置一个handler用于处理http的url的打开
        self.opener = urllib2.build_opener(self.cookie_processor, urllib2.HTTPHandler)
        #将包含了cookie、http处理器、http的handler的资源和urllib2对象绑定在一起
        urllib2.install_opener(self.opener)

        self.username = username
        self.pwd = pwd
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        'Referer':'','Content-Type':'application/x-www-form-urlencoded'}

    def get_rand(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows;U;Windows NT 5.1;zh-CN;rv:1.9.2.9)Gecko/20100824 Firefox/3.6.9',
                   'Referer':''}
        req = urllib2.Request(url ,"", headers)
        urllib2.ProxyHandler('')
        login_page = urllib2.urlopen(req).read()
        rand = HTML.fromstring(login_page).xpath("//form/@action")[0]
        passwd = HTML.fromstring(login_page).xpath("//input[@type='password']/@name")[0]
        vk = HTML.fromstring(login_page).xpath("//input[@name='vk']/@value")[0]
        return rand, passwd, vk

    def login(self, username=None, pwd=None, cookie_filename=None):
        if self.username is None or self.pwd is None:
            self.username = username
            self.pwd = pwd
        assert self.username is not None and self.pwd is not None

        url = 'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=4'
        #获取随机数rand、password的name和vk
        rand, passwd, vk = self.get_rand(url)
        print rand
        data = urllib.urlencode({'mobile': self.username,
                                 passwd: self.pwd,
                                 'remember': 'on',
                                 'backURL': 'http://weibo.cn/',
                                 'backTitle': '微博',
                                 'vk': vk,
                                 'submit': '登录',
                                 'encoding': 'utf-8'})
        url = 'http://login.weibo.cn/login/' + rand
        page =self.fetch(url,data)

        #link="http://weibo.cn/search/mblog?hideSearchFrame=&keyword=金融&advancedfilter=1&hasori=1&starttime=20141001&endtime=20141005&sort=hot&hasv=1&page=2"
        #result=self.fetch(link, "").decode('utf-8')

        #保存cookie
        if cookie_filename is not None:
            self.cj.save(filename=cookie_filename)
        elif self.cj.filename is not None:
            self.cj.save()
        print self.cj
        #link="http://weibo.cn/search/mblog?hideSearchFrame=&keyword=金融&advancedfilter=1&hasori=1&starttime=20141001&endtime=20141005&sort=hot&hasv=1&page=2"
        #result=self.fetch(link, "").decode('utf-8')
        #opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        #searchURL='http://weibo.cn/search/mblog/?keyword=helloworld'
        #result=self.opener.open(searchURL).decode('utf-8')
        print 'login success!'
        #print data
        #print result
        #print page1
        

    def fetch(self, url,data):
        print 'fetch url: ', url
        req = urllib2.Request(url,data, headers=self.headers)
        return urllib2.urlopen(req).read()

    def return_search_url(self,keyword,start_time,end_time):
        link="http://s.weibo.com/weibo/%s&scope=ori&suball=1&timescope=custom:%s:%s&Refer=g"%(keyword,start_time,end_time)
        return link

def getWeibos(page):
    weibolist=[]
    hasNextPage=False
    nextPageUrl=None
    content=demjson.decode(page)[u'html']
    soup=BeautifulSoup(content,'html.parser')
    notResult=False
    if soup.find('div',class_='pl_noresult'):
        notResult=True
    dataList=soup.find_all('div',class_='content clearfix')
    for data in dataList:
        weibo_data={
            'userid':None,
            'txt':None,
            'time':None,
            'img_url':None,
            'url':None
        }
        list=data.find('a',class_='name_txt W_fb')['href'].split('/')
        weibo_data['userid']=list[len(list)-1]
        weibo_data['txt']=data.find('p',class_='comment_txt').get_text()
        time=data.find('a',class_='W_textb')['title'].split(' ')
        weibo_data['time']=time[0].replace('-','')+time[1].split(':')[0]
        if data.find('img',class_='bigcursor'):
            weibo_data['img_url']=data.find('img',class_='bigcursor')['src']
        weibo_data['url']=data.find('a',class_='W_textb')['href']
        weibolist.append(weibo_data)
    if soup.find('div',class_='WB_cardwrap S_bg2 relative').find(text='下一页'):
        hasNextPage=True
        nextPageUrl=soup.find('div',class_='WB_cardwrap S_bg2 relative').find('a',class_='page next S_txt1 S_line1')['href']
    return weibolist,hasNextPage,nextPageUrl,notResult

def get_script_content(page,id):
    re_str=r'STK && STK.pageletM && STK.pageletM.view\({\"pid\":\"%s\"(.*)}\)'%id
    pattern=re.compile(re_str)
    content=pattern.search(page).group().replace('STK && STK.pageletM && STK.pageletM.view(','').strip(')')
    return content

def crawlWeibo(startTime,endTime):
    user1=['antony11@126.com','zhouyiyi19890420']
    user2=['18559827007','woshitia']
    account_list=[]
    account_list.append(user1)
    account_list.append(user2)
    weibolists=[]
    fet=Fetcher()
    fet.login(account_list[0][0],account_list[0][1])
    result=fet.fetch(fet.return_search_url('习马会',startTime,endTime),'')
    try:
        page=get_script_content(result,'pl_weibo_direct')
    except:
        print '需要进行验证'
        raw_input('press enter')
        return
    weibolist,hasNextPage,nextPageUrl,notResult=getWeibos(page)
    for one in weibolist:
        weibolists.append(one)
    print '当前抓取的微博数为'+str(len(weibolists))
    i=1
    iterTime=1
    second_user=False
    print hasNextPage
    print '第'+str(i)+'页'
    #for one in weibolist:
        #print one['txt']
    while(hasNextPage):
        nextUrl='http://s.weibo.com/'+nextPageUrl
        if iterTime==5 or iterTime==10:
            if second_user==False:
                d=1
                print '使用第二个账户抓取'
                second_user=True
            else:
                d=0
                second_user=False
                print '使用第一个用户抓取'
            fet.login(account_list[d][0],account_list[d][1])
        if iterTime==10:
            print '暂停爬取2分钟'
            time.sleep(120)
            iterTime=0
        try:
            result=fet.fetch(nextUrl,'')
            page=get_script_content(result,'pl_weibo_direct')
            weibolist,hasNextPage,nextPageUrl,notResult=getWeibos(page)
            for one in weibolist:
                weibolists.append(one)
            print '当前抓取的微博数为'+str(len(weibolists))
            i=i+1
            print '第'+str(i)+'页'
            #for one in weibolist:
              #  print one['txt']
        except:
            print '最后一条抓到微博的时间为'
            print weibolist[len(weibolist)-1]['time']
            return weibolist[len(weibolist)-1]['time'],weibolists,notResult
        iterTime=iterTime+1
        time.sleep(3)
    return weibolist[len(weibolist)-1]['time'],weibolists,notResult

def writeWeiboToFile(filepath,weibolist):
    if not os.path.exists(filepath):
        file=open(filepath,'w')
    else:
        file=open(filepath,'a')
    for one in weibolist:
        file.write(str(one)+'\n')
def changeTimeFormat(str):
    time=str[0:4]+'-'+str[4:6]+'-'+str[6:8]+'-'+str[8:10]
    return time


if __name__=='__main__':
    #time=crawlWeibo()
    filepath='/Users/antony/Desktop/ximahui_text.txt'
    dTime=20151101
    hTime=0
    print '开始抓取'
    for i in range(0,29):
        for j in range(0,23):
            startTime=str(dTime)+str(hTime+j)
            endTime=str(dTime)+str(hTime+j+1)
            print changeTimeFormat(endTime)
            print '抓取第'+str(i+1)+'天,第'+str(j+1)+'小时。'
            try:
                lastTime,weibolist,notResult=crawlWeibo(changeTimeFormat(startTime),changeTimeFormat(endTime))
            except:
                continue
            if notResult:
                print '没有想要的结果'
                time.sleep(3)
                continue
            print 'wei bo num'+str(len(weibolist))
            writeWeiboToFile(filepath,weibolist)
            time.sleep(10)
        dTime=dTime+1
