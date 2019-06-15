from gensim.models import Word2Vec

def main():
	
	fname = "bloomberg_news_149000"
	stock_news_model = Word2Vec.load(fname)
	
	seed_words = ["surge", "rise", "shrink", "jump", "drop", "fall", "plunge", "gain", "slump"]
	
	bag_of_words = []
	for i in xrange(0,5):
		bag_of_words.append(list(seed_words))
		seed_words = find_similar_words(stock_news_model,seed_words)
		
	
	#flattening the list
	bag_of_words = [item for sublist in bag_of_words for item in sublist]
	
	with open("feature_words_list","w") as outfile:
		for word in bag_of_words:
			outfile.write(str(word)+"\n")


def find_similar_words(model,words):
	final_words = []
	for word in words:
		try:
			
			print "words similar to "+ word
			cur_similar_words = model.most_similar(word, topn=5)
			
			print cur_similar_words
			
			for cur_word in cur_similar_words:
				final_words.append(cur_word[0])
		except:
			print " word: " + word + " not in vocabulary"
	
	unique_words = set(final_words)
	return unique_words
			
	
	

if __name__=="__main__": main()