import nltk 
from nltk.probability import *
from nltk.corpus import stopwords
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk import precision, recall, f_measure
import random
import collections
from nltk.tokenize import word_tokenize
import string
import utility 

class Classifier(object):
	"""
	Classifier class to train, create and predict the sentiment of comments
	"""
	def __init__(self):
		"""Method for initializing a classifier object
		Args: 
		   config: dicitionary containing the DB parameters
		"""	
		self.model = utility.load_classifier() 

	def extract_features(self, document):
		"""Method to Extract the features from the comments in words based on top words in 
		the imdb movies dataset 2000 most common words
	    Args: 
	       self  
	    Returns:
	    	None
	    """
		all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
		# limit to the 2000 most common words
		word_features = list(all_words)[:2000] 
		document_words = set(document)
		features = {}
		for word in word_features:
			features['contains({})'.format(word)] = (word in document_words)
		return features


	def train(self):
		"""Method to train the naive bayes classifier using imdb movies review dataset 
		imdb movie dataset contains 2000 movie reviews wiht the category(sentiment) and review text
	    Args: 
	       self  
	    Returns:
	    	None
	    """
	    # document is created as tuple of list of words in the review and the category
		documents = [(list(movie_reviews.words(fileid)), category)
			for category in movie_reviews.categories()
			for fileid in movie_reviews.fileids(category)]

		random.shuffle(documents)
		features_set = [(self.extract_features(document_words), category) for (document_words,category) in documents]
		# using 100 features from the document and last 100 for testing
		train_set, test_set = featuresets[100:], featuresets[:100] 
		classifier = nltk.NaiveBayesClassifier.train(train_set)
		utility.save_classifier(classifier)
		self.model = classifier 
		# print the metrics 
		self.classifier_metrics(test_set)

	def preprocess_comment(self, comment):
		"""Method to remove the punctuation in the comments before predicating the sentiment
	    Args: 
	       comment text  
	    Returns:
	    	clean comment without punctuation and lower case
	    """
		table = str.maketrans({key: " " for key in string.punctuation})
		return comment.lower().translate(table)
		

	def classifier_metrics(self, test_set):
		"""Method to print the classifier metrics(precision, recall, accuracy, f-measure) and the most informative features
		The NLTK metrics module provides functions for calculating all three metrics but we need build 2 sets for each classification label
	    Args: 
	       comment text  
	    Returns:
	    	None
	    """
		classifier = self.model
		refsets = collections.defaultdict(set)
		testsets = collections.defaultdict(set)
		for i, (features, label) in enumerate(test_set):
			refsets[label].add(i)
			observed = classifier.classify(features)
			testsets[observed].add(i)

		print("The Naive bayes classifier accuracy is : {}".format(nltk.classify.accuracy(classifier, test_set)))
		print ('')
		print("The Naive bayes classifier positive sentiment precision is : {}".format(precision(refsets['pos'], testsets['pos'])))
		print("The Naive bayes classifier negative sentiment precision is : {}".format(precision(refsets['neg'], testsets['neg'])))
		print ('')
		print("The Naive bayes classifier positive sentiment recall is : {}".format(recall(refsets['pos'], testsets['pos'])))
		print("The Naive bayes classifier negative sentiment recall is : {}".format(recall(refsets['neg'], testsets['neg'])))
		print ('')
		print("The Naive bayes classifier positive sentiment f-measure is : {}".format(f_measure(refsets['pos'], testsets['pos'])))
		print("The Naive bayes classifier negative sentiment f-measure is : {}".format(f_measure(refsets['neg'], testsets['neg'])))
		print('')
		print('classifier top 5 most informative features is {}'.format(classifier.show_most_informative_features(5)))


	def predict(self, comment):
		"""Method to predict the sentiment of the comment
	    Args: 
	       comment text  
	    Returns:
	    	comment sentiment Negative or Positive
	    """
		clean_comment = self.preprocess_comment(comment)
		comment_tokens = word_tokenize(comment)
		comment_features = extract_features(comment_tokens)
		predication = self.model.classify(comment_features)
		if predication == 'neg':
			return 'Negative Sentiment'
		else:
			return 'Positive Sentiment'


	def sentiment_predication(self, comment):
		"""Method to provide sentiment predication for comment 
	    Args: 
	       comment text  
	    Returns:
	    	Negative or Positive sentiment 
	    """
		if self.model:
			return self.predict(comment)
		else: 
			self.train(self)
			return self.predict(clean_comment)

	