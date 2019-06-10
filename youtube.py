import googleapiclient.discovery
from comment import Comment

class Youtube(object):
	"""
 	Youtube class to use REST requests using Google Youtube API V3
    https://developers.google.com/youtube/v3/docs/
	"""
	def __init__(self, service_name, api_key, api_version):
		"""Method for initializing a Youtube object
		Args: 
		service_name (str)
		api_key (int)
		api_version(str)
		Attributes:
		service_name: Google API service
		api_key: Google API key for Youtube
		api_version: api version 
		"""
		self.api_key = api_key
		self.service_name = service_name
		self.api_version =  api_version
		self.service = None	


	def get_endpoint(self):
		"""Method to get the conneciton to the youtube api 
	    Args: 
	       None
	    Returns:
	    	connection object to the google api using config
	    """
		try:
			self.service = googleapiclient.discovery.build(serviceName=self.service_name, version=self.api_version, developerKey = self.api_key)
			return self.service
		except Exception:
			raise

	def get_video_comments(self, video_id):
		"""Method to return list of video comments
		Args: 
		    video_id (str): Youtube video unique id from url

		Returns: 
			list: comment objects including replies 
		"""
		try:

			parameters = {
			    'textFormat': 'plainText', 
			    'part': "snippet,replies", 
			    'videoId': video_id,
			    'maxResults':100
			}
			comments = []
			service = self.get_endpoint()
			results = self.service.commentThreads().list(**parameters).execute()
			next_page_token = results.get('nextPageToken')
			while next_page_token:
				for item in results['items']:
					comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
					comment_id = item['id']
					comment = Comment(comment_text, comment_id, video_id)
					comments.append(comment)

					# get replies to each comment
					if 'replies' in item.keys():
						for reply_item in item['replies']['comments']:
							reply_text = reply_item['snippet']['textDisplay']
							reply_id = reply_item['id']
							reply = Comment(reply_text, reply_id, video_id)
							comments.append(reply)
				next_page_token = results.get('nextPageToken')	        
				parameters['pageToken'] = next_page_token
				results = self.service.commentThreads().list(**parameters).execute()
			return comments 
		except KeyError as key_error:
			raise
		except Exception as e:
			raise