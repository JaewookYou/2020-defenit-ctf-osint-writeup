#-*- coding: utf-8 -*-

from flask import Flask, render_template, request
import pymysql
import os
import subprocess

app = Flask(__name__)


def connect_db():
	db = pymysql.connect(
		user='b4d_aR4n9',
		#passwd=os.environ['DBPW'],
		host='172.22.0.4',
                port=3306,
		db='defenit_ctf_2020',
		charset='utf8'
	)

	return db

db = connect_db()

@app.route('/')
def index():
	try:
		if request.remote_addr != '172.22.0.3' and request.remote_addr != '127.0.0.1':
			return '[INTERNAL] localhost only..'

		return render_template('index.html')
	except:
		return '[x] errr.....'


# if input killcode, kill all ransomware
@app.route('/k1ll_r4ns0mw4r3')
def kill_ransom():
	try:
		if request.remote_addr != '172.22.0.3' and request.remote_addr != '127.0.0.1':
			return '[INTERNAL] localhost only..'

		cursor = db.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT ki11c0d3 from secret;")

		if cursor.fetchall()[0]['ki11c0d3'] == request.args.get('ki11c0d3'):
			return subprocess.Popen("/app2/getFlag", stdout=subprocess.PIPE).stdout.read().strip()
		else:
			return '[x] you put wrong killcode!'

	except:
		return '[x] errr.....'

if __name__=="__main__":
	app.run(host='0.0.0.0', port=7777)
