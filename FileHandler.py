import bz2
import gc

class FileHandler:
    
    def __init__(self):
        pass
    
    def writeIndexToDisk(self,rootDir,index,indexFileNumber):
        # toIndexFile = []
        
        #sort the index on terms obtained from corpus
        words = sorted(index)
        
        toIndexFile = [str(word)+' '+str(index[word]) for word in words]
        
        
#         for word in words:
#             #gc.disable()
#             posting = index[word]
#             entry = str(word)+' '+str(posting)
#             toIndexFile.append(entry)
#             #gc.enable()
        #write to disk (TODO: create threads for writing)
        
        fileOnDisk = rootDir+'/index'+str(indexFileNumber)+'.txt.bz2'
        toIndexFile = '\n'.join(toIndexFile)
        
        fnew = rootDir+'/index'+str(indexFileNumber)+'.txt'
        
        ''' If mode is 'w', 'x' or 'a', compresslevel can be a number between 1
        and 9 specifying the level of compression: 1 produces the least
        compression, and 9 (default) produces the most compression.'''
        with bz2.BZ2File(fileOnDisk,'wb') as indexHandle:
            indexHandle.write(toIndexFile.encode(encoding='utf_8'))
            
#         with open(fnew,'w') as f:
#             f.write(toIndexFile)
         
    def writeDocIdTitleMappingToDisk(self,rootDir,docIdTitleMapping):
        
        toTitleFile = [str(docId)+' '+title for docId, title in docIdTitleMapping.items()]
        
#         toTitleFile = 
#         
#         for docId, title in docIdTitleMapping.items():
#             #gc.disable()
#             entry = str(docId)+' '+title
#             toTitleFile.append(entry)
#             #gc.enable()
        toTitleFile = '\n'.join(toTitleFile)
        
        fileOnDisk = rootDir+'/title.txt'
        with open(fileOnDisk,'ab') as titleFileHandle:
            titleFileHandle.write(toTitleFile.encode(encoding='utf_8'))
         
#         fileOnDisk = rootDir+'/title1.txt'
#         with open(fileOnDisk,'a') as titleFileHandle:
#             titleFileHandle.write(toTitleFile)          
        