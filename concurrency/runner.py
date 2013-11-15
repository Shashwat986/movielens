import os
import sys
from StringIO import StringIO

try:
	while 1:
		if os.stat('input.txt').st_size > 1:
			print "Yay!"
			fp = open('input.txt','r')
			line = fp.readline()
			fp.close()
			buffer = StringIO()
			sys.stdout = buffer
			exec(line)
			sys.stdout=sys.__stdout__
			fp = open('input.txt','w')
			fp.close()
			
			fp = open('output.txt','w')
			fp.write(buffer.getvalue())
			fp.close()
except KeyboardInterrupt:
	exit(0)