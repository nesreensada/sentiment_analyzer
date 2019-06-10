Get comments from top YouTube political videos, create a sentiment classifier.

Determine sentiment of Youtube video per comment based analysis using Naive Bayes from NLTK library by analyzing video comments based on positive/negative sentiment. 
- The imdb movie reviews data set from NLTK library was used to train the classifier and it contained pos and neg sentiment label
- Naive bayes is probablistic machine learning algorithm that depending on the words the comment contain it will gives a probability of the comment being a positive or negative sentiment


## Install Instructions
Required packages
```
	- googleapiclient.discovery
	- argparse
	- psycopg2
	- flask
	- flask_restplus
	- nltk
	- postgresql
```

## How to Use
```
1)change the configuration in the config.yml file:
   - create a new postgresql DB and change the configuration listed under db parameter
   - add a proper API_KEY to gain to youtube api to read the comments
   - change the list of video ids in the config 
2) install the required packages 
3) use python3 api.py to run the application and list the comment and the sentiment
```


