import pickle 
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import os.path


def save_classifier(classifier):
	"""Method to save the trained classifier 
	Args: 
	classifier (object): trained Naive Bayes classifier

	Returns: 
	None 
	"""
	f = open('models/naive_bayes_classifier.pickle', 'wb')
	pickle.dump(classifier, f, -1)
	f.close()

def load_classifier():
	"""Method to load the trained classifier from saved directory
		Args: 
		    None: trained Naive Bayes classifier

		Returns: 
			trained Naive Bayes classifier
	"""
	try:

		file_name = 'models/naive_bayes_classifier.pickle'

		if os.path.isfile(file_name): 
		    f = open(file_name, 'rb')
		    classifier = pickle.load(f)
		    f.close()
		    return classifier
		else:
			return None
	except Exception:
		raise

