import os
from gensim.models import Word2Vec
from nltk.corpus import stopwords
import re
import sys

# Download the punkt tokenizer for sentence splitting
import nltk.data

# Load the punkt tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

source = sys.argv[1]

def main():
	rootdir = os.getcwd()
	file_list = []
	for subdir, dirs, files in os.walk(rootdir + "/"+source):
		for file in files:
			
			file_list.append(os.path.join(subdir, file))
			
	print ("Total files in "+source+": " + str(len(file_list)))


	contents=''
	counter=0
	for file in file_list:
		with open(file) as infile:
			contents+= infile.read()
		if counter % 1000 == 0:
			prepare_model_and_save(contents.decode("utf-8", "ignore"),counter)
			print("Progress: "+ str((float(counter)/len(file_list))*100))
		counter+=1
			
	
	
def prepare_model_and_save(contents,counter):
	wordlist = news_to_sentences(contents,tokenizer)
		
	stock_news_model = Word2Vec(wordlist)
	
	stock_news_model.init_sims(replace=True)
	
	model_name = source+"_news_"+ str(counter)
	stock_news_model.save(model_name)
	
	#model = Word2Vec.load(fname) 
	
	try:
		print stock_news_model.most_similar("increase", topn=5)
	except:
		print "exception"

	
# Define a function to split a news into parsed sentences
def news_to_sentences( news, tokenizer, remove_stopwords=False ):
	# Function to split a news into parsed sentences. Returns a 
	# list of sentences, where each sentence is a list of words
	#
	# 1. Use the NLTK tokenizer to split the paragraph into sentences
	
	raw_sentences = tokenizer.tokenize(news.strip())
	
	#
	# 2. Loop over each sentence
	sentences = []
	for raw_sentence in raw_sentences:
		# If a sentence is empty, skip it
		if len(raw_sentence) > 0:
			# Otherwise, call review_to_wordlist to get a list of words
			sentences.append( sentence_to_wordlist( raw_sentence, \
			  remove_stopwords ))
	#
	# Return the list of sentences (each sentence is a list of words,
	# so this returns a list of lists
	return sentences
	
def sentence_to_wordlist( sentence, remove_stopwords=False ):
	# Function to convert a document to a sequence of words,
	# optionally removing stop words.  Returns a list of words.
	
	#Remove non-letters
	text = re.sub("[^a-zA-Z]"," ", sentence)
	#
	#Convert words to lower case and split them
	words = text.lower().split()
	#
	#Optionally remove stop words (false by default)
	if remove_stopwords:
		stops = set(stopwords.words("english"))
		words = [w for w in words if not w in stops]
	#
	#Return a list of words
	return(words)
	
if __name__=="__main__" : main()