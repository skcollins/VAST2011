__author__ = 'susancollins'

from tfidf import *
import ner

# This file is is used to create matricies used for gensim. Matricies are written
# to file, so this only needs to be done once

#=====DICTIONARY AND MATRIX INCLUDES UNIQUE WORDS================
# #Create dictionary for each unique word to a token id.
# allDictionary = corpora.Dictionary(allWords)
# allDictionary.save('allFiles.dict') # store the dictionary, for future reference
# allDictionary.compactify()
# #Create matrix representation of corpus and save
# corpus = [allDictionary.doc2bow(text) for text in allWords]
# corpora.MmCorpus.serialize('allFiles.mm', corpus) # store to disk, for later use
# #Removes unique words in the dictionary

#=====DICTIONARY AND MATRIX DOES NOT INCLUDE UNIQUE WORDS================
# #Removes unique words in the dictionary
# allWords = pickleToObject("allWords.p")
# all_tokens= pickleToObject('all_tokens.p')
# counter = Counter(all_tokens)
# tokens_once = set(word for word in set(all_tokens) if counter[word] == 1)
# allWords_NU = [[word for word in text if word not in tokens_once]
#                for text in allWords]
#
# #Create dictionary for each word to a token id.
# allDictionary_NU = corpora.Dictionary(allWords_NU)
# allDictionary_NU.save('allFiles_NU.dict') # store the dictionary, for future reference
# allDictionary_NU.compactify()
#
# #Create matrix representation of corpus and save
# corpus = [allDictionary_NU.doc2bow(text) for text in allWords]
# corpora.MmCorpus.serialize('allFiles_NU.mm', corpus) # store to disk, for later use