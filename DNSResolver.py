import socket
import csv
import sys


IP = ''
PORT = 4701
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(1)

my_dict = {}
with open('dnsentries.csv', 'r') as csvfile:
			reader = csv.reader(csvfile)
			for rows in reader:
				k = rows[0]
				v = rows[1]
				my_dict[k] = v



while True:
	print "DNSResolver: waiting for request..."
	conn, addr = s.accept()


	data = conn.recv(BUFFER_SIZE)
	d = data.split(" ") # Splits incomming string arguments 

	if d[0] == 'add' or d[0]=='update' or d[0]=='delete':
		count = 0
		fail = 0
		green = 0
		p = 'AUTH'
		conn.send(p)
		while fail == 0 or green == 0:
			v = conn.recv(BUFFER_SIZE)
			if v == '12345':
				green = 1 
				break
			else:
				if count == 2:
					fail = 1
					break
			count = count + 1
			conn.send(p)

		if fail == 1:
			f = 'FAIL'
			conn.send(f)
		elif green == 1:
			g = 'OK'
			conn.send(g)

	if fail == 1:
		break
		
	if d[0] == 'add':
		do = 0
		y = 'YES'
		n = 'NO' 
		print "DNSResolver: \"add\" request recieved "
		for rows in my_dict:
			k = rows
			if k == d[1]:
				do = 1
				break
		# if its not already in add it 
		if do == 0:
			k = d[1]
			v = d[2]
			my_dict[k] = v
			print "DNSResolver: added " + k + " as " + v + ": sending success response"
			conn.send(y)  # echo
		else: 
			print "DNSResolver: could not add " + k + " as" + v + ": sending failure response"
			conn.send(n)


	elif d[0] == 'update':
		print "DNSResolver: \"update\" request recieved "
		do = 0
		y = 'YES'
		n = 'NO' 
		for rows in my_dict:
			k = rows
			if k == d[1]:
				do = 1
				v = d[2]
				my_dict[k] = v
				break
		# if its not already in add it 
		if do == 1:
			print "DNSResolver: updated " + k + " as " + v + ": sending success response"
			conn.send(y)  # echo
		else: 
			print "DNSResolver: could not update " + d[1] + " as " + d[2] + ": sending failure response"
			conn.send(n)



	elif d[0] == 'delete':
		print "DNSResolver: \"delete\" request recieved "
		found = 0
		for rows in my_dict:
			k = rows
			if k == d[1]:
				del my_dict[k]
				found = 1
				break
		if found == 0:
			n = "NO"
			print "DNSResolver: Could not delete " + d[1] + ": sending failure response"
			conn.send(n)
		else:
			y = "YES"
			print "DNSResolver: deleted " + d[1] + ": sending success response"
			conn.send(y)  # echo
	

	else:
		r = 'null'
		print "DNSResolver: Request recieved - ", data
		if not data: break
		with open('dnsentries.csv', 'r') as csvfile:
			reader = csv.reader(csvfile)
			for rows in reader:
				k = rows[0]
				v = rows[1]
				if k == data:
					r = v
		print "DNSResolver: Responding with - ", r
		conn.send(r)  # echo
		close(csvfile)

conn.close()
