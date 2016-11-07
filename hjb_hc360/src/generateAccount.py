#encoding=gbk
__author__='hjb'
import random

""" 批量生成注册邮箱和密码 """

def randomStr(l):
    ret = ''
    for i in xrange(l):
        ret += chr(ord('a') + random.randint(0,25))
    return ret

def GenerateAccount():
    for i in xrange(100000):
        base = randomStr(10)
        ret = {}
        ret['nickName'] = base
        ret['txtemail'] = base + '@163.com'
        ret['password'] = base + '_'
        yield ret

def RecordSuccess(account,g_SuccessFile):
    with open(g_SuccessFile,'a') as f:
        f.write(account['nickName'] + ' ' + account['txtemail']
                +' '+ account['password'] + '\n')



if __name__ == '__main__':
    GenerateAccount()
