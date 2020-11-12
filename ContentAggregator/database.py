import sqlite3
import json
import requests
import random


def nothing():

	conn = sqlite3.connect('feeds.db')
	c = conn.cursor()

	c.execute(
		'''
		DROP TABLE feeds
		'''
	)

	conn.commit()

	c.execute(
		'''
		CREATE TABLE IF NOT EXISTS feeds (
			title TEXT,
			summary TEXT,
			link TEXT,
			published TEXT
		)
		'''
	)

	conn.commit()
	conn.close()

def addRowsFromJson(feed):
	conn = sqlite3.connect('feeds.db')
	c = conn.cursor()

	entries = feed['entries']

	with open('feed.txt', 'w') as file:
		for entry in entries:
			#print(entry['published'])
			summary = ''
			for char in entry['summary']:
				if char == '<':
					break

				summary += char

			title = entry['title']

			try:
				published = entry['published']
			except Exception:
				published = ''

			link = entry['link']

			file.write('\n' + title + '\n' + '*' * len(title) + '\n' + summary + '\n\n')

			c.execute('INSERT INTO feeds VALUES (:title, :summary, :link, :published)', 
				{'title' : title, 'summary' : summary, 'link' : link, 'published' : published})
			conn.commit()

	conn.close()


def update():
	nothing()
	addRowsFromJson(requests.get('http://127.0.0.1:5000/api?site=http://rssfeeds.usatoday.com/UsatodaycomNation-TopStories').json())
	addRowsFromJson(requests.get('http://127.0.0.1:5000/api?site=http://rss.cnn.com/rss/cnn_topstories.rss').json())

def returndb():
	conn = sqlite3.connect('feeds.db')
	c = conn.cursor()

	c.execute('SELECT * FROM feeds')
	feed = c.fetchall()
	conn.close()
	
	random.shuffle(feed)

	return feed