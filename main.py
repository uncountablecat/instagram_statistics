import os
import sys
import json
import urllib as urllib
import requests
import unicodecsv as csv # emoji might be in captions


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
		else:
			all_posts_fetched = True

	return post_list

def extract_statistics(post_list):
	'''
	INTAKE: a list of posts
	RETURN: a dictionary of lists
	'''
	num_of_posts = len(post_list)

	stats_list = []
	caption_list = []

	for i in range(0, num_of_posts):
		stats_list.append([post_list[i]['code'], post_list[i]['likes']['count'], post_list[i]['comments']['count']])
		if post_list[i]['caption'] == None: # check if there is caption
			caption_list.append([post_list[i]['code'], ''])
		else:
			caption_list.append([post_list[i]['code'], post_list[i]['caption']['text'].replace("\n", " ")]) 
			# some captions have '\n' but we want them to be in one line

	account_info = {'stats_list':stats_list, 'caption_list':caption_list}

	return account_info

def download_photos(post_list):
	'''
	INTAKE: a list of posts
	RETURN: 0
	'''
	if (os.path.exists("/Users/chaoguo/Desktop/"+ insta_id) == False):
			os.mkdir("/Users/chaoguo/Desktop/"+ insta_id)
			
	for x in post_list:
		url = x["images"]["standard_resolution"]["url"].replace("s640x640", "s1080x1080")
		file_name = x["code"]
		urllib.urlretrieve(url, "/Users/chaoguo/Desktop/"+ insta_id + "/" + file_name + ".jpg")

	return 0

def write_to_csv(list_name,file_name,col_names):
	'''
	INTAKE: a list, name of the csv file, column names of the csv file
	RETURN: a csv file with given name and column names
	'''
	output_file = open(file_name+'.csv','w')
	output_writer = csv.writer(output_file,encoding='utf-8')

	output_writer.writerow(col_names)

	for i in list_name:
		output_writer.writerow(i)
		
	output_file.close()

def write_bio(insta_id):
	'''
	INTAKE: an Instagram id
	RETURN: a csv file with bio
	'''
	r = requests.get("https://www.instagram.com/" + insta_id)
	page_source = r.text

	start_index = page_source.find("<meta property=\"og:description\" content=") + len("<meta property=\"og:description\" content=")
	end_index = page_source.find("/>\n",start_index)
	bio = page_source[start_index:end_index]
	
	bio_file = open(insta_id + '_bio.csv','w')
	bio_writer = csv.writer(bio_file, encoding = 'utf-8')
	bio_writer.writerow(['instagram_id','bio'])
	bio_writer.writerow([insta_id,bio])

if __name__ == '__main__':
	insta_id = sys.argv[1]

	post_list = get_post_list(insta_id)
	account_info = extract_statistics(post_list)

	write_to_csv(account_info['stats_list'],'stats_list',['post_id','num_of_likes','num_of_comments'])
	write_to_csv(account_info['caption_list'],'caption_list',['post_id','caption'])
	# download_photos(post_list)
	write_bio(insta_id)