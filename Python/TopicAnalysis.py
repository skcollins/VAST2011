from tfidf import *
from operator import itemgetter

from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()

#================ 500 File dictionary and corpus ====================================
#_500FilesDict= get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/500/*.txt')
#objectToPickle("_500FilesDict_blobDictionary.p", _500FilesDict)
#_500FilesDict = pickleToObject("_500FilesDict_blobDictionary.p")
#files = _500FilesDict.values()


#Make String[String[]] for words in the 500 files
#wordListArray =[remove_stopWords(file.lower().words, stoplist) for file in files]

# #Lemmatize words
#wordListArray = [[lmtzr.lemmatize(word) for word in file] for file in wordListArray]

# #Remove words that appear <= 5 times in 500 file corpus
# # for topic modeling this is okay
# wordListArray = removeUniques(wordListArray, 5)


#Save words into a dictionary
# dictionary = corpora.Dictionary(wordListArray)
# dictionary.save('500File.dict') # store the dictionary, for future reference
# print dictionary
# dictionary = corpora.Dictionary.load('500File.dict')
# print dictionary
# dictionary.filter_extremes(no_below=5, no_above=0.75)
# print dictionary

#Save corpus in Mm format
#corpus = [dictionary.doc2bow(text) for text in wordListArray]
#corpora.MmCorpus.serialize('500File_1000WordDict.mm', corpus) # store to disk, for later use
#corpus = corpora.MmCorpus('500File_1000WordDict.mm')

#Initialzie tfidf model
#tfidf = models.TfidfModel(corpus)
#tfidf.save("tfidf500file.model")
#tfidf = models.TfidfModel.load("tfidf500file.model")

#corpus_tfidf = tfidf[corpus]

#======================= All Files Dictionary and Corpus========================
# #Get values
# allFiles = pickleToObject("allFilesDict.dict.p").values()
#
# #Make String[String[]] for words in the 500 files
# wordListArray =[remove_stopWords(file.lower().words, stoplist) for file in allFiles]
#
# # #Lemmatize words
# wordListArray = [[lmtzr.lemmatize(word) for word in file] for file in wordListArray]

# Save words into a dictionary
# dictionary = corpora.Dictionary(wordListArray)
# dictionary.save('AllFile.dict') # store the dictionary, for future reference
dictionary = corpora.Dictionary.load('AllFile.dict')
print dictionary

#Filter out extremes: words that appear less than 500 items and in more than 75% of documents
dictionary.filter_extremes(no_below=5, no_above=0.75)
print dictionary

# #Create and save corpus in Mm format
# corpus = [dictionary.doc2bow(text) for text in wordListArray]
# corpora.MmCorpus.serialize('AllFiles_SanitizedDict.mm', corpus) # store to disk, for later use
# #corpus = corpora.MmCorpus('AllFiles_SanitizedDict.mm')
#
# #Unpack 13 files for classification
# _13Files = corpora.MmCorpus('13File_SanitizedDic.mm')
#
# #=============LDA MODEL 15 TOPICS  =================================
# lda = models.LdaModel(corpus, id2word=dictionary, num_topics=15, chunksize=15, passes=2)
# lda.save("AllFile_t15c15p2.lda")
# #lda= models.LdaModel.load("500File_t15c15p15.lda")
# topics =  lda.show_topics(topics=-1, topn=50, log=False, formatted=True)
# writeList("AllFile_LDA_t15c15p2_SanitizedDic.txt", topics)
#
#
#
# #Apply model to files
# corpus_lda = lda[_13Files]
# for doc in corpus_lda:
#     print max(doc,key=lambda item:item[1])
#
#
# #=============LDA MODEL 25 TOPICS  =================================5
# lda = models.LdaModel(corpus, id2word=dictionary, num_topics=25, chunksize=15, passes=2)
# topics = lda.show_topics(topics=-1, topn=50, log=False, formatted=True)
# lda.save("AllFile_t25c15p2.lda")
# writeList("500Files_LDA_T25_c15p15.txt", topics)
#
# #Apply model to files
# corpus_lda = lda[_13Files]
# for doc in corpus_lda:
#     print max(doc,key=lambda item:item[1])

#=============LDA MODEL 15 TOPICS 1000 Word Dictionary  =================================
#_500_lda = models.LdaModel(corpus, id2word=dictionary, num_topics=15, chunksize=15, passes=15)



#==========================LSI MODEL 15 Topics==========================
#lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=15) # initialize an LSI transformation
#lsi.save("500File_t15.lsi")
# lsi = models.LsiModel.load("500File_t15.lsi")
#topics = lsi.show_topics(num_topics=-1, num_words=50, log=False, formatted=True)

# writeList("500Files_LSI_t15.txt", topics)

# #==========================LSI MODEL 25 Topics==========================
# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=25) # initialize an LSI transformation
# topics = lsi.show_topics(num_topics=-1, num_words=50, log=False, formatted=True)
# writeList("500Files_LSI_t25.txt", topics)