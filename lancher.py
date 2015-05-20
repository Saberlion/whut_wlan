# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import urlparse
from lxml import _elementpath as DONTUSE
from lxml import etree

class RedirctHandler(urllib2.HTTPRedirectHandler):
    """docstring for RedirctHandler"""
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    def http_error_302(self, req, fp, code, msg, headers):
        pass

def getUnRedirectUrl(url,timeout=10):
    req = urllib2.Request(url)
    debug_handler = urllib2.HTTPHandler(debuglevel = 1)
    opener = urllib2.build_opener(debug_handler, RedirctHandler)

    html = None
    response = None
    try:
        response = opener.open(url,timeout=timeout)
        html = response.read()
    except urllib2.URLError as e:
        if hasattr(e, 'headers'):
            error_info = e.headers
        elif hasattr(e, 'code'):
            error_info = e.code
        elif hasattr(e, 'reason'):
            error_info = e.reason

    finally:
        if response:
            response.close()
    if html:
        return html
    else:
        if error_info["location"]:
            url = urllib.unquote(error_info["location"])
        else:
            url = error_info
        return url
#url = "http://172.30.16.58/srun_portal.php?cmd=login&switchip=172.30.12.247&mac=24:0a:64:f9:cd:02&ip=10.139.14.210&essid=WHUT-WLAN&apname=JB-JH-ITL-1508-C&apgroup=WHUT-JXBG-JH-AG&url=http%3A%2F%2Fwww%2Esrun%2Ecom%2F&ac_id=13&sys="
openurl = 'http://saberlion.info'
url = getUnRedirectUrl(openurl)
#print url
isWLAN = True


if url[0:len(openurl)] == openurl:
    isWLAN = False

user_ip = ''
mac = ''
nas_ip = ''
if isWLAN:
    url = 'http://saberlion.info'
    sock = urllib.urlopen(url)
    html = sock.read()
    print html
    page = etree.HTML(html)
    x = page.xpath('//html//head//meta')
    redirect_url = x[0].get('content')
    print redirect_url
    params = None
    if redirect_url:
        redirect_url = redirect_url[7:]
        print redirect_url
        UnRedirectUrl = getUnRedirectUrl(redirect_url)
        print UnRedirectUrl
        parses = urlparse.urlparse(UnRedirectUrl)
        print parses
        params = urlparse.parse_qs(parses.query, True)
        print params

        user_ip = params["ip"][0]
        mac = params["mac"][0]
        nas_ip = params["switchip"][0]

#用户名和密码

username = '*******'
password = '******'

post_data = urllib.urlencode({'action':'login',
                              'uid':'-1',
                              'is_pad':'0',
                              'force':'0',
                              'ac_id':'13',
                              'page_error':'/Fac_detect.php',
                              'pop':'1',
                              'ac_type':'h3c',
                              'rad_type':'',
                              'gateway_auth':'0',
                              'local_auth':'1',
                              'is_debug':'0',
                              'is_ldap':'0',
                              'user_ip':user_ip,
                              'mac':mac,
                              'nas_ip':nas_ip,
                              'ssid':'',
                              'vlan':'',
                              'wlanacname':'',
                              'wbaredirect':'',
                              'page_succeed':'http://172.30.16.53/help.html',
                              'page_logout':'http://www.whut.edu.cn',
                              'page_error':'http://172.30.16.53/help.html',
                              'username':username,
                              'password':password,
                              'save_me':'1',
                              'x':'72',
                              'y':'17'})

path = 'http://172.30.16.53/cgi-bin/srun_portal'
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Opera/9.23')]
urllib2.install_opener(opener)
req = urllib2.Request(path, post_data)
conn = urllib2.urlopen(req)

print conn.read()
#test webpage
bd = urllib2.urlopen(urllib2.Request('http://saberlion.info')).read()
print bd

input()
