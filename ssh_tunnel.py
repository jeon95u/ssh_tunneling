import redis, json
import subprocess
import time, sys

conn = redis.StrictRedis(host="127.0.0.1", port=6379)

data = {}
p = subprocess.Popen([sys.executable, '-c', 'print "Hello";'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

while True:
	if data != json.loads(conn.get('ssh-tunnel')) or p.poll() is not None:
		
		if p.poll() is None:
			p.terminate()
		else:
			stdout, stderr = p.communicate()
			print stdout

		print "[+] new Process"

		data = json.loads(conn.get('ssh-tunnel'))
		tmp = ""
		for i in data:
			tmp += " -R 0.0.0.0:%s:%s:%s" % (i, data[i]['in_i'], data[i]['in_p'])
		
		cmd = str("""ssh -N -i /Users/jeon95u/Documents/jeon95u_seoul.pem root@aws.ko.jeong.su""" + tmp + """ -o ExitOnForwardFailure=yes -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=no""").split()
		
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	
	time.sleep(1)

