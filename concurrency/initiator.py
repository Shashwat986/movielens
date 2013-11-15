import os
import time

fp = open('input.txt','w')
a=raw_input()
fp.write(a)
fp.close()
while os.stat('output.txt').st_size < 1:
	time.sleep(1)
fp = open('output.txt')
lines = fp.readlines()
print lines
fp.close()
