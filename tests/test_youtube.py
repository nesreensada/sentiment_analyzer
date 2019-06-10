import Youtube 
import pytest


def test_get_video_comments():

	API_KEY = 'AIzaSyAZPBKsgQraYdcQOJFgiXUd9IU3M9NtYJc' 
	yt = Youtube(api_key= API_KEY, api_version = 'v3', service_name='youtube')
	video_id = '_VB39Jo8mAQ'
	comments = yt.get_video_comments(video_id)
	comments_text = [comment.text for comment in comments]
	# test
	assert "This is why they use chips in casino's and poker games." in comments_text

	