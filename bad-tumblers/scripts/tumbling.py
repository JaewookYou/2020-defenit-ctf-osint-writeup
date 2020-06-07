#-*- coding: utf-8 -*-
import os
os.environ['WEB3_INFURA_PROJECT_ID']='[redacted]'
import random
import time
from web3.auto.infura.ropsten import w3


with open('usefulWallets.txt','r') as f:
	addrs = f.read().split('\n')

sended_bal = 0

# step1 is spreading hacker's address' ether to tumbling address
def step1():
	global sended_bal
	global addrs

	cnt = 0
	key = '[hacker secret key]'.lower()
	fromaddr = w3.toChecksumAddress('0x4c5E179bBc6D393AffB72018f9bba4b3Cee6dE65'.lower())
	curbal = float(w3.fromWei(w3.eth.getBalance(fromaddr),'ether'))
	while 1:
		try:
			if curbal < 5:
				print('--------------***--------------')
				print('[!] spread complete')
				print('[+] doing next step...')
				break

			print('--------------***--------------')
			toaddr = w3.toChecksumAddress(addrs[random.randint(0,len(addrs)-1)].split(':')[2])
			print('[{}] toaddr - {}'.format(cnt,toaddr))
			sendbal = random.uniform(20,80) * 0.01 * 5
			print('[+] sendbal - {}'.format(str(sendbal)))
			print('[+] [before] hacker bal - {}'.format(str(curbal)))

			transaction = {
				'from':fromaddr,
				'to':toaddr, 
				'value':w3.toWei(sendbal,'ether'), 
				'gasPrice':w3.eth.gasPrice, 
				'gas':100000,
				'nonce':w3.toHex(w3.eth.getTransactionCount(fromaddr,"pending"))
			}

			signed = w3.eth.account.sign_transaction(transaction, key)
			w3.eth.sendRawTransaction(signed.rawTransaction)
			sended_bal += sendbal
			curbal = curbal - sendbal
			cnt += 1
			print('[+] sended bal - {}'.format(sended_bal))
			print('[+] cur bal - {}'.format(curbal))
			print('-------------------------------')

		except Exception as e:
			print('[x] err.. {}'.format(str(e)))
		except KeyboardInterrupt:
			print("W: Ctrl-C received, stopping…")
			exit(1)

		time.sleep(1)

	print('[!] sended bal\'s sum is {}'.format(str(sended_bal)))

# print('[+] step 1 start!')
# step1()


tumbled_bal = 0
sended_bal = 455
# step2 is collecting spreaded tumbling address' to hacker's withdraw address at 'B exchanging site'
def step2():
	global tumbled_bal
	toaddr = w3.toChecksumAddress('0x2Fd3F2701ad9654c1Dd15EE16C5dB29eBBc80Ddf'.lower())
	curbal = float(w3.fromWei(w3.eth.getBalance(toaddr),'ether'))
	gas = 100000
	while 1:
		try:
			if tumbled_bal > sended_bal:
				print('[!] tumbling is completed')
				print('----------------------------')
				break
			print('--------------***--------------')
			addr = addrs[random.randint(0,len(addrs)-1)]
			key = '0x'+addr.split(':')[0]
			print('[+] fromaddr - {}'.format('0x'+addr.split(':')[2]))
			fromaddr = w3.toChecksumAddress('0x'+addr.split(':')[2])
			curbal = w3.fromWei(w3.eth.getBalance(fromaddr),'ether')
			sendbal = round(float(curbal) * random.uniform(20,80) * 0.01,1)

			curbal2 = w3.fromWei(w3.eth.getBalance(toaddr),'ether')
			
			print('[+] [before] from curbal - {}'.format(curbal))
			print('[+] [before] to curbal - {}'.format(curbal2))
			print('[+] send bal - {}'.format(sendbal))

			transaction = {
				'from':fromaddr,
				'to':toaddr, 
				'value':w3.toWei(sendbal,'ether'), 
				'gasPrice':w3.eth.gasPrice, 
				'gas':gas,
				'nonce':w3.toHex(w3.eth.getTransactionCount(fromaddr,"pending"))
			}

			signed = w3.eth.account.sign_transaction(transaction, key)
			w3.eth.sendRawTransaction(signed.rawTransaction)


			tumbled_bal += sendbal

			print('[+] [after] from curbal - {}'.format(str(round(float(curbal),2)-round(float(sendbal),2))))
			print('[+] [after] to curbal - {}'.format(str(round(float(curbal2),2)+round(float(sendbal),2))))
			print('-------------------------------')

		except Exception as e:
			print('[x] err.. {}'.format(str(e)))
		except KeyboardInterrupt:
			print("W: Ctrl-C received, stopping…")
			exit(1)

print('[+] step 2 start!')
step2()
