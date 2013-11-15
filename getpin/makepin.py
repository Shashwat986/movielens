import csv

dictzip = {}
# first three of pin : 

fp = open('canada.csv', 'rb')
#"A0A0A0","47.055640","-53.201979","Gander","NL"

ctr=0
for line in fp:
	ctr+=1
	if ctr%1000==0:
		print ctr
	k = line.split('","')
	k[0]=k[0][1:]		# Get rid of quotes around first value
	pin = k[0][:3]
	pin_rest = k[0][3:5]	# Truncates Canada postal codes, since dataset doesn't have more information
	lat = float(k[1])
	lng = float(k[2])
	if pin in dictzip.keys():
		dictzip["default"+pin] = [[lat,lng],1]		# stores a pin in the area as the default lat/long
		if pin_rest not in dictzip[pin].keys():
			dictzip[pin][pin_rest]=[[lat,lng],1]
		else:
			newlat = 1.0*((dictzip[pin][pin_rest][0][0]*dictzip[pin][pin_rest][1])+lat)/(dictzip[pin][pin_rest][1]+1)
			newlng = 1.0*((dictzip[pin][pin_rest][0][1]*dictzip[pin][pin_rest][1])+lng)/(dictzip[pin][pin_rest][1]+1)
			dictzip[pin][pin_rest][0]=[newlat,newlng]
			dictzip[pin][pin_rest][1]+=1
	else:
		dictzip[pin]={}
		dictzip[pin][pin_rest]=[[lat,lng],1]

fp.close()

fp = open('us.csv', 'rb')
#"00501","UNIQUE","Holtsville","","I R S Service Center","NY","Suffolk County","America/New_York","631","40.81","-73.04","NA","US","0","384",
fp.next()	# Get rid of header

ctr=0
for line in fp:
	ctr+=1
	if ctr%1000==0:
		print ctr
	k = line.split('","')
	k[0]=k[0][1:]		# Get rid of quotes around first value
	pin = k[0][:3]
	pin_rest = k[0][3:5]
	lat = float(k[9])
	lng = float(k[10])
	if pin in dictzip.keys():
		dictzip["default"+pin] = [[lat,lng],1]		# stores a pin in the area as the default lat/long
		if pin_rest not in dictzip[pin].keys():
			dictzip[pin][pin_rest]=[[lat,lng],1]
		else:
			newlat = 1.0*((dictzip[pin][pin_rest][0][0]*dictzip[pin][pin_rest][1])+lat)/(dictzip[pin][pin_rest][1]+1)
			newlng = 1.0*((dictzip[pin][pin_rest][0][1]*dictzip[pin][pin_rest][1])+lng)/(dictzip[pin][pin_rest][1]+1)
			dictzip[pin][pin_rest][0]=[newlat,newlng]
			dictzip[pin][pin_rest][1]+=1
	else:
		dictzip[pin]={}
		dictzip[pin][pin_rest]=[[lat,lng],1]

fp.close()

import json

with open('dictzip.json', 'w') as f:
    json.dump(dictzip, f)