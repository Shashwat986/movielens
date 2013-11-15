import csv

dictzip = {}
# first three of pin : 

fp = open('us.csv')
#A0A0A0,47.055640,-53.201979,Gander,NL
fp.next()

ctr=0
for line in fp:
	ctr+=1
	k = line.split('","')
	k[0]=k[0][1:]		# Get rid of quotes around first value
	pin = k[0][:3]
	pin_rest = k[0][3:5]	# Truncates Canada postal codes, since dataset doesn't have more information
	lat = float(k[9])
	lng = float(k[10])
	print pin, pin_rest, lat, lng
	#print k
	if ctr>20:
		break