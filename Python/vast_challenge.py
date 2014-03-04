__author__ = 'susancollinscollins'


from tfidf import *

# targetList = ["bioterrorism", "microbes", "microbe", "trespass","trespassering","trespasser","trespassers", "suspicious", "food",
#               "farm", "patino", "paramurderers", "raid", "stolen", "laboratory"]
#
terrorCategoryBank = create_TextBlob('/Users/susancollins/Google Drive/Draper/Python/wordLists/terrorCategory.txt').words
terrorWords = create_TextBlob('/Users/susancollins/Google Drive/Draper/Python/wordLists/terroristWords.txt').words
terrorWordBank = [word.lower() for word in terrorWords]
bioTerrorBank = create_TextBlob('/Users/susancollins/Google Drive/Draper/Python/wordLists/bioTerrorism.txt').words

# #word bank from 3295 3040 4085 3212 2260, 0998
# wordBank_4files = ['nicole barns', 'barns', 'cdc', 'center for disease control', 'bioterrorism', 'bryant mcfarlane', 'food supply',
#             'department of agriculture', 'farm animals', 'death of animals', 'death of farm animals', 'animal deaths', 'spore-forming',
#             'microbe', 'microbes', 'roxanne farson', 'edward patino', 'patino', 'biologist', 'biological', 'biological hazard', 'biological hazards'
#             'citizens for ethical treatment of lab mice', 'chemical corp', 'fertilizer', 'hoechst ag', 'chemical industry',
#             'vast university', 'genetic', 'spore', 'flu season', 'food']
#
# #word bank removed fertilizer and chemical industry
# wordBank_4filesv2 = ['nicole barns', 'barns', 'cdc', 'center for disease control', 'bioterrorism', 'bryant mcfarlane', 'food supply',
#             'department of agriculture', 'farm animals', 'death of animals', 'death of farm animals', 'animal deaths', 'spore-forming',
#             'microbe', 'microbes', 'roxanne farson', 'edward patino', 'patino', 'biologist', 'biological', 'biological hazard', 'biological hazards'
#             'citizens for ethical treatment of lab mice', 'chemical corp', 'hoechst ag',
#             'vast university', 'genetic', 'spore','flu season','food']
#
# wordBank_2385_1785 = ['contamination', 'farmers', 'livestock', 'food storage', 'soil', 'livestock deaths', 'livestock'
#                         'vast university', 'uptown', 'stolen equipment', 'tony grenier', 'grenier', 'lab equipment']
#
#
# wordBank_3740 = ['trespassing', 'suspicious individuals', 'beatrice brothers', 'suspicions', 'suspects', 'suspect', 'suspicious']
#
# wordBank_1878 = ['Darwin Crocker', 'gang', 'Paramurderers of Chaos', 'roy wicker', 'FBI', 'radical groups']
#
# solutionFiles = ['02385.txt', '03212.txt', '03740.txt', '03040.txt',
#                  '03622.txt', '04085.txt', '04080.txt', '01785.txt',
#                  '03435.txt',  '01878.txt', '01030.txt', '01038.txt', '03295.txt']
#
# patino = ['patino', 'edward patino']
#
# PoC = ['Paramurderers of Chaos']
#
header = ['files', 'words']

# banks = wordBank_4filesv2 + wordBank_2385_1785

#solutionDict = get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt')
#terrorCatDict = findWordList('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt', terrorCategoryBank, 1)
#terrorBank = findWordList('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt', terrorWordBank+bioTerrorBank, 3)
#print (terrorBank)
#terrorBank = findWordList('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt', terrorWordBank + bioTerrorBank, 3)
#print len(terrorBank)
#blobDictionaryToCSV(terrorBank, header, 'terrorAndbioterror_files.csv')
files = get_columnFromCSV('terrorAndbioterror_files.csv', 0)
#print files

#allFilesDict= get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt')
#Serialize dictionary for later use
#objectToPickle("allFilesDict.dict.p", allFilesDict)
#allFiles = pickleToObject("allFilesDict.dict.p")
#blobDictionaryToCSV(filterDictionary(allFiles,files), header, 'tb_terrorAndBioterror_files.csv')


#An array that contains an array of words that correspond to each document in the corpus.
#allWords =[remove_stopWords(file.lower().words, stoplist) for file in allFiles]
#objectToPickle("allWords.p", allWords)
#allWords = pickleToObject("allWords.p")
#all_tokens= pickleToObject('all_tokens.p')
#print all_tokens

##Get proper nouns and remove useless words
#bloblistNounWords =[get_ProperNouns(text) for text in bloblist]
#
##lowercase proper nouns
#bloblistLowerNouns = [[noun.lower() for noun in nounlist] for nounlist in bloblistNounWords]
#bloblistLowerNouns = [remove_stopWords(nounlist, stoplist+removalList) for nounlist in bloblistLowerNouns]

####################### WORD BANK GENERATION ###########################
#wordBank_4files_set = set(wordBank_4files)

## GET TF-IDF Scores for 4 bioterrorism articles
#get_tfidfForDict(['03295.txt', '03040.txt', '04085.txt', '03212.txt'], allFilesDict, '4files_tfidf_t3.csv', 3)
#get_tfidfForDict(['03295.txt', '03040.txt', '04085.txt', '03212.txt'], allFilesDict, '4files_tfidf_t5.csv', 5)
#get_tfidfForDict(['03295.txt', '03040.txt', '04085.txt', '03212.txt'], allFilesDict, '4files_tfidf_t8.csv', 8)
#get_tfidfForDict(['03295.txt', '03040.txt', '04085.txt', '03212.txt'], allFilesDict, '4files_tfidf_t10.csv', 10)

