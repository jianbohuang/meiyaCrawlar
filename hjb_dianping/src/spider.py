# coding=utf-8
__author__='hjb'
import time,sys,random,json
from fetcher import Fetcher

def getCategory(content):
    content = content[content.find('(') + 1:content.rfind(')')]
    data = json.loads(content)  # utf-8
    recordCount = data.get('recordCount')
    if recordCount<5100:  #记录少于5k可以一次遍历完
        return []
    categoryNavs=data.get('categoryNavs')
    category_list=[]
    for cate in categoryNavs:
        parentId=cate.get('parentId')
        id=cate.get('id')
        if (parentId==0 or parentId==10 or parentId==20 or parentId==90 ) and id!=10 and id!=20 and id!=90:
            category_list.append(id)
    return category_list

def getRegion(content):
    content = content[content.find('(') + 1:content.rfind(')')]
    data = json.loads(content)  # utf-8
    recordCount = data.get('recordCount',0)
    if recordCount<5100:
        return [],recordCount
    regionNavs=data.get('regionNavs')
    region_lsit=[]
    for region in regionNavs:
        parentId=region.get('parentId')
        if parentId == 0 and region.get('id') !=-10000:
            region_lsit.append(region.get('id'))

    return region_lsit,recordCount

# #下载一个城市，直到结束
# def crawOneCity(fetcher,cityID,start):
#     print '---start crawling city=%s,%s---' % (cityID, fetcher.getTime())
#     fetcher.setReferer(cityID=cityID,categoryID=0)
#     isEnd = False
#     fail_con=0
#     save_fail_con=0
#     for startIndex in xrange(start,5000,25): #单个索引最多翻到5000个
#         if isEnd==True:
#             break
#         url = fetcher.formUrl(start=startIndex, categoryid=0, cityid=cityID)  #种类0会返回所有类别的结果
#         content = fetcher.downLoadContent(url,times=4)  #content is utf-8
#         if content == None:
#             with open('../result/fail_url_%s.txt'%cityID, 'a') as f:  # 记录失败的下来
#                 f.write('fail_con=%s,%s' % (fail_con, url))
#                 f.close()
#             fail_con += 1
#             continue
#         list_len, isEnd = fetcher.parseContent(content,url)
#         if list_len <= 0 :
#             if list_len ==-1 :
#                 fail_con += 1
#                 print 'Error:parseContent fail_con=%s' % fail_con
#                 with open('../result/fail_url_%s.txt' % cityID, 'a') as f:  # 记录失败的下来
#                     f.write('fail_con=%s,%s' % (fail_con, url))
#                     f.close()
#                 fail_con += 1
#             elif list_len == 0 :
#                 save_fail_con += 1
#                 print 'Error:save Content fail_con=%s' % save_fail_con
#             elif list_len ==-2:
#                 print 'Debug:return empty list,isEnd=%s' % isEnd
#         else:
#             print 'Debug:city=%s startIndex=%s write_num=%s' % (cityID,startIndex,list_len)
#
#         time.sleep(random.randint(15, 30) / 10.0)  # 暂停1s
#
#     print '---end crawling city=%s,%s---' % (cityID, fetcher.getTime())


