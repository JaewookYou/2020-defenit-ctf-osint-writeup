#-*- coding: utf-8 -*-
import requests
import time
import json
import os
os.environ['WEB3_INFURA_PROJECT_ID']='[redatcted]'
import random
from web3.auto.infura.ropsten import w3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

init_addr = '0x5149Aa7Ef0d343e785663a87cC16b7e38F7029b2'

u = 'http://api-ropsten.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&sort=asc&apikey=[redacted]'

headers = {
'User-Agent': 'PostmanRuntime/7.17.1',
'Accept': '/',
'Cache-Control': 'no-cache',
'Postman-Token': '267dd7be-7f3f-4d67-a51c-05152aa8e8fc,8f8b84b0-3df1-4656-9480-c31e99d270d2',
'Host': 'ropsten.etherscan.io 4',
'Accept-Encoding': 'gzip, deflate',
'Cookie': '__cfduid=d33064099a72a08ae6f9197c790da62d21569724532',
'Connection': 'keep-alive',
'cache-control': 'no-cache'
}

cnt = 0

alladdr = []
resultaddr = []
fromtocnt = {}

def recursiveSearch(addr):
    global alladdr
    global resultaddr
    global cnt
    global fromtocnt

    try:
        cnt += 1
        r = requests.get(u.format(addr), headers=headers, verify=False)
        data = json.loads(r.content)
        txs = data['result']
        fromtocnt[addr]={'from':{'addr':[],'cnt':0},'to':{'addr':[],'cnt':0},'balance':0,'useful_balance':False,'maximum_balance':0}
        for tx in txs:
            if tx['from'] and tx['to']:
                if fromtocnt[addr]['balance'] > fromtocnt[addr]['maximum_balance']:
                    fromtocnt[addr]['maximum_balance'] = fromtocnt[addr]['balance']

                alladdr.append(tx['from'])
                alladdr.append(tx['to'])
                if tx['from'] == addr:
                    fromtocnt[addr]['to']['addr'].append(tx['to'])
                    fromtocnt[addr]['to']['cnt'] += 1
                    fromtocnt[addr]['balance'] -= float(w3.fromWei(int(tx['value']),'ether'))
                elif tx['to'] == addr:
                    fromtocnt[addr]['from']['addr'].append(tx['from'])
                    fromtocnt[addr]['from']['cnt'] += 1
                    fromtocnt[addr]['balance'] += float(w3.fromWei(int(tx['value']),'ether'))
                else:
                    print(addr)
        
        if fromtocnt[addr]['maximum_balance'] > 400:
            fromtocnt[addr]['useful_balance'] = True

        fromtocnt[addr]['to']['addr'] = list(set(fromtocnt[addr]['to']['addr']))
        fromtocnt[addr]['from']['addr'] = list(set(fromtocnt[addr]['from']['addr']))
        
        alladdr = list(set(alladdr))
        # 0x81b7e08f65bdf5648606c89998a9cc8164397647 is faucet addr. ignore it
        if alladdr.count('0x81b7e08f65bdf5648606c89998a9cc8164397647') > 0:
            alladdr.remove("0x81b7e08f65bdf5648606c89998a9cc8164397647")

        print('[{}] len {}'.format(cnt, len(alladdr)))
        with open('parse_addr.txt','w') as f:
            f.write('\n'.join(alladdr))

        for i in alladdr:
            if resultaddr.count(i) == 0 and i != '0x81b7e08f65bdf5648606c89998a9cc8164397647':
                resultaddr.append(i)
                recursiveSearch(i.lower())
            

    except Exception as e:
        print('[x] err.. {}'.format(str(e)))


recursiveSearch(init_addr.lower())
for key,value in fromtocnt.items():
    if fromtocnt[key]['to']['cnt'] < 5:
        print('[+] addr {}, from : {} - {}, to : {} - {}'.format(key, fromtocnt[key]['from']['cnt'], len(fromtocnt[key]['from']['addr']), fromtocnt[key]['to']['cnt'], len(fromtocnt[key]['to']['addr'])))
        #print(fromtocnt[key])
    if fromtocnt[key]['useful_balance']:
        print('[+] over 400 balance')
        print('[+] {} - {}'.format(key, fromtocnt[key]['maximum_balance']))

with open('parse_result.txt', 'w') as f:
    f.write(json.dumps(fromtocnt))
