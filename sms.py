import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json


timestamp=int(time.time() * 1000)
timestamp=str(timestamp)

# access key
access_key = 'm5bIyITDeH0kEW8K3sZ4' 
# secret key
secret_key = 'LS6N46NhCZmxOqbbsIDi42gQdbc1Lzk24qIyk12x'

url="https://sens.apigw.ntruss.com"
uri="/sms/v2/services/ncp:sms:kr:274685171933:network_secu/messages"

to_number= '01083006062'                 #받는 사람
contents= '개인 정보가 유출되었습니다'    #메시지 내용

def	make_signature():
	global secret_key
	global access_key
	global timestamp
	global url
	global uri
	secret_key = bytes(secret_key, 'UTF-8')
	method = "POST"
	message = method + " " + uri + "\n" + timestamp + "\n" + access_key
	message = bytes(message, 'UTF-8')
	signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
	return signingKey


header = {

"Content-Type": "application/json; charset=utf-8",
"x-ncp-apigw-timestamp": timestamp, 
"x-ncp-iam-access-key": access_key,
"x-ncp-apigw-signature-v2": make_signature()
}


data = {
    "type":"SMS",
    "from":"01029334310",
    "content":contents,
	"subject":"SENS",
    "messages":[
        {
            "to":to_number,
        }
    ]
}


res = requests.post(url+uri,headers=header,data=json.dumps(data))
datas=json.loads(res.text)
reid=datas['requestId']

print(res.text+"\n")