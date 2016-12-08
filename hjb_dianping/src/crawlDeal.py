# coding=utf-8
__author__='hjb'
import time,sys,random,json
from lxml import etree
from fetcher import Fetcher

fail_con=0
parseError_con=0
sqlError_con=0
def crawShopDeal():
    host = 'm.dianping.com'
    head_url = 'http://m.dianping.com/shop/'
    head_url_web = 'http://www.dianping.com/shop/'
    fet=Fetcher(host)
    dbUtil=fet.dbUtil
    s='select count(*) from shoplist where shopType=40'
    # ret=sql.selectData(s)
    # print ret
    global fail_con
    global sqlError_con
    global parseError_con
    for i in xrange(1,sys.maxint):
        sqlStr='select id,shopType,hasDeals,cityId from shoplist where cid=%s' % i
        ret=dbUtil.selectData(sqlStr)  #if select nothing return None
        if ret==None:
            s='Error:sql return None,count=%s,cid=%s' % (sqlError_con,i)
            print s
            with open('./sqlError.txt','a') as f:
                f.write('%s\n%s\n' % (fet.getTime(), s))
                f.close()
            sqlError_con+=1
            continue
        # shopID=int(ret[0])
        # shopType=int(ret[1])
        # hasDeals=int(ret[2])
        # cityId=ret[3]
        shopID=5447280
        shopType=15
        hasDeals=1
        cityId=19
        if shopType==35 and hasDeals==1:
            shopUrl = '%s%s' % (head_url_web, shopID)
            fet.host='www.dianping.com'
        else:
            shopUrl = '%s%s' % (head_url,shopID)
            fet.host=host
        fet.setReferer(shopType,cityId)
        content = fet.downLoadContent(shopUrl, times=7)  # content is utf-8
        if content == None:
            s='Fail:fail_con=%s id=%s shopType=%s,hasDeal=%s'%(fail_con,shopID,shopType,hasDeals)
            print s
            with open('../result/fail_url.txt', 'a') as f:  # 记录失败的下来
                f.write('%s\n%s\n' % (fet.getTime(), s))
                f.close()
            fail_con += 1
            continue
        if shopType == 35 and hasDeals == 1:
            ret=tripDeal(content)
        else:
            ret=test_parse(content,hasDeals)
        ##检查返回为空的情况
        shop=ret.get('shop')
        if len(shop)>0:
            fieldStr=','.join("%s='%s' " %(k,shop[k]) for k in shop )
            updateStr = "UPDATE shoplist SET %s WHERE cid=%s" % (fieldStr,i)  # 考虑以shopid进行查询，需要对id建立索引
            retCode=dbUtil.changeData(updateStr)
            print 'Debug:updateStr=%s,retCode=%s' % (updateStr,retCode)

        deal_list = ret.get('deal_list')
        if deal_list!=None:
            for deal in deal_list:
                fieldStr=','.join(deal.keys())
                dataStr="'%s'" % "','".join(map(str, deal.values()))
                insertStr = "insert into deal (%s) values (%s)" %(fieldStr, dataStr.decode())
                retCode=dbUtil.changeData(insertStr)
                print 'Debug:insertStr=%s,retCode=%s' % (insertStr,retCode)
        if len(shop)<1 or (deal_list!=None and len(deal_list)<1):
            s='ParseError:parseError_con=%s id=%s shopType=%s,hasDeal=%s,len(shop)=%s,deal_list=%s'%(parseError_con,shopID,shopType,hasDeals,len(shop),deal_list)
            print s
            with open('../result/parseError_content.txt', 'a') as f:  # 记录失败的下来
                f.write('%s\n%s\n%s\n' % (fet.getTime(), s,content))
                f.close()
            parseError_con += 1
            continue

        #将content快照 保存到本地
        date=time.strftime('%Y-%m-%d', time.localtime())
        with open('../result/%s_%s.txt' % (shopID,date), 'w') as f:  # 记录失败的下来
            f.write('%s' % content)
            f.close()

        time.sleep(random.randint(11, 22) / 10.0)  # 暂停1s


'''
三种不同类型的店铺美食 演出 电影院的页面分别使用不同的HTML结构
http://m.dianping.com/shop/8065256 http://m.dianping.com/shop/3513574 http://m.dianping.com/shop/22013895
'''
def test_parse(content,hasDeal):
    et = etree.HTML(content,parser=etree.HTMLParser(encoding='utf-8'))
    phones = et.xpath('//a[starts-with(@href,"tel:")]')
    address=et.xpath('//a[substring(@href, string-length(@href) - string-length("/map") +1) = "/map"]')#实现end-with()
    reviewNum =et.xpath('//a[contains(@onclick,"_viewreview")]')
    # add=address[0].xpath('./text()') #这方法在python下会返回包含子节点的文本
    ret={}
    shop={}
    if len(phones) != 0:
        shop.setdefault('phone',','.join([a.xpath('string(.)').strip()  for a in phones]))
    if len(address) !=0:
        shop.setdefault('address',address[0].xpath('string(.)').strip())
    if len(reviewNum)!=0:
        shop.setdefault('reviewNum',filter(lambda ch: ch in '0123456789',reviewNum[0].xpath('string(.)')))
    ret['shop']=shop
    if hasDeal==0:
        return ret

    tuan_list = et.xpath('//a[starts-with(@href,"/tuan/deal/")]')
    if len(tuan_list)<1:
        print 'Error: tuan_list len=%s!!' % len(tuan_list)
        return ret
    deal_list=[]
    for a in tuan_list:
        deal={}
        href = a.xpath('./@href')[0]
        img=a.xpath('.//img/@src')  #  部分亲子商家img src属性使用data-lazyload
        if len(img)<1:
            img=a.xpath('.//img/@data-lazyload')
        title = a.xpath('.//*[@class="newtitle"]/text()')
        price = a.xpath('.//span[@class="price"]/text()')  # 27.8
        o_price = a.xpath('.//span[@class="o-price"]/text()')  # ￥32
        soldNum = a.xpath('.//span[@class="soldNum"]/text()')#在移动版电影和旅游类的没有已售记录，电脑版代验证
        deal['dealId'] = href[11:]
        if len(img)>0:
            deal.setdefault('imgSrc',img[0])
        if  len(title)>0:
            deal.setdefault('title', title[0].strip())
        if  len(price)>0:
            deal.setdefault('price', filter(lambda ch: ch in '0123456789.', price[0]))#提取数字
        if  len(o_price)>0:
            deal.setdefault('o_price', filter(lambda ch: ch in '0123456789.',o_price[0]))
        if  len(soldNum)>0:
            deal.setdefault('soldNum', filter(lambda ch: ch in '0123456789',soldNum[0]))

        deal_list.append(deal)
        print 'Debug: print the deal: %s' % deal_list[len(deal_list)-1] #debug

    ret['deal_list']=deal_list
    return ret