## GET SET OF WORDS THAT HAVE TOP TFIDF SCORES FROM FILES
# top3_tfidf = set(get_columnFromCSV('4files_tfidf_t3.csv', 0))
# top5_tfidf = set(get_columnFromCSV('4files_tfidf_t5.csv', 0))
# top8_tfidf = set(get_columnFromCSV('4files_tfidf_t8.csv', 0))
# top10_tfidf = set(get_columnFromCSV('4files_tfidf_t10.csv', 0))
#
# ##PROPER NOUN WORD BANK
# properNoun_Bank = get_ProperNounsWL(bloblist)
#
# ##PROPER NOUN AND NOUN PHRASE WORD BANK
# nnp_nphrase_bank = wordBank_generator(bloblist)
#
# gen_lists = [top10_tfidf, top10_tfidf.union(properNoun_Bank),
#              top10_tfidf.union(properNoun_Bank.union(nnp_nphrase_bank)),
#              top8_tfidf, top8_tfidf.union(properNoun_Bank),
#              top8_tfidf.union(properNoun_Bank.union(nnp_nphrase_bank)),
#              top5_tfidf, top5_tfidf.union(properNoun_Bank),
#              top5_tfidf.union(properNoun_Bank.union(nnp_nphrase_bank)),
#              top3_tfidf, top3_tfidf.union(properNoun_Bank),
#              top3_tfidf.union(properNoun_Bank.union(nnp_nphrase_bank))]
#
# for gen_list in gen_lists:
#     allfiles_from_genWB = findWordListinDict(allFilesDict, gen_list, 5)
#     solfiles_from_genWB = findWordListinDict(solutionDict, gen_list, 5)
#     gl_diff_ml = gen_list.difference(wordBank_4files_set)
#     ml_diff_gl = wordBank_4files_set.difference(gen_list)
#     ml_intersect_gl = wordBank_4files_set.intersection(gen_list)
#  #   print "Generated List: "
#     print gen_list
#    # print str(len(allfiles_from_genWB)) + ' ' + str(len(solfiles_from_genWB)) \
#    #       + ' ' + str(len(gl_diff_ml)) + ' ' + str(len(ml_diff_gl)) + ' '\
#    #       + str(len(ml_intersect_gl)) + ' ' + str(len(gen_list))


#print len(top10_tfidf.difference(wordBank_4files_set))
#print len(wordBank_4files_set.difference(top10_tfidf))
#print len(generated_wordBank)
#print len(wordBank_4files_set)
#print len(solfiles_from_genWB)
#print len(allfiles_from_genWB)


#blobDictionaryToCSV(findWordListinDict(allFilesDict, words, 4), header, "generatedWB_result.csv")

#print len(findWordListinDict(allFilesDict, banks, 3))
#print findWordListinDict(allFilesDict, patino, 1)
#print findWordListinDict(allFilesDict, PoC, 1)
#print len(findWordListinDict(solutionDict, banks, 3))
#blobDictionaryToCSV(findWordListinDict(allFilesDict, wordBank_4files, 3), header, "cassie.csv")


#blobDictionaryToCSV(findWordListinDict(allFilesDict, wordBank_4filesv2, 2),header, "wordBank_4Files_t2.csv")

#print findWordListinDict(solutionDict, wordBank_4filesv2, 2)
#print len(findWordListinDict(solutionDict, wordBank_4filesv2, 2))

#allFiles= get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt')
#terrorCatFiles = get_columnFromCSV('terrorCategory.csv', 0)
#terrorCatv2Dict = filterDictionary(allFiles, terrorCatFiles)
#twbT3 = findWordListinDict(terrorCatv2Dict, terrorWordBank, 10)
#twbT3filesNames = get_columnFromCSV('terrorWordBankT3.csv', 0)
#twbT3Dict = get_filterblobsDictionary('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt', twbTfilesNames)
#get_tfidfForDict(twbT3Dict, "twbT3_tfidf.csv", 10)

#blobDictionaryToCSV(twbT3, header, 'terrorWordBankT3.csv')


#twbT3dict = filterDictionary(allFiles, filesTWBT3)
#blobDictionaryToCSV(twbT3dict, header, 'test2.csv')
#get_tfidfForDict(twbT3dict, "twbT3_tfidf_top3.csv", 3)
#get_tfidf('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt', 'test2.csv', 3)


#terrorCatv2Files=get_fileNamesFromCSV('/Users/susancollins/Google Drive/Draper/Python/9 Dec/terrorCatv2.csv')

#allFiles= get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt')

#blobDictionaryToCSV(allFiles, header, "test2.csv")
#terrorCatv2Dict = filterDictionary(allFiles, terrorCatv2Files)
#print allFiles['00001.txt']

#blobDictionaryToCSV(terrorCatv2Dict,header ,"test.csv")
#twb=findWordListinDict(terrorCatv2Dict, terrorWordBank, 3)
#solFiles = get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt')
#get_tfidfForDict(solFiles, 'test2.csv', 3)
#get_tfidf('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt','terrorCatv2_tfidf.csv', 3)
