from __future__ import division, unicode_literals
import math
from textblob import TextBlob as tb
import os

def main():
	rootdir = os.getcwd()
	file_list = []
	for subdir, dirs, files in os.walk(rootdir + "/reuters"):
		for file in files:
			file_list.append(os.path.join(subdir, file))
			
	print ("Total files in Reuters: " + str(len(file_list)))


	bloblist= []
	cutoff = 0 
	for file in file_list:
		if cutoff > 3 : break
		print("Using file "+ file)
		with open(file) as infile:
			bloblist.append(tb(infile.read()))
		cutoff+=1
	for i, blob in enumerate(bloblist):
		print("Top words in document {}".format(i + 1))
		scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
		sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
		for word, score in sorted_words[:3]:
			print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)
	
	
if __name__=="__main__": main()