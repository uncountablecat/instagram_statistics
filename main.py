import json
import requests
import csv
import sys


def get_post_list(insta_id):
	'''
	INTAKE: an Instagram insta_id
	RETURN: a list of posts (photos or videos)
	'''
	post_list = []
	max_id = ''
	all_posts_fetched = False

	while all_posts_fetched == False:
		r = requests.get('https://www.instagram.com/' + insta_id  + '/media/'+('?max_id=' + max_id if max_id != '' else ''))
		js_file = r.json()

		for i in js_file['items']:
			post_list.append(i)

		if js_file['more_available'] == True:
			max_id = js_file['items'][-1]['id']
			print(max_id)
		else:
			all_posts_fetched = True

	return post_list

def extract_statistics(post_list):
	'''
	INTAKE: a list of posts (photos or videos)
	RETURN: a list containing number of likes and comments of each post
	'''
	num_of_posts = len(post_list)
	stats_list = []

	for i in range(0,num_of_posts):
		stats_list.append([post_list[i]['code'], post_list[i]['likes']['count'], post_list[i]['comments']['count']])
	
	return stats_list

def write_to_csv(stats_list):
	'''
	INTAKE: a list containing statistics
	RETURN: a csv file
	'''
	output_file = open('account_statistics.csv','w')
	output_writer = csv.writer(output_file)

	output_writer.writerow(['post_id','num_of_likes','num_of_comments'])
	for i in stats_list:
		output_writer.writerow(i)
		
	output_file.close()

if __name__ == '__main__':
	insta_id = sys.argv[1]

	post_list = get_post_list(insta_id)
	stats_list = extract_statistics(post_list)
	write_to_csv(stats_list)
