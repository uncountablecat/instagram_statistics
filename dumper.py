import sys
import os
import MySQLdb as mysql
import time
import datetime

directory = "./" # where csv files are stored
db_connection = mysql.connect(host = "127.0.0.1", port = 3306, user = "root", passwd = "", db = "testdb") # start connection
c = db_connection.cursor()

# dump to table INST_POST_STATS
# create table inst_post_stats (insta_id varchar(255), post_id varchar(255), num_of_likes int, num_of_comments int, created_ts int, ts int);
filepath = "./kumachen93_post_stats.csv"
if os.stat(filepath).st_size > 0:
	with open(filepath) as f:
		next(f)
		for line in f:
			splitted = line.split(",")
			splitted_new = [splitted[0],splitted[1],int(splitted[2]),int(splitted[3]),int(splitted[4]),int(splitted[5])] # not good enough
			c.execute("INSERT INTO inst_post_stats VALUES (%s,%s,%s,%s,%s,%s)", splitted_new)

# dump to table INST_POST_CAPTIONS
# create table inst_post_captions (insta_id varchar(255), post_id varchar(255), captions varchar(255), ts int) default charset=utf8;
filepath = "./kumachen93_post_captions.csv"
if os.stat(filepath).st_size > 0:
	with open(filepath) as f:
		next(f)
		for line in f:
			splitted = line.split(",")
			splitted_new = [splitted[0],splitted[1],splitted[2],int(splitted[3])]
			c.execute("INSERT INTO inst_post_captions VALUES (%s,%s,%s,%s)", splitted_new) # need to fix unicode and emoji

# dump to table INST_ACCOUNT_BIO
# create table inst_account_bios (insta_id varchar(255), bio varchar(255), ts int);
filepath = "./kumachen93_account_bio.csv"
if os.stat(filepath).st_size > 0:
	with open(filepath) as f:
		next(f)
		for line in f:
			splitted = line.split(",")
			splitted_new = [splitted[0],splitted[1],int(splitted[2])]
			c.execute("INSERT INTO inst_account_bios VALUES (%s,%s,%s)", splitted_new) # need to fix unicode as well, perhaps

# dump to table INST_ACCOUNT_STATS
# create table inst_account_stats (insta_id varchar(255), num_of_posts int, num_of_followers int, num_of_followings int, ts int)
filepath = "./kumachen93_account_stats.csv"
if os.stat(filepath).st_size > 0:
	with open(filepath) as f:
		next(f)
		for line in f:
			splitted = line.split(",")
			splitted_new = [splitted[0],int(splitted[1]),int(splitted[2]),int(splitted[3]),int(splitted[4])]
			c.execute("INSERT INTO inst_account_stats VALUES (%s,%s,%s,%s,%s)", splitted_new)



db_connection.commit() # commit change
db_connection.close() # close connection
