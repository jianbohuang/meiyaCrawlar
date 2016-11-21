# coding=utf-8
import urllib2
from lxml import etree
import string,time
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
"""  自动更新点评网的地级市 """
def updateCity():
    """ 因为地级市包含县级市，所以要过滤掉县级市 """
    city_list={}
    host_rul = 'http://wap.dianping.com'
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    header['Referer'] = 'http://wap.dianping.com/citylist'
    for char in string.uppercase:
        if char=='O' or char=='U' or char=='V':  #这些字母下没有城市
            continue
        cityList_url='http://m.dianping.com/citylist?c=%s&returl=&type=0&from=city_more' % char  #type=0为国内城市
        listReq=urllib2.Request(cityList_url,headers=header)
        rep=urllib2.urlopen(listReq,timeout=5)
        content=rep.read()
        if content==None:
            print 'Error: updateCity downLoad city list fail'
            return None
        et=etree.HTML(content,parser=etree.HTMLParser(encoding='utf-8'))
        j_citylist=et.xpath('//li')
        if len(j_citylist)<=0:
            print 'Error: Parse city list fail'
            return None
        count=0
        for li in j_citylist:
            href=li.xpath('./a/@href')
            data_id=li.xpath('./a/@data-id')
            name=li.xpath('./a/text()')
            if len(href)<=0 or len(data_id)<=0 or len(name)<=0:
                print 'Error: Parse href and data id fail at %s' % count
                continue
            city_list[data_id[0]]=[href[0],name[0]]
            count+=1
            print data_id[0],name[0]
        print 'Debug : get %s city in char=%s' % (count,char)
        time.sleep(1)

    print 'Debug: totally get %s city in china' % len(city_list)

    if city_list.has_key('4432'):   #移除点评实验室
        city_list.pop('4432')
    bigCity_id_list=[]
    count=0
    for city_id in city_list:
        href=city_list[city_id][0]
        city_url='%s%s' % (host_rul,href)
        cityReq=urllib2.Request(city_url,headers=header)
        try:
            cityResp=urllib2.urlopen(cityReq,timeout=5)
            content=cityResp.read()
            if content.find('<title>出错啦</title>') < 0:
                bigCity_id_list.append(city_id)
                print 'Debug: %s city id=%s' % (count, city_list[city_id][1])
                count += 1
        except:
            print u'Debug: 县级市'
        finally:
            time.sleep(3)
    write2file('cityList.txt', city_list, bigCity_id_list)
    return city_list,bigCity_id_list

def write2file(filename,city_list,bigCity_id_list):
    with open(filename,'w') as f:
        f.write('%s\n' % len(city_list))
        for key in city_list:
            f.write(('%s %s %s\n' % (key.strip(),city_list[key][0].strip(),city_list[key][1].strip())))

        f.write('\n%s\n' % len(bigCity_id_list))
        for id in bigCity_id_list:
            f.write('%s\n' %id)
        f.close()

def readfile(filename):
    allCity = {}
    bigCity = []
    with open(filename,'r') as f:
        count=int(f.readline())
        for i in xrange(count):
            city=f.readline().split()
            allCity[city[0]]=[city[1],city[2]]
        f.readline()
        count=int(f.readline())
        for i in xrange(count):
            city=f.readline()
            bigCity.append(city)
        f.close()

    return allCity,bigCity

def getCity(update=False):
    if update:
        return updateCity()
    else:
        return readfile('cityList.txt')

if __name__=='__main__':
    print 'test'
    city_List,bigCity_list=readfile('cityList.txt')
    print 'len=%s ,%s, %s ,%s' %(len(city_List),len(bigCity_list),city_List['1'][1].decode('utf-8'),bigCity_list[0])
# <h2>Oh? 500</h2>
# <title>出错啦</title>