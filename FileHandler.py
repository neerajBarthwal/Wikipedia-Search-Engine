import bz2
from collections import defaultdict
import threading
import path
import json

class FileHandler:
    
    
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
    
    
    def writeIndexesToDisk(self,wordsOfIndex,rootDir,title,body,infobox,category,externalLink,references):
        
        prevTitleLen = 0
        prevBodyLen = 0
        prevInfoboxLen = 0
        prevCategoryLen = 0
        prevExtLen = 0
        prevRefLen = 0
        
        
        for word in wordsOfIndex:
            
            if word in title:
                entry = word+' '
                postings = title[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(title[word][docId])+' '
                self.titleLookup.append(str(prevTitleLen)+' '+str(len(postingsSortedByTF)))
                prevTitleLen = len(entry)+1
                self.titleIndex.append(entry)
            
            if word in body:
                entry = word+' '
                postings = body[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(body[word][docId])+' '
                self.bodyLookup.append(str(prevBodyLen)+' '+str(len(postingsSortedByTF)))
                prevBodyLen = len(entry)+1
                self.bodyIndex.append(entry)
                    
            if word in infobox:
                entry = word+' '
                postings = infobox[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(infobox[word][docId])+' '
                self.infoBoxLookup.append(str(prevInfoboxLen)+' '+str(len(postingsSortedByTF)))
                prevInfoboxLen = len(entry)+1
                self.infoBoxIndex.append(entry)
                
            if word in category:
                entry = word+' '
                postings = category[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(category[word][docId])+' '
                self.categoryLookup.append(str(prevCategoryLen)+' '+str(len(postingsSortedByTF)))
                prevCategoryLen = len(entry)+1
                self.categoryIndex.append(entry)
                
            if word in externalLink:
                entry = word+' '
                postings = externalLink[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(externalLink[word][docId])+' '
                self.externalLinkLookup.append(str(prevExtLen)+' '+str(len(postingsSortedByTF)))
                prevExtLen = len(entry)+1
                self.externalLinkIndex.append(entry)
                    
            if word in references:
                entry = word+' '
                postings = references[word]
                postingsSortedByTF = sorted(postings, key = postings.get, reverse=True)
                for docId in postingsSortedByTF:
                    entry+=docId+' '+str(references[word][docId])+' '
                self.referenceLookup.append(str(prevRefLen)+' '+str(len(postingsSortedByTF)))
                prevRefLen = len(entry)+1
                self.referenceIndex.append(entry)
                
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
    
                    
    def createIndexByFields(self,rootDir,index,wordsOfIndex):
        title = defaultdict(dict)
        infobox = defaultdict(dict)
        body = defaultdict(dict)
        category = defaultdict(dict)
        references = defaultdict(dict)
        externalLink = defaultdict(dict)
                
        for word in wordsOfIndex:
            postings = index[word]
            
            for entry in postings:
                entry = entry.split(' ')
                docId = entry[0]
                
                if entry[1]!='0':
                    title[word][docId] = int(entry[1])
                if entry[2]!='0':
                    body[word][docId] = int(entry[2])
                if entry[3]!='0':
                    infobox[word][docId] = int(entry[3])
                if entry[4]!='0':
                    category[word][docId] = int(entry[4])
                if entry[5]!='0':
                    externalLink[word][docId] = int(entry[5])
                if entry[6]!='0':
                    references[word][docId] = int(entry[6])
                          
        with bz2.BZ2File(rootDir+'/titleIndex.txt.bz2', 'wb') as indexHandle:
            indexHandle.write(str(title).encode(encoding='utf_8'))
        
        with bz2.BZ2File(rootDir+'/bodyIndex.txt.bz2', 'wb') as indexHandle:
            indexHandle.write(str(body).encode(encoding='utf_8', errors='strict'))
             
        with bz2.BZ2File(rootDir+'/categoryIndex.txt.bz2', 'wb') as indexHandle:
            indexHandle.write(str(category).encode(encoding='utf_8', errors='strict'))
            
        with bz2.BZ2File(rootDir+'/infoboxIndex.txt.bz2', 'wb') as indexHandle:
            indexHandle.write(str(infobox).encode(encoding='utf_8', errors='strict'))
            
        with bz2.BZ2File(rootDir+'/externalIndex.txt.bz2', 'wb') as indexHandle:
            indexHandle.write(str(externalLink).encode(encoding='utf_8', errors='strict'))
        
        with bz2.BZ2File(rootDir+'/referenceIndex.txt.bz2', 'wb') as indexHandle:
            indexHandle.write(str(references).encode(encoding='utf_8', errors='strict'))
                    
        #self.writeIndexesToDisk(wordsOfIndex,rootDir,title,body,infobox,category,externalLink,references)
            
    def writeIndexToDisk(self,rootDir,index,indexFileNumber):
        # toIndexFile = []
        
        
        #sort the index on terms obtained from corpus
        words = sorted(index)
        self.createIndexByFields(rootDir, index, wordsOfIndex=words)
#         toIndexFile = [str(word)+' '+' '.join(index[word]) for word in words]
#         
#         #write to disk (TODO: create threads for writing)
#         fileOnDisk = rootDir+'/index'+str(indexFileNumber)+'.txt.bz2'
#         toIndexFile = '\n'.join(toIndexFile)
#         
#         ''' If mode is 'w', 'x' or 'a', compresslevel can be a number between 1
#         and 9 specifying the level of compression: 1 produces the least
#         compression, and 9 (default) produces the most compression.'''
#         with bz2.BZ2File(fileOnDisk,'wb') as indexHandle:
#             indexHandle.write(toIndexFile.encode(encoding='utf_8'))
            

         
    def writeDocIdTitleMappingToDisk(self,rootDir,docIdTitleMapping):
        
        with bz2.BZ2File(rootDir+'/title.txt.bz2', 'wb') as indexHandle:
            indexHandle.write(str(docIdTitleMapping).encode(encoding='utf_8', errors='strict'))
        
#         with open(rootDir+'/title.txt', 'w') as file:
#             file.write(json.dumps(docIdTitleMapping))
        
#         toTitleFile = [str(docId)+' '+title for docId, title in docIdTitleMapping.items()]
#         
#         toTitleFile = '\n'.join(toTitleFile)
#         
#         fileOnDisk = rootDir+'/title.txt'
#         with open(fileOnDisk,'ab') as titleFileHandle:
#             titleFileHandle.write(toTitleFile.encode(encoding='utf_8'))
        


class MultithreadedWriter(threading.Thread):
    
    def __init__(self,path,data,lookup,fileName):
        threading.Thread.__init__(self)
        self.path = path
        self.data = data
        self.lookup = lookup
        self.fileName = fileName
    
    def run(self):
        fileOnDisk = self.path+'/'+self.fileName+'.txt.bz2'
        ''' If mode is 'w', 'x' or 'a', compresslevel can be a number between 1
        and 9 specifying the level of compression: 1 produces the least
        compression, and 9 (default) produces the most compression.'''
        self.data = '\n'.join(self.data)
        with bz2.BZ2File(fileOnDisk,'wb') as indexHandle:
            indexHandle.write(self.data.encode(encoding='utf_8'))
        
        fileOnDisk = self.path+'/'+self.fileName+'lookup.txt.bz2'
        self.lookup = '\n'.join(self.lookup)
        with bz2.BZ2File(fileOnDisk,'wb') as indexHandle:
            indexHandle.write(self.lookup.encode(encoding='utf_8'))




   