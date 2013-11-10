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

from scipy.cluster.vq import kmeans, kmeans2, vq
import numpy as np

user_d = dopen('ml-100k/u.user','|')
data_t = topen('ml-100k/u.data')

profs=set([])
profl=[]

for k in user_d.keys():
	user_d[k].append(0)		# Number of ratings
	user_d[k].append(0)		# Sum of ratings
	user_d[k][1] = 0 if user_d[k][1] == 'M' else 1
	if user_d[k][2] in profs:
		user_d[k][2] = profl.index(user_d[k][2])
	else:
		profs.add(user_d[k][2])
		profl.append(user_d[k][2])
		user_d[k][2] = profl.index(user_d[k][2])
	

for k, _, r, _ in data_t:
	user_d[k][-2]+=1
	user_d[k][-1]+=r

for k in user_d.keys():
	user_d[k][-1]=user_d[k][-1]*1.0/user_d[k][-2]

for i in user_d.keys()[0:10]:
	print user_d[i]

arr=[]
for i in user_d.keys():
	arr.append(user_d[i])

print 1.0*sum([k[-1] for k in arr])/len(arr)
print 1.0*sum([k[-2] for k in arr])/len(arr)

'''
arr=np.array(arr)
numcl=5

centroid, _ = kmeans(arr,numcl)
idxF, ds = vq(arr,centroid)
'''