#-*- coding: utf-8 -*-
import os
os.environ['WEB3_INFURA_PROJECT_ID']='[redacted]'
import random
from web3.auto.infura.ropsten import w3


with open('usefulWallets.txt','r') as f:
	lines = f.read().split('\n')

while 1:
	try:
		print('--------------***--------------')
		line = lines[random.randint(0,len(lines)-1)]
		key = '0x'+line.split(':')[0]
		print('[+] fromaddr - {}'.format('0x'+line.split(':')[2]))
		fromaddr = w3.toChecksumAddress('0x'+line.split(':')[2])
		curbal = w3.fromWei(w3.eth.getBalance(fromaddr),'ether')
		sendbal = round(float(curbal) * random.uniform(20,80) * 0.01,1)

		line2 = lines[random.randint(0,len(lines)-1)]
		print('[+] toaddr - {}'.format('0x'+line2.split(':')[2]))
		toaddr = w3.toChecksumAddress('0x'+line2.split(':')[2])
		curbal2 = w3.fromWei(w3.eth.getBalance(toaddr),'ether')
		
		print('[+] [before] from curbal - {}'.format(curbal))
		print('[+] [before] to curbal - {}'.format(curbal2))
		print('[+] send bal - {}'.format(sendbal))

		transaction = {
			'from':fromaddr,
			'to':toaddr, 
			'value':w3.toWei(sendbal,'ether'), 
			'gasPrice':w3.eth.gasPrice, 
			'gas':100000,
			'nonce':w3.eth.getTransactionCount(fromaddr)
		}

		signed = w3.eth.account.sign_transaction(transaction, key)
		w3.eth.sendRawTransaction(signed.rawTransaction)

		print('[+] [after] from curbal - {}'.format(str(round(float(curbal),2)-round(float(sendbal),2))))
		print('[+] [after] to curbal - {}'.format(str(round(float(curbal2),2)+round(float(sendbal),2))))
		print('-------------------------------')
	except Exception as e:
		print('[x] err.. {}'.format(str(e)))
	except KeyboardInterrupt:
		print("W: Ctrl-C received, stopping…")
		exit(1)
