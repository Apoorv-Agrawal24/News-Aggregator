import flask
from flask import request, jsonify, render_template
import feedparser


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api', methods=['GET'])
def rss():
	if 'site' in request.args:
		website = request.args['site']
		print(website)
	else:
		return 'Error: No site provided. Please enter a site.'

	feed = feedparser.parse(website)
	return feed


@app.route('/')
def index():
	import database
	feed = database.returndb()
	return render_template('index.html', feed = feed)
	'''
	import database
	return database.returndb()
	'''
app.run()


'''
import feedparser


NewsFeed = feedparser.parse("http://rss.cnn.com/rss/cnn_topstories.rss")

for entry in NewsFeed.entries:
	print(entry.link) 

print(NewsFeed.entries[1].keys())
'''