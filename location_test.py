# coding=utf-8
import hashlib
import hmac
import base64
import requests
import time
import urllib.request
import json

def make_signature(method, basestring, timestamp, access_key, secret_key):
    message = method + " " + basestring + "\n" + timestamp + "\n" + access_key
    signature = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    
    return signature

def requestApi(timestamp, access_key, signature, uri):
    
    headers = {'x-ncp-apigw-timestamp': timestamp,
               'x-ncp-iam-access-key': access_key,
               'x-ncp-apigw-signature-v2': signature}
    res = requests.get(uri, headers=headers)
    res_content = (res.content.decode('utf-8'))
    locate = json.loads(res_content)['geoLocation']
    return locate['r1']+" "+locate['r2']+" "+locate['r3']
    
def main():
    data = json.loads(urllib.request.urlopen("http://ip.jsontest.com/").read())
    method = "GET"
    basestring = '/geolocation/v2/geoLocation?ip='+data['ip']+'&ext=t&responseFormatType=json'
    timestamp = str(int(time.time() * 1000))
    access_key = "4FksYdL6OGNhHKLoShpk"
    secret_key = b"ROQSba3Y392ykrvbNS5vlnd23BfPLXnW68ol3B4y"
    signature = make_signature(method, basestring, timestamp, access_key, secret_key)
    hostname = "https://geolocation.apigw.ntruss.com"
    requestUri = hostname + basestring
    user_locate = requestApi(timestamp, access_key, signature, requestUri)

    return user_locate 
if __name__ == "__main__":
    location = main()
    print(location)
