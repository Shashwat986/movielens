#!/bin/python
import re, numpy
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
		self.item_id=0;
		self.title=tit;
		self.r_date=rdate;
		self.vr_date=vrdate;
		self.IMDb_URl=url;
		self.genre=genre_list;
		#			unknown | Action | Adventure | Animation |
	    #          Children's | Comedy | Crime | Documentary | Drama | Fantasy |
	    #         Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
	    #          Thriller | War | Western 

movies_list=[];
#	Read movie data from file
with open('u.item') as u_item:
        	for line_ in u_item:
        		line_=line_[:-1];
        		item_id=line_.split('|')[0];
        		title=line_.split('|')[1];
        		release=line_.split('|')[2];
        		vrelease=line_.split('|')[3];
        		url=line_.split('|')[4];
        		genre_list=line_.split('|')[5:];
        		movies_list.append(Movie(item_id,title,release,vrelease,url,map(int,genre_list)));


users_list=[];
#	Read User Info from file
with open('u.user') as u_user:
        	for line_ in u_user:
        		line_=line_[:-1];
        		id=line_.split('|')[0];
        		ag=line_.split('|')[1];
        		gen=line_.split('|')[2];
        		occ=line_.split('|')[3];
        		zip=line_.split('|')[4];
        		zip=re.sub('[A-Za-z]','0',zip);
        		users_list.append(User(int(id),int(ag),gen,occ,int(zip)));

#computing data for Normalization
max_age=0;
min_age=100;
max_zip=0;
min_zip=1000000;
avg_age=0;
for user in users_list:
	max_zip=max(max_zip,user.zipcode);
	max_age=max(max_age,user.age);
	min_zip=min(min_zip,user.zipcode);
	min_age=min(min_age,user.age);
	avg_age+=user.age;
avg_age=avg_age/len(users_list);

#	Normalization Functions
def normalize_age(age):
	return float(age-min_age)/(max_age-min_age);

def normalize_zip(zip):
	return float(zip-min_zip)/(max_zip-min_zip);



#print max_age,max_zip,min_zip,min_age,avg_age;

# dictionaries to map gender, occs, genre to numbers
# TODO: (Re)arrange occupations in an order of similarity, so as to get a better estimate of their similarity on the basis of their occcupations
genders={'M':1, 'F':0}
occupations={'administrator':0,'artist':6,'doctor':2,'educator':3,'engineer':4,'entertainment':5,'executive':1,'healthcare':7,'homemaker':8,'lawyer':9,'librarian':10,'marketing':11,'none':12,'other':13,'programmer':14,'retired':15,'salesman':16,'scientist':17,'student':18,'technician':19,'writer':20}
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
	user1_vec.append(normalize_zip(user1.zipcode));
	user2_vec.append(normalize_zip(user2.zipcode));
	user1_vec.append(genders[user1.gender]);
	user2_vec.append(genders[user2.gender]);
	user1_vec.append(occupations[user1.occupation]/20.0);
	user2_vec.append(occupations[user2.occupation]/20.0);
	#print user1_vec,user2_vec;
	return numpy.linalg.norm(numpy.array(user1_vec)-numpy.array(user2_vec));

# Prints k-nearest neighbours using the the similarity metric (function is passed as an arg) in the arguments

def k_NN(user,k, dist_metric=user_euclidean_dist_demographic):
	dist_list=[dist_metric(user,user_i) for user_i in users_list];
	print "Top",k," Users closest to User ",user.user_id,": ",[(users_list[i].user_id,users_list[i].age,users_list[i].occupation,users_list[i].gender,users_list[i].zipcode) for i in sorted(range(len(dist_list)), key=lambda i: dist_list[i])[:k]];
	return [users_list[i] for i in sorted(range(len(dist_list)), key=lambda i: dist_list[i])[:k]];

#	predict the rating, avged using weights=similarity
def predict_rating(user_id,movie_id,k=10,dist_metric=user_euclidean_dist_demographic):
	user=users_list[user_id-1];
	movie=movies_list[movie_id-1];
	nns=k_NN(user,k);
	avg_rating=0;
	ctr=0;
	sum_of_inv_dists=0;
	for n_users in nns:
		if movie_id in n_users.ratings:
			dist=dist_metric(n_users,users_list[user_id-1])
			if dist!=0:
				avg_rating+=float(n_users.ratings[movie_id])/dist;
				ctr+=1;
				sum_of_inv_dists+=float(1/dist);
	avg_rating=float(avg_rating)/sum_of_inv_dists;
	#print ctr, sum_of_dists;
	return avg_rating;


k_NN(users_list[1],5);

with open('u.data') as datafile:
        	for line in datafile:
        		[u,mov_id,rat,tstamp]=line.split('\t');
        		users_list[int(u)-1].ratings[int(mov_id)]=int(rat);
        		

#print users_list[195].ratings;
print predict_rating(195,258)

#for i in range(0,10):
#	print user_euclidean_dist_demographic(users_list[9],users_list[i]);

user_movie_matrix=[[0 for _ in range(len(movies_list))] for _ in range(len(users_list))];
for user in users_list:
	for key in user.ratings:
		user_movie_matrix[user.user_id-1][key-1]=user.ratings[key];

#print user_movie_matrix[195];
import numpy as np
u,s,v=np.linalg.svd(np.array(user_movie_matrix));

