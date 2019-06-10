from flask import Flask, g
from flask_restful import Api, Resource, reqparse
from youtube import Youtube
from comment import Comment
from db_controller import DBController
import yaml
from classifier import Classifier

app = Flask(__name__)
api = Api(app=app)

def get_config():
	"""Method for reading configuration file
		Args: 
		   None
		Returns:
			config 
	"""
	with open('config.yml','r') as ymlfile:
		cfg = yaml.load(ymlfile)
	return cfg

def initialize():
	"""Method for initializing a youtube object, connection to the DB and load comments 
	get the comments for the youtube videos ids listed in the DB, store the comments in the DB, 
	train the classifier and print the classifier metrics   
		Args: 
		   config: dicitionary containing the DB parameters
	"""
	with app.app_context():
		g.config = get_config()
		g.yt = Youtube(api_key= g.config ['youtube']['API_KEY'], api_version = g.config ['youtube']['API_VERSION'], service_name=g.config['youtube']['API_SERVICE_NAME'])
		video_ids = g.config['youtube_videos_id']
		g.comments = []
		for video_id in video_ids:
			g.comments.extend(g.yt.get_video_comments(video_id))
		#db_params = {"user":g.config['db']['user'], "host":g.config['db']["host"], "port":g.config['db']["port"],"database": g.config['db']["database"]}
		g.db = DBController(**g.config['db'])

		# create table if it does not exist:
		g.db.create_comments_table()

		# train classifier
		g.classifier = Classifier()
		g.classifier.train()

		# predication of the comments
		for comment_item in g.comments:
			text = comment_item.text
			predication = g.classifier.predict(comment_text)
			comment_item.sentiment  = predication
			# insert the comment in DB 
			g.db.insert_comments(comment_item)		
	

class SentimentAnalysis(Resource):
	def get(self):
		comments = g.db.select_all_comments()
		for comment_item in comments:
			return comment_item, 200

	def post(self, comment_text):
		predication = g.classifier.predict(comment_text)
		return predication, 201 
      
api.add_resource(SentimentAnalysis, "/sentiment/")


if __name__ == '__main__':
	initialize()
	app.run()


