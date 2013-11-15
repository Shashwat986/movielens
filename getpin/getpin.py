import json
from math import sqrt

with open('dictzip.json') as f:
	dictzip = json.load(f)

def pindist(pin1,pin2):
	if type(pin1)==int:
		pin1 = "%05d"%pin1
	if type(pin2)==int:
		pin2 = "%05d"%pin2
	
	lat1 = dictzip[pin1[:3]].get(pin1[3:5],dictzip["default"+pin1[:3]])[0][0]
	lng1 = dictzip[pin1[:3]].get(pin1[3:5],dictzip["default"+pin1[:3]])[0][1]
	lat2 = dictzip[pin2[:3]].get(pin2[3:5],dictzip["default"+pin2[:3]])[0][0]
	lng2 = dictzip[pin2[:3]].get(pin2[3:5],dictzip["default"+pin2[:3]])[0][1]
	return sqrt((lat2-lat1)*(lat2-lat1) + (lng2-lng1)*(lng2-lng1))/110.0	# 110.0 is roughly the distance between alaska and hawaii in lat/long units

print pindist(70808,15610)