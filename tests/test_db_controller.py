import pytorch 
import DBController
import Comment

def test_insert_comments:
	params = { "user" : "nisreen", "host" : '127.0.0.1', "port" : "5432", "database" : 'youtube_comments'}
	db = DBController(params)
	comment = Comment(video_id = '_VB39Jo8mAQ', comment_id= 'test_test_test', comment=text)
	db.insert_comments(comment)
	


