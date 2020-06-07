#-*- coding: utf-8 -*-
import requests
import time
import json
import os
os.environ['WEB3_INFURA_PROJECT_ID']='redacted'
import random
from web3.auto.infura.ropsten import w3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

u='https://faucet.metamask.io/'

headers = {
'Content-Length': '42',
'Content-Type': 'application/rawdata',
'Host': 'faucet.metamask.io',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4103.61 Safari/537.36',
'Accept': '*/*',
'Origin': 'https://faucet.metamask.io',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Dest': 'empty',
'Referer': 'https://faucet.metamask.io/',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',

}

with open('./wallets.txt','r') as f:
  lines = f.read().split('\n')

with open('./giveEth_log2.txt','r') as f:
  cnt = len(f.read().split('\n'))

if not cnt:
  cnt = 0

#s = requests.session()



for i in lines[-2::-1]:
  if 1:
    #addr = '0x'+i.split(':')[2]

    key = '0x'+i.split(':')[0]
    addr = w3.toChecksumAddress('0x'+i.split(':')[2])

    with open('./giveEth_log2.txt','r') as f:
      archaddrs = f.read().split('\n')

    cflag = False
    for archaddr in archaddrs:
      if addr.lower().replace('0x','') in archaddr.lower():
        print('[+]{} doing... {}'.format(cnt, archaddr.split(':')[3]))
        cflag = True
        break
    if cflag:
      continue

    curbal = w3.fromWei(w3.eth.getBalance(addr),'ether')
    print('[{}] from curbal - {}'.format(cnt,curbal))


    if int(curbal)//1 < 5:
      for j in range(0,5-int(curbal)//1):
        #addr = '0x'+i.split(':')[2]
        r = requests.post(u, data=addr, headers=headers,  verify=False)
        if r.status_code==200:
          print('[+] now - {}'.format(curbal))
          print(r.content)
          curbal += 1#w3.fromWei(w3.eth.getBalance(addr),'ether')
        elif r.status_code==502:
          print('[x] 502')
        else:
          print('[?] {}'.format(r.status_code))
          if 'greedy' in r.content.decode():
            print(r.content)
            break
          if 'Too many' in r.content.decode():
            time.sleep(30)
          curbal = w3.fromWei(w3.eth.getBalance(addr),'ether')
          print('[+] now - {}'.format(curbal))
          print(u)
          print(addr)
          print(r.content.decode())
        time.sleep(2.5)
      cnt += 1
    else:
      cnt += 1
      print('[+]{} doing... {}'.format(cnt, curbal))
      with open('giveEth_log2.txt', 'a+') as f:
        f.write(i+':'+str(round(float(curbal),2))+'\n')



  with open('./giveEth_log2.txt','r') as f:
    cnt = len(f.read().split('\n'))

  print('[+] give money {} accounts'.format(cnt))
