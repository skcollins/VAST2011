__author__ = 'susancollins'

import ner
from tfidf import *

solutionDict = get_docDictionary('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt')


tagger = ner.SocketNER(host='localhost', port=8080)
for doc in solutionDict.values():
    doc_ner = tagger.json_entities(doc)
    print doc_ner

print tb("hello i can't help it!").words

