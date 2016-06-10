import json
import requests
def get_post_list(insta_id):
	'''
	INTAKE: an Instagram insta_id
	RETURN: a list of posts (photos or videos)
	'''
	r = requests.get('https://www.instagram.com/' + insta_id  + '/media/')
	js_file = r.json()
	post_list = js_file['items']

	return post_list

def extract_statistics(post_list):
	'''
	INTAKE: a list of posts (photos or videos)
	RETURN: a dictionary containing number of likes and comments of each post
	'''
	num_of_posts = len(post_list)
	stats_dic = {}

	for i in range(0,num_of_posts-1):
		stats_dic[post_list[i]['code']] = [post_list[i]['likes']['count'], post_list[i]['likes']['count']]
	
	return stats_dic
