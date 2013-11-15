#!/bin/python
import re, numpy, math
import numpy as np
from math import sqrt as root2
from prediction import RMSE, MAE
from factorize import SVD
from data import Data
from sklearn import linear_model as lm
import getpin	#!! New line

movies_list=[];
users_list=[];

def memo(f):
    "Memoize function f."
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo

class User:
	def __init__(self, id,ag,gen,occ,zip):
		self.user_id=id;
		self.age=ag;
		self.gender=gen;
		self.occupation=occ;
		self.zipcode=zip;
		self.ratings={};

class Movie:
	def __init__(self,id,tit,rdate,vrdate,url,genre_list):
		self.item_id=id;
		self.title=tit;
		self.r_date=rdate;
		self.vr_date=vrdate;
		self.IMDb_URl=url;
		self.genre_list=genre_list;
		#			unknown | Action | Adventure | Animation |
	    #          Children's | Comedy | Crime | Documentary | Drama | Fantasy |
	    #         Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
	    #          Thriller | War | Western 


#	Read movie data from file
def read_item_file(file='u.item'):
	with open(file) as u_item:
		for line_ in u_item:
			line_=line_[:-1];
			item_id=line_.split('|')[0];
			title=line_.split('|')[1];
			release=line_.split('|')[2];
			vrelease=line_.split('|')[3];
			url=line_.split('|')[4];
			genre_list=line_.split('|')[5:];
			movies_list.append(Movie(int(item_id),title,release,vrelease,url,map(int,genre_list)));

read_item_file();

#	Read User Info from file
def read_user_file(file='u.user'):
	with open(file) as u_user:
		for line_ in u_user:
			line_=line_[:-1];
			id=line_.split('|')[0];
			ag=line_.split('|')[1];
			gen=line_.split('|')[2];
			occ=line_.split('|')[3];
			zip=line_.split('|')[4];
			#zip=re.sub('[A-Za-z]','0',zip);
			users_list.append(User(int(id),int(ag),gen,occ,zip));

read_user_file();

def read_data_file(file='u.data'):
	with open(file) as datafile:
			for line in datafile:
				[u,mov_id,rat,tstamp]=line.split('\t');
				users_list[int(u)-1].ratings[int(mov_id)]=int(rat);


read_data_file();
data=Data();
data.load('u.data', sep='\t', format={'col':0, 'row':1, 'value':2, 'ids':int})
svd = SVD();
svd.set_data(data)

def recompute_svd():
	svd.set_data(data)
     		
#computing data for Normalization
max_age=0;
min_age=100;
#max_zip=0;
#min_zip=1000000;
avg_age=0;
avg_rating_global=0;
rating_ctr=0;
for user in users_list:
	#max_zip=max(max_zip,user.zipcode);		#!! New line
	max_age=max(max_age,user.age);
	#min_zip=min(min_zip,user.zipcode);		#!! New line
	min_age=min(min_age,user.age);
	avg_age+=user.age;
	for movie_id in user.ratings:
		avg_rating_global+=user.ratings[movie_id];
		rating_ctr+=1;
avg_rating_global=float(avg_rating_global)/rating_ctr;
#calculating std dev
var=0;
for user in users_list:
	for movie_id in user.ratings:
		var+=(user.ratings[movie_id]-avg_rating_global)**2
std_dev_rating_global=root2(float(var)/rating_ctr);
avg_age=avg_age/len(users_list);

#	Normalization Functions
def normalize_age(age):
	return float(age-min_age)/(max_age-min_age);

#!! New line
'''def normalize_zip(zip):
	return float(zip-min_zip)/(max_zip-min_zip);
'''


#print max_age,max_zip,min_zip,min_age,avg_age;

# dictionaries to map gender, occs, genre to numbers
# TODO: (Re)arrange occupations in an order of similarity, so as to get a better estimate of their similarity on the basis of their occcupations
genders={'M':1, 'F':0}

#!! New line
#occupations={'administrator':0,'artist':6,'doctor':2,'educator':3,'engineer':4,'entertainment':5,'executive':1,'healthcare':7,'homemaker':8,'lawyer':9,'librarian':10,'marketing':11,'none':12,'other':13,'programmer':14,'retired':15,'salesman':16,'scientist':17,'student':18,'technician':19,'writer':20}
#!! New line
occupations = {
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
genres={}
with open('u.genre') as u_genres:
        	for line_ in u_genres:
        		line_=line_[:-1];
        		genres[int(line_.split('|')[1])]=line_.split('|')[0];      		

#	Eucledian Distance only using Demographic features
def user_euclidean_dist_demographic(user1,user2):
	user1_vec=[];
	user2_vec=[];
	user1_vec.append(normalize_age(user1.age));
	user2_vec.append(normalize_age(user2.age));
	#user1_vec.append(normalize_zip(user1.zipcode));		#!! New line
	#user2_vec.append(normalize_zip(user2.zipcode));
	user1_vec.append(genders[user1.gender]);
	user2_vec.append(genders[user2.gender]);
	user1_vec.append(occupations[user1.occupation]/20.0);
	user2_vec.append(occupations[user2.occupation]/20.0);
	#print user1_vec,user2_vec;
	ans = numpy.array(user1_vec)-numpy.array(user2_vec)			#!! New line
	numpy.append(ans,getpin.pindist(user1.zipcode,user2.zipcode))
	return numpy.linalg.norm(ans);

# Prints k-nearest neighbours using the the similarity metric (function is passed as an arg) in the arguments

@memo
def k_NN(user,k=20, dist_metric=user_euclidean_dist_demographic):
	dist_list=[dist_metric(user,user_i) for user_i in users_list];
	#print "Top",k," Users closest to User ",user.user_id,": ",[(users_list[i].user_id,users_list[i].age,users_list[i].occupation,users_list[i].gender,users_list[i].zipcode) for i in sorted(range(len(dist_list)), key=lambda i: dist_list[i])[:k]];
	nns=[users_list[i] for i in sorted(range(len(dist_list)), key=lambda i: dist_list[i])[:k]];
	try:
		nns.remove(user);
		return nns
	except:
		return nns;


#	predict the rating, avged using weights=similarity
def predict_rating_knn(user_id,movie_id,k=20,dist_metric=user_euclidean_dist_demographic):
	user=users_list[user_id-1];
	movie=movies_list[movie_id-1];
	nns=k_NN(user,k);
	avg_rating=0;
	ctr=0;
	sum_of_inv_dists=0;
	for n_users in nns:
		if movie_id in n_users.ratings:
			avg_rating+=float(n_users.ratings[movie_id]);
			ctr+=1;
			#sum_of_inv_dists+=float(1/dist);
	if ctr!=0:
		avg_rating=float(avg_rating)/ctr;
	else:
		avg_rating=avg_rating_global- std_dev_rating_global
	#print ctr, sum_of_dists;
	return avg_rating;


#k_NN(users_list[1],5);



##print users_list[195].ratings;
#print predict_rating(195,258)

#for i in range(0,10):
#	print user_euclidean_dist_demographic(users_list[9],users_list[i]);

# user_movie_matrix=[[0 for _ in range(len(movies_list))] for _ in range(len(users_list))];
# for user in users_list:
# 	for key in user.ratings:
# 		user_movie_matrix[user.user_id-1][key-1]=user.ratings[key];

#print user_movie_matrix[195];

#u,s,v=np.linalg.svd(np.array(user_movie_matrix));


