import requests
import sys
import re
import json
from bs4 import BeautifulSoup
from multiprocessing import Pool
import csv
import glob
import os

headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"}
csvheader = ['user_id', 'name', 'nick','articles_count','comments_count', 'following_count','followers_count',
		     'regular_articles_count','pro_articles_count','stocktalks_count', 'instablogs_count', 
		     'premium_articles_count','likes_count','member_since','bio_tags']
file_path = './data/%s_meta'%('contributors')

def get_user_profile(user_id, user_type):
	url = 'http://seekingalpha.com/user/%s/'%(user_id)
	
	r = requests.get(url, headers=headers)
	r = r.text.split('\n')[-1].split('init(')[1].split(');')[0]
	s = json.loads(r)
	#print s.keys()
	profile = s["profile_info"]
	object_count = s['object_count']
	profile.update(object_count)
	with open('./data/%s_meta.csv'%(user_type), 'a') as wf:
		Writer = csv.writer(wf)
		Writer.writerow([profile[key] for key in csvheader])

def get_user_ids(user_type):
	useridPath = './%s.csv'%(user_type)
	with open(useridPath, 'r') as f:
		Reader  = csv.reader(f)
		id_list = []
		for row in Reader:
			if row[0].isdigit(): 
				id_list.append(row[0])
			else:
				exit('Illigal ID, pls check the user list file.')
		return id_list

def master(n_process, user_type):
	user_ids = get_user_ids(user_type)
	with open('./data/%s_meta.csv'%(user_type), 'w') as wf:
		Writer = csv.writer(wf)
		Writer.writerow(csvheader)
	pool = Pool(processes=n_process)    # set the processes max number 3
	for user_id in user_ids:
		result = pool.apply_async(get_user_profile, (user_id, user_type, ))
	pool.close()
	pool.join()
	if result.successful():
		print 'successful'


if __name__ == "__main__":
	master(3,'contributors')
	#get_user_profile(769697,'contributors')

