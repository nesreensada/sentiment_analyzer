class Comment(object):
	"""
 	Youtube Comment class 
	"""
	def __init__(self, text, comment_id, video_id, sentiment =''):
		"""Method for initializing a Comment object
		Args: 
			text (str)
			video_id (int)
			comment_id (str)
		Attributes:
			text : comment text
			video_id : unique video_id associated with the comment
			comment_id : comment_id
		"""
		self.text = text
		self.comment_id = comment_id
		self.video_id = video_id
		self.sentiment  = sentiment

	def set_sentiment(self, sentiment):
		"""Method for setting the sentiment of a comment
		Args: 
			sentiment (str)
		Returns:
			None
		"""
		self.sentiment = sentiment
