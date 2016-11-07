meiyaCrawlar
========  

上传源码后记得提交commit和pull request合并master主分支
--------

请在项目文件夹下新建Readme.md,注明一下自己项目目录结构和程序的入口，<br>
方便自己和大家阅读使用

### 使用类似目录结构
    |根目录
    |     |—— hjb_hc360  姓名+项目的名字<br>
    |         |—— README.md 项目说明<br>
    |         |—— src    .py源码<br>
    |         |—— result .scv .txt等数据<br>
    |
    |     |—— zsl_hc360  姓名+项目的名字
    |         |—— README.md 项目说明
    |         |—— src    .py源码
    |         |—— result ./.scv .txt等数据
    |
    |     |—— lf_hc360   姓名+项目的名字
    |         |—— README.md 项目说明
    |         |—— src    .py源码
    |         |—— result ./.scv .txt等数据
### 使用类似目录结构
>根目录
>>hjb_hc360  姓名+项目的名字
>>README.md 项目说明
>>src    .py源码
>>result .scv .txt等数据
>
>zsl_hc360  姓名+项目的名字
>>README.md 项目说明
>>src    .py源码
>>result ./.scv .txt等数据
>
>lf_hc360   姓名+项目的名字
>>README.md 项目说明
>>src    .py源码
>>result ./.scv .txt等数据
### 根目录目录结构
    |根目录
    |   |—— download 从网上下载下来的原验证码图片，未经过处理
    |   |—— 1_gray 灰度化处理过的图片
    |   |—— 2_cfs 使用CFS连通域切割之后的图片
    |   |—— 3_drop 使用滴水算法切割之后的图片
    |   |—— 4_scale 缩放成16X16像素之后的图片
    |   |—— svm 使用livsvm建立的训练集，模型，以及分类的结果都保存在这里
    |   |—— src java的源代码
    |   |—— 其它的目录都是用来测试的
