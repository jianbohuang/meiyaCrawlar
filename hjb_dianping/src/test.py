# coding=utf-8
import os,time ,sys,locale,re
import urllib,urllib2,cookielib
from ContentEncodingProcessor import ContentEncodingProcessor
from lxml import etree

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 转换单个string为url编码
# def my_urlencode(str) :
#     str=str.decode('utf-8').encode('gbk')
#     reprStr = repr(str).replace(r'\x', '%')
#     return reprStr[1:-1]
chrome_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
header={'User-agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322)','Upgrade-Insecure-Requests':1}
header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
# header['Accept-Encoding'] = 'gzip, deflate, sdch'
url='http://s.hc360.com/'
data={}
data['ee']='2'
# data['w']=str.decode('utf-8').encode('gbk')
data['af']='3'
data['mc']='enterprise'

# url_keyword = 'w=' + urllib.quote(str.decode('utf-8').encode('gbk')) + '&mc=' + 'enterprise' + '&ee=2'+ '&af=9'
# nn_url=url+'?'+url_keyword
# req = urllib2.Request(nn_url,None,header)
# print req.get_full_url()
# # proxy=None
# # proxy_support = urllib2.ProxyHandler(proxy)
# # opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
# # urllib2.install_opener(opener)
# encoding_support = ContentEncodingProcessor
#  #直接用opener打开网页，如果服务器支持gzip/defalte则自动解压缩
# cookie_support= urllib2.HTTPCookieProcessor(None)
# proxy_support = urllib2.ProxyHandler({})
# opener = urllib2.build_opener( proxy_support, cookie_support,encoding_support, urllib2.HTTPHandler )
# urllib2.install_opener(opener)
# print req.header_items()

# resp = urllib2.urlopen(req)
# content=resp.read()
# print resp.info()
# print content.decode('gbk').encode('utf-8')
#
companys=[('控制','起b')]
# print 'parseSearch: %s company,[1]= %s, %s' % (len(companys), companys[0][0], companys[0][1])
# print u'\xd5'.encode('GB18030')
# print  sys.getfilesystemencoding()
# print locale.getdefaultlocale()

# re_str=r'(province:\[.+?\])'
# pattern=re.compile(re_str)
# content = re.findall(pattern,page)
#
# province_list=[]
# for i in content:
#     exec(i.replace(':','='))#执行字符串中的代码
#     province_list=province_list+province
#
# re_city=r'(city(.+?)})'
# pattern=re.compile(re_city)
# content=re.findall(pattern,page)
# print content
# city_list=[]#各省城市列表
# for i in content:
#     print i
#     i=i[:-1].replace(':','=')#去掉}和更改:
#     print i
#     exec(i)
#     city_list=city_list+city
# print city_list
# exec(page)
import json

# data = {
#     'name': 'ACME',
#     'shares': 100,
#     'price': 542.23
# }
# d=[]
# d.append(('a','b'))
# print 'data=%s,,%s' % (str(d[0]),d[0])
# with open('../example.json','r') as f:
#     content=f.read()
#     content=content[content.find('(')+1:content.rfind(')')]
#     js =json.loads(content)
#     if(not js['isEnd']):
#         print 'f'
#     print js['list'][0]
#     f.close()
# a=[]
# a.append(('1','2','3'))
# a.append(('0',1,2))
#
# for line in urls:
#     file_path=line.split('/')[-1]
#     print line,file_path
#     # urllib.urlretrieve(line, file_path)
#     req=urllib2.Request(line)
#     resp=urllib2.urlopen(req)
#     s=resp.read()
#     foo=open(file_path,'wb')
#     foo.write(s)
#     foo.close()
# s=u'哈哈'
# t='哈哈你好'
# print t
# print isinstance(s, unicode)
# s=s.encode('utf-8')
# print isinstance(s, str)
#
# print isinstance(t,str),t
# t=t.decode('utf-8')
# print isinstance(t,unicode),t
import  sys
print sys.maxint
