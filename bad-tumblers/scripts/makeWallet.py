#-*- coding: utf-8 -*-

import requests
import time
import json
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

api_key = "[REDACTED]"

u = "https://api.blockcypher.com/v1/eth/main/addrs?token={}".format(api_key)
s = requests.session()

cnt = 0
for i in range(0,20):
	for j in range(0,200):
		try:
			if cnt % 20 == 0:
				print('[+] I\'m doing... {}'.format(cnt))
			r =s.post(u, verify=False)
			#print(r.content)
			rdict = json.loads(r.content)
			# print(rdict['private'])
			# print(rdict['public'])
			# print(rdict['address'])
			
			rtext = '{}:{}:{}'.format(rdict['private'],rdict['public'],rdict['address'])
			#print(rtext)
			with open('wallets.txt','a+') as f:
				f.write(rtext+'\n')
			time.sleep(0.33)
			cnt += 1
		except Exception as e:
			if r:
				print('[{}] err - {}'.format(r.status_code,str(e)))
			else:
				print('[[x] {}'.format(str(e)))
			print('{}'.format(r.content))
			now = datetime.datetime.now()
			nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
			print(nowDatetime)
			print('')
			time.sleep(30)
		except KeyboardInterrupt:
			print("[w]: Ctrl-C received, stopping…")
			exit(1)
		
