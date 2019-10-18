import re
from collections import defaultdict
from PorterStemmer import PorterStemmer
from TextProcessor import TextProcessor
import time
import sys
import math
import path

vocabularyLookup = []
titleOffset = []

stemmer = PorterStemmer()
txtProcessor = TextProcessor()
fieldWeights = {'title':0.4,'body':0.2,'infobox':0.1,'category':0.1,'references':0.1,'externalLink':0.1}

def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries


def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            for line in output:
                file.write(line.strip() + '\n')
            file.write('\n')
            
            
def findTitleByDocId(low, high, docId, titleFileHandle):
        
    while low<=high:
        mid = int(low + (high-low)/2)
        #print(titleOffset[mid])
        
        titleFileHandle.seek(titleOffset[mid])
        
        entry = titleFileHandle.readline().strip().split(' ')
        
        if(int(entry[0])==int(docId)):
            return entry[1:]
        elif(int(docId)>int(entry[0])):
            low = mid+1
        else:
            high = mid-1
        
    return []

def ranking(postingsList,documentFrequency,numberOfFiles):
    
    documentList, idfOfWord = defaultdict(float), defaultdict(float)
    
    for word in documentFrequency.keys():
        idfOfWord[word] = math.log((float(numberOfFiles)/(float(documentFrequency[word]) + 1)))
    
    for word in postingsList:
        fieldPostingList = postingsList[word]
        for field in fieldPostingList.keys():
            if len(field)>0:
                postingList = fieldPostingList[field]
                factor = fieldWeights[field]
                for i in range(0, len(postingList), 2):
                    documentList[postingList[i]] += float(postingList[i+1]) * idfOfWord[word] * factor
                    
    return documentList


def searchFileNumber(low, high, word, offset,indexFileHandle):
    
    while low<=high:
        mid = int(low + (high-low)/2)
       
        indexFileHandle.seek(offset[mid])
        currentWord = indexFileHandle.readline().strip().split(' ')
        #print(low, high, mid, currentWord, offset[mid])
        if word == currentWord[0]:
            return currentWord[1:],mid
        elif word > currentWord[0]:
            low = mid+1
        else:
            high = mid-1
    return [],-1

def searchIndexForPostingsList(path_to_index,fieldName,indexFileNumber,word):
    fieldOffset = []
    docFreq = []
    
    #open the index file
    indexFileHandle = open(path_to_index+'/'+fieldName+str(indexFileNumber)+'.txt','r')
    
    #load the corresponding offset file
    with open(path_to_index+'/'+fieldName+'lookup'+str(indexFileNumber)+'.txt','r') as offsetHandle:
        for line in offsetHandle:
            entry = line.strip().split(' ')
            fieldOffset.append(int(entry[0]))
            docFreq.append(int(entry[1]))
    
    docList, mid = searchFileNumber(0,len(fieldOffset),word,fieldOffset,indexFileHandle)
    
    return docList, docFreq[mid]

def processQuery(path_to_index, queryTermToFieldMap, vocabularyHandle):
    
    postingsList = defaultdict(dict)
    documentFrequency = defaultdict(int)

    vocabLen = len(vocabularyLookup)
    for word in queryTermToFieldMap.keys():
        fileList,_ = searchFileNumber(0,vocabLen,word,vocabularyLookup,vocabularyHandle)
        if len(fileList)>0:
            indexFileNumber = fileList[0]
            #documentFrequency[word] = fileList[1]
            for fieldName in queryTermToFieldMap[word]:
                #print(indexFileNumber,word)
                documentList, docFreq = searchIndexForPostingsList(path_to_index,fieldName,indexFileNumber,word)
                postingsList[word][fieldName] = documentList
                documentFrequency[word]+=docFreq
    return postingsList, documentFrequency
         
def search(path_to_index, queries,vocabularyHandle):
    '''Write your code here'''
    outputs = []
    queries = ''.join(queries).split('\n')
    for query in queries:
        query = query.lower()
        query = query.strip().split(' ')
        queryTermToFieldMap = defaultdict(list)
        for word in query:
            if re.search(r'[title|body|infobox|category|ref|ext]{1,}:', word):
                entry = word.split(':')
                field = entry[0]
                if field=='ref':
                    field = 'references'
                if field == 'ext':
                    field = 'externalLink'
                term = entry[1]
                term = txtProcessor.cleanTextData(''.join(term))
                term = ''.join(term)
                queryTermToFieldMap[term].append(field)
                
            else:
                fields = ['title','body','infobox','category','references','externalLink']
                term = txtProcessor.cleanTextData(''.join(word))
                term = ''.join(term)
                queryTermToFieldMap[term].extend(fields)
            
        
        postingsList, documentFrequency = processQuery(path_to_index, queryTermToFieldMap,vocabularyHandle)
        
        with open(path_to_index+'/numberOfFiles.txt','r') as f:
            numberOfFiles = int(f.read().strip())
            
        results = ranking(postingsList,documentFrequency,numberOfFiles)
        
        if len(results)>0:
            top_ten_docs = sorted(results, key=results.get, reverse=True)[:10]
            titleFile = open(path_to_index + '/title.txt','r')
            output = []
            for docid in top_ten_docs:
                title = findTitleByDocId(0, len(titleOffset), docid, titleFile)
                output.append(' '.join(title))
            outputs.append(output)
    return outputs

def performPreProcessing(path_to_index):
    
    #Load the vocabulary lookup file
    with open(path_to_index+'/vocabularyLookup.txt','r') as vocabLookupHandle:
        for line in vocabLookupHandle:
            vocabularyLookup.append(int(line.strip()))

    #Load the title lookup file
    with open(path_to_index+'/titleOffset.txt','r') as titleOffsetHandle:
        for line in titleOffsetHandle:
            titleOffset.append(int(line.strip()))
        
def main():
    path_to_index = '/home/neeraj/IRE/run/index'#sys.argv[1] #index folder
    if path_to_index[-1]=='/':
        path_to_index = path_to_index[:-1]
    #testfile = '/home/aman/neeraj/run/queryfile' #sys.argv[2]    # query file
    #path_to_output ='/home/aman/neeraj/run/output.txt' # sys.argv[3] 
    
    performPreProcessing(path_to_index)
     
    vocabularyHandle = open(path_to_index+'/vocabulary.txt')

    #queries = read_file(testfile)
    print("Type \'quit\' to exit.")
    while True:
        print("Search Here: ",end="")
        input_query  = input()
        if input_query.lower() == "quit":
            sys.exit(0)  
        queries = []
        queries.append(input_query)
        startTime= time.clock()    
        outputs = search(path_to_index, queries,vocabularyHandle)
        print()
        print("========++++++RESULTS+++++++======")
        for result in outputs:
            for title in result:
                print(title)
        stopTime = time.clock()
        print("\ntime:", stopTime - startTime,"seconds")
        print()
    #write_file(outputs, path_to_output)


if __name__ == '__main__':
    #startTime= time.clock()
    main()
    #stopTime = time.clock()
    #print(stopTime - startTime) 