#下载一个城市，直到结束
def crawOneCity(fetcher,cityID,start):
    print '---start crawling city=%s,%s---' % (cityID, fetcher.getTime())
    fetcher.setReferer(cityID=cityID,categoryID=0)
    fail_con=0
    save_fail_con=0
    url = fetcher.formUrl(start=0, categoryid=0, cityid=cityID)  # 种类0会返回所有类别的结果
    content = fetcher.downLoadContent(url, times=10)  # content is utf-8
    if content == None:
        with open('../result/fail_url_%s.txt' % cityID, 'a') as f:  # 记录失败的下来
            f.write('fail_con=%s,%s' % (fail_con, url))
            f.close()
        print 'Error :Get start=0 fail,end up this city!'
        return

    # startbug=False#debug
    # startbug2=False
    region_lsit,recodCnt = getRegion(content) #获取业务种类和地区
    print'Debug: city %s has %s shop recod!' % (cityID,recodCnt)
    if len(region_lsit) >0 :
        for region in region_lsit:
            # if startbug ==False:#debug
            #     if region==12:
            #         startbug=True
            #     else:
            #         continue
            time.sleep(1)
            url = fetcher.formUrl(start=0, regionid=region,categoryid=0, cityid=cityID)
            content = fetcher.downLoadContent(url, times=5)  # content is utf-8
            categorys = getCategory(content)  # 获取业务种类和地区
            if  len(categorys) >0:
                for category in categorys:
                    # if startbug2 == False:  # debug
                    #     if category==60 :
                    #         startbug2 = True
                    #     continue
                    fail, save_fail=crawOneSearch(fetcher, region, category, cityID)
                    fail_con+=fail
                    save_fail_con+=save_fail
            else:
                fail, save_fail = crawOneSearch(fetcher, region, 0, cityID)
                fail_con += fail
                save_fail_con += save_fail
    else:
        fail, save_fail = crawOneSearch(fetcher, 0, 0, cityID)
        fail_con += fail
        save_fail_con += save_fail


    if fail_con>1000 or save_fail_con>1000:
        with open('../result/fail_url_%s.txt' % cityID, 'a') as f:  # 记录失败的下来
            f.write('fail_con=%s,%s' % (fail_con, url))
            f.close()
        print 'Error :Get start=0 fail,end up this city!'
    print '---end crawling city=%s,%s---' % (cityID, fetcher.getTime())


def crawOneSearch(fetcher, regionid, categoryid, cityID):
    isEnd = False
    fail_con = 0
    save_fail_con = 0
    for startIndex in xrange(0, 5000, 25):  # 单个索引最多翻到5000个
        if isEnd == True:
            break
        url = fetcher.formUrl(start=startIndex, regionid=regionid, categoryid=categoryid, cityid=cityID)  # 种类0会返回所有类别的结果
        content = fetcher.downLoadContent(url, times=5)  # content is utf-8
        if content == None:
            with open('../result/fail_url_%s.txt' % cityID, 'a') as f:  # 记录失败的下来
                f.write('fail_con=%s,%s' % (fail_con, url))
                f.close()
            fail_con += 1
            continue
        list_len, isEnd = fetcher.parseContent(content, url)
        if list_len <= 0:
            if list_len == -1:
                fail_con += 1
                print 'Error:parseContent fail_con=%s' % fail_con
            elif list_len == 0:
                save_fail_con += 1
                print 'Error:save Content fail_con=%s' % save_fail_con
            elif list_len == -2:
                print 'Debug:return empty list,isEnd=%s' % isEnd
        else:
            print 'Debug:city=%s startIndex=%s regionid=%s write_num=%s' % (cityID, startIndex,regionid, list_len)
        time.sleep(random.randint(7, 15) / 10.0)  # 暂停1s
    return fail_con,save_fail_con


if __name__=='__main__':
    if len(sys.argv)!=2:
        print 'usge: python spider.py startCityID endCityID'
        sys.exit()

    print '---start dianping.com spider---%s' %time.strftime('%Y-%m-%d %X', time.localtime())
    search_host='mapi.dianping.com'

    import cityUtil
    allCity, bigCity=cityUtil.getCity(False)
    if bigCity==None or len(bigCity)<1:
        print '---getCity fail.----'
        sys.exit()
    else:
        print '---get %s bigCity---' % len(bigCity)

    fet=Fetcher(search_host)
    for c in bigCity:
        if int(c)<sys.argv[1] or int(c)>sys.argv[2]:        #debug 26->50
            continue
        crawOneCity(fet,cityID=c,start=0)

    print '---end spider %s ---' % time.strftime('%Y-%m-%d %X', time.localtime())



