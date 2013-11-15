#from scipy.cluster.vq import kmeans, kmeans2, vq
#import numpy as np

def topen(fname, spl = '\t'):
	fp = open(fname)
	val=[]
	for l in fp:
		val.append([])
		k=l.split(spl)
		for elem in k:
			try:
				if float(elem)==int(elem):
					val[-1].append(int(elem))
				else:
					val[-1].append(float(elem))
			except:
				val[-1].append(elem.strip())
	return val

def dopen(fname, spl = '\t'):
	fp = open(fname)
	val={}
	for l in fp:
		k=l.split(spl)
		p = int(k[0])
		val[p]=[]
		for elem in k[1:]:
			try:
				if float(elem)==int(elem):
					val[p].append(int(elem))
				else:
					val[p].append(float(elem))
			except:
				val[p].append(elem.strip())
	return val

user_d = dopen('ml-100k/u.user','|')
data_t = topen('ml-100k/u.data')

profs = {
	'administrator':0,
	'executive':1,
	'lawyer':2,
	'entertainment':3,
	'marketing':4,
	'salesman':5,
	'technician':6,
	'artist':7,
	'writer':8,
	'librarian':9,
	'educator':10,
	'doctor':11,
	'engineer':12,
	'scientist':13,
	'programmer':14,
	'healthcare':15,
	'homemaker':16,
	'retired':17,
	'student':18,
	'none':19,
	'other':20
}

for k in user_d.keys():
	user_d[k].append(0)		# Number of ratings
	user_d[k].append(0)		# Sum of ratings
	user_d[k][0]/=100.0
	user_d[k][1] = 0 if user_d[k][1] == 'M' else 1
	user_d[k][2] = profs[user_d[k][2]]/20.0
	try:
		user_d[k][3]/=125000.0			# If US Pin Code, normalize to 0-0.8
	except:
		user_d[k][3]=1.0				# If Canada Pin Code, set to 1.0

for k, _, r, _ in data_t:
	user_d[k][-2]+=1
	user_d[k][-1]+=r

for k in user_d.keys():
	user_d[k][-1]=user_d[k][-1]*1.0/user_d[k][-2]

def run(age, sex, job, zip):
	