#周边游的页面不一样,不在页面显示团购，需要到电脑版网页获取shopTpye=35
def tripDeal(content):
    et = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))  # 默认用utf-8
    address=et.xpath('//span[@itemprop="street-address"]')
    phones=et.xpath('//span[@itemprop="tel"]')
    reviewNum = et.xpath('//span[@class="sub-title"]')
    ret = {}
    shop = {}
    if len(phones) != 0:
        shop.setdefault('phone', ','.join([a.xpath('string(.)').strip() for a in phones]))
    if len(address) != 0:
        shop.setdefault('address', address[0].xpath('string(.)').strip())
    if len(reviewNum) != 0:
        shop.setdefault('reviewNum', filter(lambda ch: ch in '0123456789', reviewNum[0].xpath('string(.)')))
    ret['shop'] = shop
    print 'address=%s phones=%s,reviewNum=%s' %(len(address),len(phones),len(reviewNum))

    tag_tuan = et.xpath('//i[@class="tag tag-tuan"]')
    if len(tag_tuan)<1: #item big>2个才会有small
        print 'Error: tuan_list len=%s!!' % len(tag_tuan)
        return ret
    tuan_list=tag_tuan[:2] #前两个为big item
    deal_list=[]
    for i in tuan_list:
        deal = {}
        div=i.xpath('..')[0]
        href = div.xpath('./a/@href')[0]
        title=div.xpath('./p/text()')
        img = div.xpath('./img/@src')  # 部分亲子商家img src属性使用data-lazyload
        price=div.xpath('./span[@class="price"]/text()')
        del_price=div.xpath('./del/text()')
        soldNum=div.xpath('./span[@class="sold-count"]/text()')
        deal['dealId'] = href.split('/')[-1]  #http://t.dianping.com/deal/11863123
        if len(img) > 0:
            deal.setdefault('imgSrc', img[0])
        if len(title) > 0:
            deal.setdefault('title', title[0].strip())
        if len(price) > 0:
            deal.setdefault('price', filter(lambda ch: ch in '0123456789.', price[0]))  # 提取数字
        if len(del_price) > 0:
            deal.setdefault('o_price', filter(lambda ch: ch in '0123456789.', del_price[0]))
        if len(soldNum) > 0:
            deal.setdefault('soldNum', filter(lambda ch: ch in '0123456789', soldNum[0]))
        deal_list.append(deal)
        print 'Debug: print the deal: %s' % deal_list[len(deal_list) - 1]  # debug

    tuan_small=tag_tuan[2:]
    for i in tuan_small:
        deal = {}
        a=i.xpath('..')[0]
        href=a.xpath('./@href')[0]
        price=a.xpath('./span/text()')
        del_price=a.xpath('./del/text()')
        deal['dealId'] = href.split('/')[-1]
        if len(price) > 0:
            deal.setdefault('price', filter(lambda ch: ch in '0123456789.', price[0]))  # 提取数字
        if len(del_price) > 0:
            deal.setdefault('o_price', filter(lambda ch: ch in '0123456789.', del_price[0]))
        deal_list.append(deal)
        print 'Debug: print the deal: %s' % deal_list[len(deal_list) - 1]  # debug
    ret['deal_list']=deal_list
    return ret



if __name__=='__main__':
    crawShopDeal()


'''
旅游票务类shopType=35
旅游类在移动版大众点评网只显示订票信息而没有展示团购信息，
点评网旅游订票产品使用的是美团的订票页面
在电脑网页版只显示团购信息不显示订票信息(因为票务由美团在做）
查看网站js代码可知 移动版的订票信息是通过AJAX动态加载
因此可以通过两次分别访问AJAX和网页版分别获得订票和团购以及店铺地址电话信息
因为订票属于美团的链接，先不考虑抓订票的，抓电脑版的就好
http://www.dianping.com/shop/2117227
http://lvyou.meituan.com/mdr/api/v1/trip/deal/poi/full/18977113?client=wap&version=0.0&source=dp

'''
# shopType: '35'  http://lvyou.meituan.com/mdr/api/v1/trip/deal/poi/full/18977113?client=wap&version=0.0&source=dp

