__author__ = 'susancollins'

from tfidf import *



# lda = models.LdaModel(corpus, id2word=dictionary, num_topics=3, passes=5)
# corpus_lda = lda[corpus]
# print "---------------------Corpus LDA--------------------"
# for doc in corpus_lda:
#    print doc


#=============All Files (Unique words included)=======================
allDictionary = corpora.Dictionary.load('allFiles_NU.dict')
all_corpus = corpora.MmCorpus('allFiles_NU.mm')

#=============LDA MODEL 15 TOPICS  =================================
# all_lda = models.LdaModel(all_corpus, id2word=allDictionary, num_topics=15, chunksize=15, passes=10)
# all_lda.save("allFilesLDAModel_t15_c15p10_NU")
# topics =  all_lda.show_topics(topics=-1, topn=50, log=False, formatted=True)
# writeList("AllFiles_LDA_T15_c15p10_NU.txt", topics)
#
# all_lda = models.LdaModel(all_corpus, id2word=allDictionary, num_topics=15, chunksize=15, passes=20)
# all_lda.save("allFilesLDAModel_t15_c15p20_NU")
# topics =  all_lda.show_topics(topics=-1, topn=50, log=False, formatted=True)
# writeList("AllFiles_LDA_T15_c15p20_NU.txt", topics)

#=============LDA MODEL 25 TOPICS  =================================
# all_lda = models.LdaModel(all_corpus, id2word=allDictionary, num_topics=25, chunksize=15, passes=1)
# all_lda.save("allFilesLDAModel_t25_c15p1_NU")
# topics =  all_lda.show_topics(topics=-1, topn=50, log=False, formatted=True)
# writeList("AllFiles_LDA_T25_c15p1_NU.txt", topics)
#
# #=============LDA MODEL 100 TOPICS  =================================
# all_lda= models.LdaModel(all_corpus, id2word=allDictionary, num_topics=100, chunksize = 15, passes=10)
# all_lda.save("allFilesLDAModel_t100_c15p10_NU")
# topics =  all_lda.show_topics(topics=-1, topn=50, log=False, formatted=True)
# writeList("AllFiles_LDA_T100_c15p10_NU.txt", topics)

# all_lda= models.LdaModel(all_corpus, id2word=allDictionary, num_topics=150, chunksize = 15, passes=10)
# all_lda.save("allFilesLDAModel_t150_c15p10")
# topics =  all_lda.show_topics(topics=-1, topn=50, log=False, formatted=True)
# writeList("AllFiles_LDA_T150_c15p10_NU.txt", topics)
#
# # #=============LDA MODEL 200 TOPICS  =================================
# all_lda= models.LdaModel(all_corpus, id2word=allDictionary, num_topics=200, chunksize = 15, passes=10)
# all_lda.save("allFilesLDAModel_t200_c15p10")
# topics =  all_lda.show_topics(topics=-1, topn=50, log=False, formatted=True)
# writeList("AllFiles_LDA_T200_c15p10_NU.txt", topics)
#
#=============LDA MODEL 300 TOPICS  =================================
all_lda= models.LdaModel(all_corpus, id2word=allDictionary, num_topics=300, chunksize = 15, passes=10)
all_lda.save("allFilesLDAModel_t300_c15p10_NU")
topics =  all_lda.show_topics(topics=-1, topn=50, log=False, formatted=True)
writeList("AllFiles_LDA_T300_c15p10_NU.txt", topics)

# all_corpus_lda = all_lda[all_corpus]
# print "---------------------Corpus LDA--------------------"
# for doc in all_corpus_lda:
#     print doc