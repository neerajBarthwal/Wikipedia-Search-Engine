from collections import defaultdict
import threading
import heapq
import os

class FileHandler:
    
    INDEX_FILE_NUMBER_AFTER_MERGE = 0
    NUMBER_OF_WORDS = 0
    OFFSET_SIZE = 0
    
    def __init__(self):
        self.titleIndex = []
        self.bodyIndex = []
        self.infoBoxIndex = []
        self.categoryIndex = []
        self.externalLinkIndex = []
        self.referenceIndex = []
        self.titleLookup = []
        self.bodyLookup = []
        self.infoBoxLookup = []
        self.categoryLookup = []
        self.externalLinkLookup = []
        self.referenceLookup = []
        self.heap = []
    
    def writeIndexesToDisk(self,wordsOfIndex,rootDir,title,body,infobox,category,externalLink,references):
        
        prevTitleLen = 0
        prevBodyLen = 0
        prevInfoboxLen = 0
        prevCategoryLen = 0
        prevExtLen = 0
        prevRefLen = 0
        
        self.titleIndex = []
        self.bodyIndex = []
        self.infoBoxIndex = []
        self.categoryIndex = []
        self.externalLinkIndex = []
        self.referenceIndex = []
        self.titleLookup = []
        self.bodyLookup = []
        self.infoBoxLookup = []
        self.categoryLookup = []
        self.externalLinkLookup = []
        self.referenceLookup = []
        
        for word in wordsOfIndex:
            
            if word in title:
                entry = word+' '
                postings = title[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(title[word][docId])+' '
                self.titleLookup.append(str(prevTitleLen)+' '+str(len(postingsSortedByTF)))
                prevTitleLen+= len(entry.encode('utf-8'))+1
                self.titleIndex.append(entry)
            
            if word in body:
                entry = word+' '
                postings = body[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(body[word][docId])+' '
                self.bodyLookup.append(str(prevBodyLen)+' '+str(len(postingsSortedByTF)))
                prevBodyLen+= len(entry.encode('utf-8'))+1
                self.bodyIndex.append(entry)
                    
            if word in infobox:
                entry = word+' '
                postings = infobox[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(infobox[word][docId])+' '
                self.infoBoxLookup.append(str(prevInfoboxLen)+' '+str(len(postingsSortedByTF)))
                prevInfoboxLen+= len(entry.encode('utf-8'))+1
                self.infoBoxIndex.append(entry)
                
            if word in category:
                entry = word+' '
                postings = category[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(category[word][docId])+' '
                self.categoryLookup.append(str(prevCategoryLen)+' '+str(len(postingsSortedByTF)))
                prevCategoryLen+= len(entry.encode('utf-8'))+1
                self.categoryIndex.append(entry)
                
            if word in externalLink:
                entry = word+' '
                postings = externalLink[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(externalLink[word][docId])+' '
                self.externalLinkLookup.append(str(prevExtLen)+' '+str(len(postingsSortedByTF)))
                prevExtLen+= len(entry.encode('utf-8'))+1
                self.externalLinkIndex.append(entry)
                    
            if word in references:
                entry = word+' '
                postings = references[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(references[word][docId])+' '
                self.referenceLookup.append(str(prevRefLen)+' '+str(len(postingsSortedByTF)))
                prevRefLen += len(entry.encode('utf-8'))+1
                self.referenceIndex.append(entry)
                
#         try:
#             if os.path.getsize(rootDir+'/body'+str(FileHandler.INDEX_FILE_NUMBER_AFTER_MERGE)+'.txt') > 20485760:
#                 FileHandler.INDEX_FILE_NUMBER_AFTER_MERGE+=1
#         except:
#             pass
                
        titleThread = MultithreadedWriter(rootDir,self.titleIndex,self.titleLookup,"title")
        bodyThread = MultithreadedWriter(rootDir,self.bodyIndex,self.bodyLookup,"body")
        infoBoxThread = MultithreadedWriter(rootDir,self.infoBoxIndex,self.infoBoxLookup,"infobox")
        categoryThread = MultithreadedWriter(rootDir,self.categoryIndex,self.categoryLookup,"category")
        externalThread = MultithreadedWriter(rootDir,self.externalLinkIndex,self.externalLinkLookup,"externalLink")
        referenceThread = MultithreadedWriter(rootDir,self.referenceIndex,self.referenceLookup,"references")
         
        titleThread.start()
        bodyThread.start()
        infoBoxThread.start()
        categoryThread.start()
        externalThread.start()
        referenceThread.start()
         
        titleThread.join()
        bodyThread.join()
        infoBoxThread.join()
        categoryThread.join()
        externalThread.join()
        referenceThread.join()
        

        
    def mergeIndexes(self,rootDir,totalIndexFiles):
        
        indexFileDescriptor = {}
        topOfIndexFile = {}
        wordsInIndexFile = {}
        isOpen = [0] * totalIndexFiles
        finalIndex = defaultdict(list)
        self.heap = []
        FileHandler.OFFSET_SIZE = 0
        print("Starting merge process")
        for i in range(0,totalIndexFiles):
            indexFileName = rootDir+'/index'+str(i)+'.txt'
            indexFileDescriptor[i] = open(indexFileName,'r')
            isOpen[i] = 1
            topOfIndexFile[i] = indexFileDescriptor[i].readline().strip()
            wordsInIndexFile[i] = topOfIndexFile[i].split(' ')
            if wordsInIndexFile[i][0] not in self.heap:
                heapq.heappush(self.heap, wordsInIndexFile[i][0])
        print("Initial loading done.")
        while any(isOpen)==1:
            currentWord = heapq.heappop(self.heap)
            FileHandler.NUMBER_OF_WORDS+=1
            for i in range(0,totalIndexFiles):
                if isOpen[i]==1:
                    if wordsInIndexFile[i][0] == currentWord:
                        finalIndex[currentWord].extend(wordsInIndexFile[i][1:])
                        if FileHandler.NUMBER_OF_WORDS%50000==0:
                            #prevFileNumber = FileHandler.INDEX_FILE_NUMBER_AFTER_MERGE
                            self.createIndexByFields(rootDir, finalIndex)
                            FileHandler.INDEX_FILE_NUMBER_AFTER_MERGE+=1
                            finalIndex = defaultdict(list)
                            print("Merge Word count: ", FileHandler.NUMBER_OF_WORDS)
                            #if prevFileNumber!=FileHandler.INDEX_FILE_NUMBER_AFTER_MERGE:
                            #   finalIndex = defaultdict(list)
                            
                        topOfIndexFile[i] = indexFileDescriptor[i].readline().strip()
                        if topOfIndexFile[i]=='':
                            isOpen[i] = 0
                            indexFileDescriptor[i].close()
                            os.remove(rootDir+'/index'+str(i)+'.txt')
                        else:
                            wordsInIndexFile[i] = topOfIndexFile[i].split(' ')   
                            if wordsInIndexFile[i][0] not in self.heap:
                                heapq.heappush(self.heap, wordsInIndexFile[i][0])
        self.createIndexByFields(rootDir, finalIndex)
                    
    def createIndexByFields(self,rootDir,finalIndex):
        
        title = defaultdict(dict)
        infobox = defaultdict(dict)
        body = defaultdict(dict)
        category = defaultdict(dict)
        references = defaultdict(dict)
        externalLink = defaultdict(dict)
        vocabulary = []
        vocabularyOffset = []
        
        wordsInIndex = sorted(finalIndex.keys())
        for word in wordsInIndex:
            postings = finalIndex[word]
            entryFound = False
            for i in range(0,len(postings),7):
                docId = postings[i]
                
                if postings[i+1]!='0.0':
                    title[word][docId] = float(postings[i+1])
                    entryFound = True       
                if postings[i+2]!='0.0':
                    body[word][docId] = float(postings[i+2])
                    entryFound = True
                if postings[i+3]!='0.0':
                    infobox[word][docId] = float(postings[i+3])
                    entryFound = True
                if postings[i+4]!='0.0':
                    category[word][docId] = float(postings[i+4])
                    entryFound = True
                if postings[i+5]!='0.0':
                    externalLink[word][docId] = float(postings[i+5])
                    entryFound = True
                if postings[i+6]!='0.0':
                    references[word][docId] = float(postings[i+6])
                    entryFound = True
                
            if entryFound == True:
                entry = word+' '+str(FileHandler.INDEX_FILE_NUMBER_AFTER_MERGE)+' '+str(len(postings)/7)
                vocabulary.append(entry)
                vocabularyOffset.append(str(FileHandler.OFFSET_SIZE))
                FileHandler.OFFSET_SIZE = FileHandler.OFFSET_SIZE + len(entry.encode('utf-8'))+1
                    
        #self.writeIndexesToDisk(wordsInIndex,rootDir,title,body,infobox,category,externalLink,references)
        prevTitleLen = 0
        prevBodyLen = 0
        prevInfoboxLen = 0
        prevCategoryLen = 0
        prevExtLen = 0
        prevRefLen = 0
        
        self.titleIndex = []
        self.bodyIndex = []
        self.infoBoxIndex = []
        self.categoryIndex = []
        self.externalLinkIndex = []
        self.referenceIndex = []
        self.titleLookup = []
        self.bodyLookup = []
        self.infoBoxLookup = []
        self.categoryLookup = []
        self.externalLinkLookup = []
        self.referenceLookup = []
        
        for word in wordsInIndex:
            
            if word in title:
                entry = word+' '
                postings = title[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(title[word][docId])+' '
                self.titleLookup.append(str(prevTitleLen)+' '+str(len(postingsSortedByTF)))
                prevTitleLen+= len(entry.encode('utf-8'))+1
                self.titleIndex.append(entry)
            
            if word in body:
                entry = word+' '
                postings = body[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(body[word][docId])+' '
                self.bodyLookup.append(str(prevBodyLen)+' '+str(len(postingsSortedByTF)))
                prevBodyLen+= len(entry.encode('utf-8'))+1
                self.bodyIndex.append(entry)
                    
            if word in infobox:
                entry = word+' '
                postings = infobox[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(infobox[word][docId])+' '
                self.infoBoxLookup.append(str(prevInfoboxLen)+' '+str(len(postingsSortedByTF)))
                prevInfoboxLen+= len(entry.encode('utf-8'))+1
                self.infoBoxIndex.append(entry)
                
            if word in category:
                entry = word+' '
                postings = category[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(category[word][docId])+' '
                self.categoryLookup.append(str(prevCategoryLen)+' '+str(len(postingsSortedByTF)))
                prevCategoryLen+= len(entry.encode('utf-8'))+1
                self.categoryIndex.append(entry)
                
            if word in externalLink:
                entry = word+' '
                postings = externalLink[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(externalLink[word][docId])+' '
                self.externalLinkLookup.append(str(prevExtLen)+' '+str(len(postingsSortedByTF)))
                prevExtLen+= len(entry.encode('utf-8'))+1
                self.externalLinkIndex.append(entry)
                    
            if word in references:
                entry = word+' '
                postings = references[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(references[word][docId])+' '
                self.referenceLookup.append(str(prevRefLen)+' '+str(len(postingsSortedByTF)))
                prevRefLen += len(entry.encode('utf-8'))+1
                self.referenceIndex.append(entry)
                
#         try:
#             if os.path.getsize(rootDir+'/body'+str(FileHandler.INDEX_FILE_NUMBER_AFTER_MERGE)+'.txt') > 20485760:
#                 FileHandler.INDEX_FILE_NUMBER_AFTER_MERGE+=1
#         except:
#             pass
                
        titleThread = MultithreadedWriter(rootDir,self.titleIndex,self.titleLookup,"title")
        bodyThread = MultithreadedWriter(rootDir,self.bodyIndex,self.bodyLookup,"body")
        infoBoxThread = MultithreadedWriter(rootDir,self.infoBoxIndex,self.infoBoxLookup,"infobox")
        categoryThread = MultithreadedWriter(rootDir,self.categoryIndex,self.categoryLookup,"category")
        externalThread = MultithreadedWriter(rootDir,self.externalLinkIndex,self.externalLinkLookup,"externalLink")
        referenceThread = MultithreadedWriter(rootDir,self.referenceIndex,self.referenceLookup,"references")
         
        titleThread.start()
        bodyThread.start()
        infoBoxThread.start()
        categoryThread.start()
        externalThread.start()
        referenceThread.start()
         
        titleThread.join()
        bodyThread.join()
        infoBoxThread.join()
        categoryThread.join()
        externalThread.join()
        referenceThread.join()
        
        with open(rootDir+"/vocabulary.txt","a") as vocabHandle:
            vocabHandle.write('\n'.join(vocabulary)+'\n')
            
        with open(rootDir+"/vocabularyLookup.txt","a") as vocabHandle:
            vocabHandle.write('\n'.join(vocabularyOffset)+'\n')
            
    def writeIndexToDisk(self,rootDir,index,indexFileNumber):
        
        #sort the index on terms obtained from corpus
        words = sorted(index)
        toIndexFile = [str(word)+' '+' '.join(index[word]) for word in words]
         
        fileOnDisk = rootDir+'/index'+str(indexFileNumber)+'.txt'
        toIndexFile = '\n'.join(toIndexFile)
         
        with open(fileOnDisk,'w') as indexHandle:
            indexHandle.write(toIndexFile)
            
    def writeDocIdTitleMappingToDisk(self,rootDir,docIdTitleMapping):
      
        toTitleFile = [str(docId)+' '+title for docId, title in docIdTitleMapping.items()]
         
        toTitleFile = '\n'.join(toTitleFile)
         
        fileOnDisk = rootDir+'/title.txt'
        with open(fileOnDisk,'a') as titleFileHandle:
            titleFileHandle.write(toTitleFile+'\n')
        


class MultithreadedWriter(threading.Thread):
    
    def __init__(self,path,data,lookup,fileName):
        threading.Thread.__init__(self)
        self.path = path
        self.data = data
        self.lookup = lookup
        self.fileName = fileName
    
    def run(self):
        fileOnDisk = self.path+'/'+self.fileName+str(FileHandler.INDEX_FILE_NUMBER_AFTER_MERGE)+'.txt'
       
        self.data = '\n'.join(self.data)
        with open(fileOnDisk,'w') as indexHandle:
            indexHandle.write(self.data)
        
        fileOnDisk = self.path+'/'+self.fileName+'lookup'+str(FileHandler.INDEX_FILE_NUMBER_AFTER_MERGE)+'.txt'
        self.lookup = '\n'.join(self.lookup)
        with open(fileOnDisk,'w') as indexHandle:
            indexHandle.write(self.lookup) 
