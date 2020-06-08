#-*- coding: utf-8 -*-
from flask import Flask, render_template, request
from io import BytesIO
import subprocess
import pycurl
import re
from urllib import parse

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

# health check! - ps
@app.route('/he41th_ch3ck_C2_ps')
def health_ps():
	r = subprocess.Popen("ps -ef".split(' '),stdout=subprocess.PIPE).stdout.read().decode().split('\n')
	result = []
	for i in r:
		if 'python' in i:
			result.append(i)
	
	return render_template('he41th_ch3ck_C2_ps.html', results=result)

# health check! - netstat
@app.route('/h3alTh_CHeCK_c2_nEtsTaT')
def health_netstat():
	r = subprocess.Popen("netstat -lntp".split(' '),stdout=subprocess.PIPE).stdout.read().decode().split('\n')
	return render_template('h3alTh_CHeCK_c2_nEtsTaT.html', results=r)

# health check! - curl
@app.route('/He4ltH_chEck_c2_cur1')
def health_curl():
	url = request.args.get('url')
	try:
		if url:
			turl = filterUrl(url)
			if turl:
				url = turl
				try:
					buffer = BytesIO()
					c = pycurl.Curl()
					c.setopt(c.URL,url)
					c.setopt(c.SSL_VERIFYPEER, False)
					c.setopt(c.WRITEDATA,buffer)
					c.perform()
					c.close()
					try:
						result = buffer.getvalue().decode().split('\n')
					except:
						result = buffer.getvalue()
				except Exception as e:
					print('[x] curl err - {}'.format(str(e)))
					result = ['err.....']
				return render_template('He4ltH_chEck_c2_cur1.html', results=result)
			else:
				return render_template('He4ltH_chEck_c2_cur1.html', results=['nah.. url is error or unsafe!'])
	except Exception as e:
		print('[x] curl err2... - {}'.format(str(e)))
	return render_template('He4ltH_chEck_c2_cur1.html', results=['nah.. you didn\'t give url'])

def filterUrl(url):
	try:
		# you may not read any file
		if re.compile(r"(^[^:]{3}:)").search(url):
			if re.compile(r"(^[^:]{3}:/[^(.|/)]/[^(.|/)]/)").search(url):
				print('[+] curl url - {}'.format(url.replace("..","").encode('idna').decode().replace("..","")))
				return url.replace("..","").encode('idna').decode().replace("..","")
		elif re.compile(r"(^[^:]{4}://(localhost|172\.22\.0\.\d{1,3})((:\d{1,5})/|/))").search(url):
			p = parse.urlparse(url)
			if (p.scheme == 'http'):
				print('[+] curl url - {}'.format(url))
				return url
		elif re.compile(r"(^[^:]{6}://(localhost|172\.22\.0\.\d{1,3})((:\d{1,5})/|/))").search(url):
			print('[+] curl url - {}'.format(url))
			return url
	except Exception as e:
		print('[x] regex err - {}'.format(str(e)))
		return False

	return False


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=9090)
    except Exception as ex:
        print(ex)
