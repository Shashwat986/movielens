fp = open('u.user')

users={}
for line in fp:
	k=line.split('|')
	users[k[0]]=[kk.strip() for kk in k[1:]]

fp.close()

fp = open('u.item')

movies={}
for line in fp:
	k=line.split('|')
	movies[k[0]]=[k[2].split('-')[-1].strip()] + [kk.strip() for kk in k[5:]]

fp.close()

useravg={}
for u in users.keys():
	useravg[u]=[0,0]

write=[]
fp = open('u.data')
lines = fp.readlines()
fp.close()

for line in lines:
	k=line.split('\t')
	useravg[k[0]][1]+=1
	useravg[k[0]][0]+=int(k[2])

for u in useravg.keys():
	useravg[u] = useravg[u][0]*1.0/useravg[u][1]

for line in lines:
	k=line.split('\t')
	temp=[]
	temp+=users[k[0]]
	temp+=movies[k[1]]
	temp.append("0" if int(k[2])<int(useravg[k[0]]) else "1")
	write.append(",".join(temp)+"\n")

fp = open('dataNew.txt','w')
fp.writelines(write)
fp.close()