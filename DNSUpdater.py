import socket
import sys 

IP = sys.argv[1]
PORT = 4701
BUFFER_SIZE = 1024

if len(sys.argv) < 3 or len(sys.argv) > 5:
	print 'Wrong Number of Arguments'
	sys.exit()

if( IP == 'localhost'):
	IP = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

#LOOKUP 
if len(sys.argv) == 3:
	site = sys.argv[2]
	s.sendto(site, (IP, PORT))
	data = s.recv(BUFFER_SIZE)
	print "DNSLookup: " + site + " is " + data
	s.close()

# DELETE
if len(sys.argv) == 4:
	command = sys.argv[2]
	site = sys.argv[3]
	send = command + " " + site
	s.sendto(send, (IP, PORT))

	# AUTH ----------------------------------------------
	okay = 0
	while okay == 0:
		ver = s.recv(BUFFER_SIZE)
		if ver == 'OK':
			print "DNSUpdater: Code accepted"
			okay = 1
			break
		elif ver == 'FAIL': 
			print "DNSUpdater: Authentication Failed"
			break
		innit = raw_input("DNSResolver is requesting authentication code: ")
		type(innit)
		s.sendto(innit, (IP, PORT))

	# ----------------------------------------------------
	if okay == 1:
		data = s.recv(BUFFER_SIZE)
		if data == 'YES':
			print "DNSLookup: Successfully removed " + site
		else:
			print "DNSLookup: No such host to delete - " + site
		s.close()

# ADD OR UPDATE 
if len(sys.argv) == 5:
	command = sys.argv[2]
	site = sys.argv[3]
	addr = sys.argv[4]
	send = command + " " + site + " " + addr
	s.sendto(send, (IP, PORT))

	# AUTH ----------------------------------------------
	okay = 0
	while okay == 0:
		ver = s.recv(BUFFER_SIZE)
		if ver == 'OK':
			print "DNSUpdater: Code accepted"
			okay = 1
			break
		elif ver == 'FAIL': 
			print "DNSUpdater: Authentication Failed"
			break
		innit = raw_input("DNSResolver is requesting authentication code: ")
		type(innit)
		s.sendto(innit, (IP, PORT))

	# ----------------------------------------------------

	if command == 'add' and okay == 1:
		data = s.recv(BUFFER_SIZE)
		if data == 'YES':
			print "DNSLookup: Successfully added " + site + " " + addr
		else:
			print "DNSLookup: Failure to add " + site + " " + addr
	elif command == 'update' and okay == 1:
		data = s.recv(BUFFER_SIZE)
		if data == 'YES':
			print "DNSLookup: Successfully updated " + site + " " + addr
		else:
			print "DNSLookup: Failure to update " + site + " " + addr






