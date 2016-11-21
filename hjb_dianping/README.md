大众点评团购数据采集
========
搜索采集团购类平台上餐厅、酒店、电影、旅游、购物等相关信息，形成平台信息库；
采集对应详情页面快照，形成网页库。

---------
./src/spider.py         代码入口，实现业务逻辑和<br>
./src/fetcher.py        封装爬虫网络交互部分的通用框架，包含网络交互和反爬虫处理。<br>
./src/crawlProxy.py     实现自动抓取代理验证可用代理，以及获取下一个不同的代理  <br>
./src/cityUtil.py       实现从点评网获取城市县区列表及其代号 <br>
./src/generateAccount.py实现gzip页面解压缩，使得爬虫支持gizp，加快速度 <br>
./result/               存放采集数据<br>
大众点评网的charset=utf-8 <br>
—————————————————————————————————————————————————————
驴妈妈
http://m.dianping.com/shoplist/19/search?from=m_search&keyword=
http://m.dianping.com/shoplist/19/search/加载时会显示小头像
http://m.dianping.com/shoplist/19/d/1/
http://m.dianping.com/shoplist/19/        加载时会显示小头像
http://m.dianping.com/shoplist/19/r/0/c/0/s/s_0 智能排序

品海，轮转时光
http://m.dianping.com/shoplist/19  Upgrade-Insecure-Requests  User-Agent:

颐和
http://m.dianping.com/shoplist/19/d/1/c/10/s/s_-1?from=m_nav_1_meishi
http://m.dianping.com/shoplist/19/d/1/c/10/s/s_-1
http://m.dianping.com/shoplist/19/d/1/c/10/s/


url规则：
http://m.dianping.com/shoplist/19/d/1/c/10/s/s_-1?from=m_nav_1_meishi
http://m.dianping.com/shoplist/19/search?from=m_search&keyword=
m.dianping.com/：手机站域名
shoplist    :商家列表
19          :cityID城市代号 1=上海
r,d         :regionID县区,r=0所有地区。 d 商区？
c=10        :category业务的种类，c=0代表所有业务。c=10代表美食业务
s           :sort排序，s=s_-1默认排序 ，
?from       :from指向来源页面
?keyword    :搜索的关键字

	http://m.dianping.com/shoplist/19/r/0/c/0/s/s_0 智能排序
	http://m.dianping.com/shoplist/19/r/0/c/0/s/s_1  距离最近
	http://m.dianping.com/shoplist/19/r/0/c/0/s/s_2  人气最高
	http://m.dianping.com/shoplist/19/r/0/c/0/s/s_3  评价最好
	http://m.dianping.com/shoplist/19/r/0/c/0/s/s_8  人均最低
	http://m.dianping.com/shoplist/19/r/0/c/0/s/s_9  人均最高
—————————————————————————————————————————————————————
AjaxUrl规则：
http://m.api.dianping.com/searchshop.json?start=25&regionid=0&categoryid=10
&sortid=0&locatecityid=19&cityid=19&_=1478595937130&callback=jsonp1478595937182

start:25        :起始个数，以0开始，每次返回25个
regionid:0      :县市地区
categoryid:0    :业务ID
sortid:0        :排序ID 每个sortid对应一个排序的type(网站目录中用到），
locatecityid:19 :当前定位城市ID
cityid:19       :目标城市ID
_:1478595937130 :毫秒时间
callback:jsonp1478595937182 :返回的jsonp开头名称 jsonp+(毫秒时间+0至100的随机数)

—————————————————————————————————————————————————————
返回json字段
根节点_queryid   代表当前json的ID，用于组建商家链接http的shoplistqueryid，可以忽略
categoryid  细分的业务ID，比如火锅135
categoryName  细分的业务名称
shopType 总的分类的业务类别，也是ID，是categoryid中的大类。比如35是景点，10是美食。
originalUrlKey
defaultPic   默认首页图片的URL
商家链接http://m.dianping.com/shop/23111550?from=shoplist&shoplistqueryid=c3127436-877a-4bc3-af68-915f80ede9a2

—————————————————————————————————————————————————————
http://m.dianping.com/tuan/dalian/list/0_13823_8_0
团购搜索结果页面 /全部类别_县区_排序方式_距离

latitude	float	纬度坐标，须与经度坐标同时传入，与城市名称二者必选其一传入
longitude	float	经度坐标，须与纬度坐标同时传入，与城市名称二者必选其一传入
offset_type	int	偏移类型，0:未偏移，1:高德坐标系偏移，2:图吧坐标系偏移，如不传入，默认值为0
radius	int	搜索半径，单位为米，最小值1，最大值5000，如不传入默认为1000
city	string	城市名称，可选范围见相关API返回结果，与经纬度坐标二者必选其一传入
region	string	城市区域名，可选范围见相关API返回结果（不含返回结果中包括的城市名称信息），如传入城市区域名，则城市名称必须传入
category	string	分类名，可选范围见相关API返回结果；支持同时输入多个分类，以逗号分隔，最大不超过5个。
keyword	string	关键词，搜索范围包括商户名、地址、标签等
out_offset_type	int	传出经纬度偏移类型，1:高德坐标系偏移，2:图吧坐标系偏移，如不传入，默认值为1
platform	int	传出链接类型，1:web站链接（适用于网页应用），2:HTML5站链接（适用于移动应用和联网车载应用），如不传入，默认值为1
has_coupon	int	根据是否有优惠券来筛选返回的商户，1:有，0:没有
has_deal	int	根据是否有团购来筛选返回的商户，1:有，0:没有
has_online_reservation	int	根据是否支持在线预订来筛选返回的商户，1:有，0:没有
sort	int	结果排序，1:默认，2:星级高优先，3:产品评价高优先，4:环境评价高优先，5:服务评价高优先，6:点评数量多优先，7:离传入经纬度坐标距离近优先，8:人均价格低优先，9：人均价格高优先
limit	int	每页返回的商户结果条目数上限，最小值1，最大值40，如不传入默认为20
page	int	页码，如不传入默认为1，即第一页
format	string	返回数据格式，可选值为json或xml，如不传入，默认值为json
