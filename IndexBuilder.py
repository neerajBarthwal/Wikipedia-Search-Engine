from FileHandler import FileHandler
import gc
from _collections import defaultdict

class IndexBuilder:
    
    INDEX_ROOT_DIR = "/home/neeraj/IRE"
    
    def __init__(self):
        self.index = defaultdict(list)
        self.vocab = []
        self.indexFileNumber = 0
        self.writeCounter = 0 
        self.fileIO = FileHandler()
        
    def getVocabForDocument(self,titleTermFreq,bodyTermFreq,infoBoxTermFreq,categoryTermFreq,externalLinksTermFreq,referencesTermFreq):
        
        titleTerms = list(titleTermFreq.keys())
        bodyTerms = list(bodyTermFreq.keys())
        infoBoxTerms = list(infoBoxTermFreq.keys())
        categoryTerms = list(categoryTermFreq.keys())
        externalLinksTerms = list(externalLinksTermFreq.keys())
        referencesTerms  = list(referencesTermFreq.keys())
        
        allWords = []
        
        allWords.extend(titleTerms)
        allWords.extend(bodyTerms)
        allWords.extend(infoBoxTerms)
        allWords.extend(categoryTerms)
        allWords.extend(externalLinksTerms)
        allWords.extend(referencesTerms)
        
        uniqueWords = set(allWords)
        return list(uniqueWords)
    
    def makeIndexEntryForWord(self,docId,t,b,i,c,e,r):
        entry = str(docId)+' '+str(t)+' '+str(b)+' '+str(i)+' '+str(c)+' '+str(e)+' '+str(r)
        return entry
    
    def buildIndex(self,docId,titleTermFreq,bodyTermFreq,infoBoxTermFreq,categoryTermFreq,externalLinksTermFreq,referencesTermFreq, docIdTitleMapping):
        
        
        """
        Creates an entry for each wikipedia page in an in memory data structure 'index'
        dict of {word: freq} of [title, text, infoBox, category, externalLink, references]
        
        In memory index is then written to the disk for every 5000 files.
       """
        
        self.vocab = self.getVocabForDocument(titleTermFreq, bodyTermFreq, infoBoxTermFreq, categoryTermFreq, externalLinksTermFreq, referencesTermFreq)
        
        #t,b,i,c,e,r = len(titleTermFreq), len(bodyTermFreq), len(infoBoxTermFreq), len(categoryTermFreq), len(externalLinksTermFreq), len(referencesTermFreq)
        for word in self.vocab:
            gc.disable()
            entry = self.makeIndexEntryForWord(docId,titleTermFreq[word],bodyTermFreq[word],infoBoxTermFreq[word],
                                               categoryTermFreq[word],externalLinksTermFreq[word],
                                               referencesTermFreq[word])
            self.index[word].append(entry)
            gc.enable()
        
            
    def buildIndexBulk(self,processedTextBulk,processedTitleBulk,docIdTitleMapping):
        
        for docId in processedTextBulk.keys():
            gc.disable()
            bodyTermFreq = processedTextBulk[docId]['b']
            infoBoxTermFreq = processedTextBulk[docId]['i']
            categoryTermFreq = processedTextBulk[docId]['c']
            externalTermFreq = processedTextBulk[docId]['e']
            referenceTermFreq = processedTextBulk[docId]['r']
            titleTermFreq = processedTitleBulk[docId]
            self.buildIndex(docId, titleTermFreq, bodyTermFreq, infoBoxTermFreq, categoryTermFreq, 
                            externalTermFreq, referenceTermFreq, docIdTitleMapping)
            gc.enable()
            
        self.fileIO.writeIndexToDisk(IndexBuilder.INDEX_ROOT_DIR,self.index, self.indexFileNumber)
        self.fileIO.writeDocIdTitleMappingToDisk(IndexBuilder.INDEX_ROOT_DIR,docIdTitleMapping)
        self.indexFileNumber+=1
            
        
