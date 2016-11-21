# coding=utf-8
__author__='hjb'
import time,sys,random
from fetcher import Fetcher


#下载一个城市，直到结束
def crawOneCity(fetcher,cityID,start,saveFile):
    print '---start crawling city=%s,%s---' % (cityID, fetcher.getTime())
    fetcher.setReferer(cityID=cityID,categoryID=0)
    isEnd = False
    fail_con=0
    for startIndex in xrange(start,sys.maxint,25):
        if isEnd==True:
            break
        url = fetcher.formUrl(start=startIndex, categoryid=0, cityid=cityID)  #种类0会返回所有类别的结果
        content = fetcher.downLoadContent(url,times=4)  #content is utf-8
        if content == None:
            with open('../result/fail_url.txt', 'a') as f:  # 记录失败的下来
                f.write('%s,%s' % (fetcher.getTime(), url))
                f.close()
            fail_con += 1
            continue
        # content = content.decode('utf-8')
        data_list, isEnd = fetcher.parseContent(content)

        if len(data_list) <= 0:
            fail_con += 1
            print 'Error:parseContent data_list<=0,fail_con=%s' % fail_con
            continue
        write_num = fetcher.writeList2file(data_list, saveFile)
        print 'Debug:city=%s startIndex=%s write_num=%s' % (cityID,startIndex,write_num)

    print '---end crawling city=%s,%s---' % (cityID, fetcher.getTime())


if __name__=='__main__':
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
        file_path = '../result/%s_city.txt' % c  # 按省份_company保存
        crawOneCity(fet,cityID=c,saveFile=file_path)

    print '---end spider %s ---' % time.strftime('%Y-%m-%d %X', time.localtime())



