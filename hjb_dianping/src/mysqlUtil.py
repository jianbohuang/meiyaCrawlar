# coding=utf-8
import pymysql,sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class SqlUtil():
    def __init__(self,database):
        try:
            conn=pymysql.connect(host='localhost',user='root',passwd='123456',db=database,charset="utf8")
            cur = conn.cursor()  # 获取cursor对象来进行操作
        except Exception ,e:
            print e
            sys.exit()

        self.conn=conn
        self.cur=cur

    def create_shop_table(self):
        sql = "CREATE TABLE IF NOT EXISTS shoplist (\
            nid        INT        NOT NULL AUTO_INCREMENT,\
            id         INT        NOT NULL ,\
            name       VARCHAR(100)   NULL,\
            adShop     TINYINT(1) NOT NULL DEFAULT 0,\
            authorityLabelType INT NOT NULL DEFAULT 6,\
            bookable   TINYINT(1)     NULL DEFAULT 0,\
            branchName VARCHAR(50)    NULL,\
            categoryId INT        NOT NULL,\
            categoryName VARCHAR(100) NULL,\
            cityId     INT        NOT Null,\
            defaultPic VARCHAR(255)   NULL,\
            hasDeals   TINYINT(1) NOT NULL DEFAULT 0,\
            hasMoPay   TINYINT(1) NOT NULL DEFAULT 0,\
            hasPromo   TINYINT(1) NOT NULL DEFAULT 0,\
            hasTakeaway TINYINT(1) NOT NULL DEFAULT 0,\
            hotelBookable TINYINT(1) NOT NULL DEFAULT 0,\
            matchText  VARCHAR(100)   NULL,\
            memberCardId INT      NOT NULL DEFAULT 0,\
            newShop    TINYINT(1) NOT NULL DEFAULT 0,\
            orderDish  TINYINT(1) NOT NULL DEFAULT 0,\
            queueable  TINYINT(1) NOT NULL DEFAULT 0,\
            priceText  VARCHAR(50)    NULL,\
            regionName VARCHAR(100)   NULL,\
            shopPower  INT            NULL,\
            shopType   INT        NOT NULL,\
            status     INT        NOT NULL DEFAULT 0,\
            tagList    VARCHAR(100)   NULL,\
            searchquery INT       NOT NULL,\
            PRIMARY KEY (id));"
        try:
            self.cur.execute(sql)
            print 'Debug: create shop table %s' %self.cur.rowcount
        except Exception, e:
            print e
            self.closeDB()

    def create_search_table(self):
        sql = "CREATE TABLE IF NOT EXISTS searchquery (\
            id        INT         NOT NULL AUTO_INCREMENT,\
            queryId   VARCHAR(50) NOT NULL,\
            isEnd     TINYINT(1)  NOT NULL DEFAULT 0,\
            startIndex     INT    NOT NULL DEFAULT 0,\
            url      VARCHAR(255) NULL,\
            recordCount    INT    NOT NULL,\
            created   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,\
            PRIMARY KEY (id));"
        try:
            self.cur.execute(sql)
            print 'Debug: create search table %s' %self.cur.rowcount
        except Exception, e:
            print e
            self.closeDB()

    def create_deal_table(self):
        sql = "CREATE TABLE IF NOT EXISTS deal(" \
              "id     INT      NOT NULL   AUTO_INCREMENT," \
              "dealId INT      NOT NULL   DEFAULT 0," \
              "imgSrc VARCHAR(255) NULL," \
              "title  VARCHAR(100) NULL," \
              "price  FLOAT    NOT NULL   DEFAULT 0," \
              "o_price FLOAT   NOT NULL   DEFAULT 0," \
              "soldNum FLOAT   NULL," \
              "created   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP," \
              "PRIMARY KEY (id));"
        try:
            self.cur.execute(sql)
            print 'Debug: create deal table %s' % self.cur.rowcount
        except Exception, e:
            print e
            self.closeDB()

    def clearTable(self,tableName):
        try:
            self.cur.execute("truncate table %s;" % tableName)
            self.conn.commit()
        except Exception, e:
            print e
            self.closeDB()

    def insertQuery(self,data):
        sql = "insert into searchquery (%s) values (%s)" % (
            ','.join(map(str, data.keys())), "'" + "','".join(map(str, data.values())) + "'")
        try:  #为了加快速度不考虑判断
            # self.cur.execute("select * from searchquery where queryId = %s" ,(data['queryId']))
            # if self.cur.rowcount == 0:
            self.cur.execute(sql)
            self.conn.commit()
            return self.cur.lastrowid
            # else:
            #     return self.cur.fetchone()[0]
        except Exception, e:
            print 'Error: insert query->%s\n%s' %(sql,e)
            # self.closeDB()
            return -1

    def insertShop(self,fieldStr,dataStr):
        sql = "insert into shoplist (%s) values %s" % (
            fieldStr, dataStr)
        try: #为了加快速度不考虑判断
            # self.cur.execute("select * from shoplist where id=%s" ,(data['id']))
            # if self.cur.rowcount == 0:
                self.cur.execute(sql)
                self.conn.commit()
                return self.cur.lastrowid
            # else:
            #     return self.cur.fetchone()[0]
        except Exception, e:
            print 'Error: insertShop->%s\n%s' %(sql,e)
            # self.closeDB()
            return -1

    def changeData(self,sqlStr):
        try:
            self.cur.execute(sqlStr)
            self.conn.commit()
            return self.cur.lastrowid
        except Exception, e:
            print 'Error: changeData->%s\n%s' % (sqlStr, e)
            return -1

    def selectData(self,sqlStr):
        try:
            self.cur.execute(sqlStr)
            ret=self.cur.fetchone()
            return ret
        except Exception ,e:
            print  'Error: select data fail'
            return 0

    def __del__(self):
        self.closeDB()

    def closeDB(self):
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    dbUtil = SqlUtil('dianping')

    ret=dbUtil.create_deal_table()
    print 'Debug:create deal tabler return=%s' % ret

    sql = 'alter table shoplist add address varchar(50) NULL,add phone varchar(50) NULL,add reviewNum int NULL;'
    ret=dbUtil.changeData(sql)
    print 'Debug:alter shoplist return=%s' % ret

    # import json
    # with open('../example.json','r') as f:
    #     content=f.read()
    #     f.close()
    # data=json.loads(content)
    #
    # shop_list = data['list']
    # shopData={}
    # for shop in shop_list:
    #     shopData['id'] = shop.get('id')
    #     shopData['name'] = shop.get('name')
    #     shopData['adShop'] = int (shop.get('adShop'))
    #     shopData['authorityLabelType'] = shop.get('authorityLabelType')
    #     shopData['bookable'] = int (shop.get('bookable'))
    #     shopData['branchName'] = shop.get('branchName')
    #     shopData['categoryId'] = shop.get('categoryId',6)
    #     shopData['categoryName'] = shop.get('categoryName')
    #     shopData['cityId'] = shop.get('cityId')
    #     shopData['defaultPic'] = shop.get('defaultPic')
    #     shopData['hasDeals'] = int (shop.get('hasDeals'))
    #     shopData['hasDeals'] = int (shop.get('hasDeals'))
    #     shopData['hasMoPay'] = int (shop.get('hasMoPay'))
    #     shopData['hasPromo'] = int (shop.get('hasPromo'))
    #     shopData['hasTakeaway'] = int (shop.get('hasTakeaway'))
    #     shopData['hotelBookable'] = int (shop.get('hotelBookable'))
    #     shopData['matchText'] = shop.get('matchText')
    #     shopData['memberCardId'] = shop.get('memberCardId')
    #     shopData['newShop'] = int (shop.get('newShop'))
    #     shopData['orderDish'] = int (shop.get('orderDish'))
    #     shopData['queueable'] = int (shop.get('queueable'))
    #     shopData['priceText'] = shop.get('priceText')
    #     shopData['regionName'] = shop.get('regionName')
    #     shopData['shopPower'] = shop.get('shopPower')
    #     shopData['shopType'] = shop.get('shopType')
    #     shopData['status'] = shop.get('status')
    #     shopData['tagList'] = str(shop.get('tagList'))


    # try:
        # create_shop_table(cur)
        # create_search_table(cur)
        # clearTable('pages')
    #     rowid=insertQuery(conn, cur, queryData)
    #     shopData['searchquery'] =rowid
    #     rowid=insertShop(conn,cur,shopData)
    #     print rowid
    # finally:
    #     cur.close()
    #     conn.close()

