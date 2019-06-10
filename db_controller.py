import psycopg2 
from comment import Comment

class DBController(object):
	"""
	DBController class to access, retrieve, update postgresql 
	"""
	def __init__(self, **config):
		"""Method for initializing a DB object
		Args: 
		   config: dicitionary containing the DB parameters
		"""
		self.config = config
		
	def check_comments_existance(self):
		"""Method for checking for the existance of comments table in the DB 
		Args: 
		   None
		Returns:
			boolean: True if comments table exist and False otherwise
		"""
		try:
			query = "select exists(select * from information_schema.tables where table_name=%s)"
			connection = self.get_connection()
			cursor = connection.cursor()
			cursor.execute(query,("comments",))
			result = cursor.fetchone()[0]
			cursor.close()
			return result
		except Exception :
			raise

	def create_comments_table(self):
		"""Method for creating comments table in the DB 
		the table contains comment text, video id for that comment,
		comment_id and sentiment 
		Args: 
		   None
		Returns:
			None
		"""
		try:
			if self.check_comments_existance():
				query = """CREATE TABLE comments(
					id serial PRIMARY KEY,
				   video_id text NOT NULL,
				   comment text NOT NULL,
				   comment_id text UNIQUE NOT NULL,
				   sentiment text 
				);"""
				connection = self.get_connection()
				cursor = connection.cursor()
				cursor.execute(query)
				cursor.close()
		except Exception :
			raise

	def get_connection(self):
		"""Method to get the conneciton to the DB  
	    Args: 
	       None
	    Returns:
	    	connection object to the DB using config
	    """
		try:
			return psycopg2.connect(**self.config)
		except Exception:
			raise


	def insert_comments(self, comment):
		"""Method to insert youube comment into the DB  
	    Args: 
	       comment(object):containing comment_id, text, video_id  
	    Returns:
	    	None
	    """
		try:
			query = "INSERT INTO COMMENTS (video_id, comment, comment_id, sentiment) VALUES (%s, %s,%s,%s)"
			connection = self.get_connection()
			cursor = connection.cursor()
			cursor.execute(query, (comment.video_id, comment.text, comment.comment_id, comment.sentiment))
			connection.commit()
			cursor.close()
		except Exception:
			raise

	def update_comment_sentiments(self, sentiment, comment_id):
		"""Method to insert comments to the DB  
	    Args: 
	       comment(object):containing comment_id, text, video_id  
	    Returns:
	    	None
	    """
		try:	
			query = "UPDATE COMMENTS sentiment = %s where comment_id = %s"
			connection = self.get_connection()
			cursor = connection.cursor()
			cursor.execute(query, (sentiment, comment_id))
			connection.commit()
			cursor.close()
		except Exception:
			raise

	def select_all_comments(self):
		"""Method to retrieve comments stored in the DB  
	    Args: 
	       None 
	    Returns:
	    	List of comments
	    """
		try:	
			query = "SELECT * FROM COMMENTS"
			connection = self.get_connection()
			cursor = connection.cursor()
			cursor.execute(query)
			comments = []
			for row in cursor:
				comments.append(Comment(text = row['comment'], comment_id = row['comment_id'], video_id = row['video_id'], sentiment=row['sentiment']))
			connection.commit()
			cursor.close()
			return comments
		except Exception:
			raise






