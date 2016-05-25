import requests
import Image
import rsa
import binascii
import json
import re
import time



session = requests.Session()

captcha = session.get('http://www.bilibili.com')
c = captcha.cookies
captcha = session.get('http://passport.bilibili.com/login', cookies=c)
print captcha.cookies
captcha = session.get('http://passport.bilibili.com/captcha')
sessionCookies = captcha.cookies

f = open('pic.jpeg','wb')
f.write(captcha.content)
f.close()
im=Image.open('pic.jpeg')
im.show()

jsonText = session.get('http://passport.bilibili.com/login?act=getkey', cookies=sessionCookies)
token = json.loads(jsonText.content)
print jsonText.content
username = 'user'
passwd = 'pass'
vdcode = raw_input('Enter captcha > ')
def encryptpwd(passwd,token):
    password = token['hash'] + passwd
    pub_key = token['key']
    pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
    message = rsa.encrypt(str(password),pub_key)
    message = binascii.b2a_base64(message)
    return message
encrypass = encryptpwd(passwd, token)

postdata = {
    'act':'login',
    'gourl':'',
    'keeptime':'2592000',
    'userid':username,
    'pwd':encrypass,
    'vdcode':vdcode
    }
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
jsonText = session.post('http://passport.bilibili.com/login/dologin', postdata, cookies=sessionCookies)

#获取av信息
av = 4757328
cont = session.get('http://www.bilibili.com/video/av'+str(av))
m = re.search('cid=\d*',cont.content)
cid = m.group()[4:]
t = time.strftime('%Y-%m-%d %H:%M:%S')

#aid为视频的av号
def postdanmu(content, t, pt): 
    postdata = {
        'mode':0, #0为顶端弹幕，如果你要发送顶端的，改成1
        'color':'16777215', #还没测试其他颜色，先用白的试试吧
        'message': content, #弹幕内容
        'pool':'0', #这个字段什么鬼
        'playTime': pt, #在视频中的时间轴
        'cid': cid, 
        'fontsize': 25, #字体大小，两种规格，这个是那个小的
        'rnd': 1485739224, #好像是个时间参数，蛋疼啊，到底怎么来的，算了，随便生成一个好了_(:з」∠)_
        'data': str(t) 
    }
    return session.post('http://interface.bilibili.com/dmpost?cid='+str(cid)+'&aid='+str(av)+'&pid=1', postdata)
#这里是测试，批量发送再说
test = postdanmu('hahaha', t, 0)