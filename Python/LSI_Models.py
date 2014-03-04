__author__ = 'susancollins'

from tfidf import *

#=============All Files (Unique words included)=======================
allDictionary = corpora.Dictionary.load('allFiles_NU.dict')
all_corpus = corpora.MmCorpus('allFiles_NU.mm')

#Initialize tfidf model
tfidf = models.TfidfModel(all_corpus, id2word=allDictionary)
corpus_tfidf = tfidf[all_corpus] #calculate tfidf for all features in corpus
tfidf.save("allFilesTFIDFModel")
#tfidf=models.TfidfModel.load('allFilesTFIDFModel')

#==========================LSI MODEL 15 Topics==========================
lsi = models.LsiModel(corpus_tfidf, id2word=allDictionary, num_topics=15) # initialize an LSI transformation
lsi.save('allFilesLSAModel_t15_NU')
topics = lsi.show_topics(num_topics=-1, num_words=50, log=False, formatted=True)
writeList("AllFiles_LSI_T15_NU.txt", topics)

#==========================LSI MODEL 25 Topics==========================
lsi = models.LsiModel(corpus_tfidf, id2word=allDictionary, num_topics=25) # initialize an LSI transformation
lsi.save('allFilesLSAModel_t25_NU')
topics = lsi.show_topics(num_topics=-1, num_words=50, log=False, formatted=True)
writeList("AllFiles_LSI_T25_NU.txt", topics)

#==========================LSI MODEL 100 Topics==========================
lsi = models.LsiModel(corpus_tfidf, id2word=allDictionary, num_topics=100) # initialize an LSI transformation
lsi.save('allFilesLSAModel_t100_NU')
topics = lsi.show_topics(num_topics=-1, num_words=50, log=False, formatted=True)
writeList("AllFiles_LSI_T100_NU.txt", topics)

#==========================LSI MODEL 200 Topics==========================
lsi = models.LsiModel(corpus_tfidf, id2word=allDictionary, num_topics=200) # initialize an LSI transformation
lsi.save('allFilesLSAModel_t200_NU')
topics = lsi.show_topics(num_topics=-1, num_words=50, log=False, formatted=True)
writeList("AllFiles_LSI_T200_NU.txt", topics)

#==========================LSI MODEL 300 Topics==========================
lsi = models.LsiModel(corpus_tfidf, id2word=allDictionary, num_topics=300) # initialize an LSI transformation
lsi.save('allFilesLSAModel_t300_NU')
topics = lsi.show_topics(num_topics=-1, num_words=50, log=False, formatted=True)
writeList("AllFiles_LSI_T300_NU.txt", topics)

# corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
# print "---------------------Corpus LSI--------------------"
# for doc in corpus_lsi:
#    print doc
