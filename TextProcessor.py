from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
from collections import defaultdict
import gc
from collections import Counter
class TextProcessor:
    
    STOPWORDS = set(stopwords.words('english'))
    URL_STOP_WORDS = set(["http", "https", "www", "ftp", "com", "net", "org", "archives", "pdf", "html", "png", "txt", "redirect","web","htm"])
    STEMMER = SnowballStemmer('english')
    REFERENCES_STOP_WORDS = set(["reflist", "refs","em","30em","|","90em","24em","refbegin","refend","cite","author","publisher","ref","title","=","isbn","book","archivedate","archiveurl","accessdate","deadurl","last","first","first1","last1","last2"])
    def __init__(self):
        pass
#         self.track = 0
    
    def removePunctuationsAndDigits(self,tokenList):
        
        tokenList = [re.sub('[^A-Za-z]+', '', token) for token in tokenList]
        
#         for token in tokenList:
#             #gc.disable()
#             re.sub('[^A-Za-z]+', '', token)
#             #gc.enable() 
        return tokenList
    
    def removeStopWords(self,tokenList):
#         cleanTokens = []
        f = lambda t: (t not in TextProcessor.STOPWORDS) and (t not in TextProcessor.URL_STOP_WORDS) and (t not in TextProcessor.REFERENCES_STOP_WORDS)
        cleanTokens = [t for t in tokenList if f(t)==1]
#         for t in tokenList: 
#             #gc.disable()
#             if( (t not in TextProcessor.STOPWORDS) and (t not in TextProcessor.URL_STOP_WORDS) and (t not in TextProcessor.REFERENCES_STOP_WORDS)):
#                 cleanTokens.append(t)
#             #gc.enable()
        return cleanTokens
    
    
    def performStemming(self,tokenList):
#         stemmed = []
        
        stemmed = [TextProcessor.STEMMER.stem(t) for t in tokenList]
#         for t in tokenList:
#             #gc.disable()
#             stemmed.append(TextProcessor.STEMMER.stem(t))
#             #gc.enable()
        return stemmed
    
    
    def cleanTokenList(self,tokenList):
        
        ''' 1. Remove punctuations and digits'''
        tokenList = self.removePunctuationsAndDigits(tokenList)
        
        ''' 2. Remove STOP WORDS'''
        tokenList = self.removeStopWords(tokenList)
        
        '''3. Perform Stemming using SnowBall Stemmer'''
        tokenList = self.performStemming(tokenList)
        
        return tokenList
    
    def tokenize(self,data):
        tokenizedWords = re.findall("\d+|[\w]+",data)
        tokenizedWords = [key for key in tokenizedWords]
        return tokenizedWords
    
    
    def buildWordFreqDict(self,tokenList):
        wordFreqDict = defaultdict(int)
        for t in tokenList:
            #gc.disable()
            wordFreqDict[t]+=1
            #gc.enable()
    
        return wordFreqDict
    
    def cleanTextData(self,data):
        '''
        1. Case Folding
        2. Tokenize
        3. Stop Words Removal
        4. Stemming
        '''
        data = data.lower()
        tokenList = self.tokenize(data)
        '''Now we have a clean token list with all the pre-processing done'''
        tokenList = self.cleanTokenList(tokenList)
        
        wordFreqDict = self.buildWordFreqDict(tokenList)
        return wordFreqDict
        
    
    def processTitle(self, title):
        '''
            Takes in a title string of a document and returns a title-word:freq dictionary
        '''
        titleWordFreqList = self.cleanTextData(title)
        return titleWordFreqList
    
    def externalLinksFromText(self,text):
        refRegExp = r'== ?external links ?==(.*?)\[\['
        external = re.findall(refRegExp,text,flags=re.DOTALL)
        external = self.tokenize(' '.join(external))
        external = self.cleanTokenList(external)
        return self.buildWordFreqDict(external)
    
    
#     def externalLinksFromText(self,text):
#         links=[]
#         lines = text.split("==external links==")
#         if len(lines) > 1:
#             lines = lines[1].split("\n")
#             for i in range(len(lines)):
#                 #gc.disable()
#                 if '* [' in lines[i] or '*[' in lines[i]:
#                     words = lines[i].split(' ')
#                     words = ' '.join(words)
#                     links.append(words)
#                 #gc.enable()
# #         if(len(links)>0):
# #             print(links)
#         tokens = self.tokenize(' '.join(links))
#         tokenList = self.cleanTokenList(tokens)
#         return self.buildWordFreqDict(tokenList)

        
    
#     def referencesFromText2(self,lines,index,text,numberOfLines):
#         references = []
#         i = index
#         
#         if '==external links==' in lines[i] or '== external links ==' in lines[i]:
#             lines = text.split("==references==")
#             if len(lines)<=1:
#                 lines = text.split("== references ==")
#             
#             if(len(lines)>1):
#                 lines = lines[1].split('\n')
#                 while(i<numberOfLines):
#                     if '[[category' in lines[i] or '{{defaultsort' in lines[i] or '==external links==' in lines[i]:
#                         break
#                     words = lines[i].split(' ')
#                     words = ' '.join(words)
#                     references.append(words)
#                     i+=1
#         references = self.tokenize(' '.join(references))
#         references = self.cleanTokenList(references)
#         references =self.buildWordFreqDict(references)
#         return references, i 
    
#     def referencesFromText(self,text):
#         references = []
#         lines = text.split("==references==")
#         
#         if len(lines)<=1:
#             lines = text.split("== references ==")
#         
#         if len(lines)>1:
#             lines = lines[1].split('\n')
#             for i in range(len(lines)):
#                 #gc.disable()
#                 if '[[category' in lines[i] or '{{defaultsort' in lines[i] or '==external links==' in lines[i]:
#                     break;
#                 words = lines[i].split(' ')
#                 words = ' '.join(words)
#                 references.append(words)
#                 #gc.enable()
# #         if len(references)>0:
# #             print(references)
#         
#         references = self.tokenize(' '.join(references))
#         references = self.cleanTokenList(references)
#         return self.buildWordFreqDict(references)

    def referenceFromText(self,text):
        refRegExp = r'== ?references ?==(.*?)=='
        references = re.findall(refRegExp,text,flags=re.DOTALL)
        references = self.tokenize(' '.join(references))
        references = self.cleanTokenList(references)
        return self.buildWordFreqDict(references)
    
    def categoryFromText(self,text):
        catRegExp = r'\[\[category:(.*?)\]\]'
        category = re.findall(catRegExp,text,flags=re.MULTILINE)
        category = self.tokenize(' '.join(category))
        category = self.cleanTokenList(category)
        return self.buildWordFreqDict(category)
#         category = []
#         i = index
#         
#         while(i<numberOfLines):
#             #gc.disable()
#             if '[[category' in lines[i]:
#                 line = text.split("[[category:")
#                 if len(line)>1:
#                     category.extend(line[1:-1])
#                     line[-1]=re.sub(r'\]]','',line[-1])
#                     category.append(line[-1])
#             i+=1
#             #gc.enable()
#         
#         category = self.tokenize(' '.join(category))
#         category = self.cleanTokenList(category)
#         return category, i

    def infoBoxNew(self,text):
        
        infoBox = []
        infoBoxReg = '{{infobox'
        start = text.find()
    
    def extractFieldsFromText(self,text):
        '''
            Extract infoBox and bodyText
        '''
        infoBox = []
        body = []
        category = []
        lines = text.split('\n')
        bodyStart = True
        i=0
        numberOfLines = len(lines)
        while(i<numberOfLines):
            #gc.disable()
            if '{{infobox' in lines[i]:
                countBracket = 0
                info = lines[i].split('{{infobox')[1:]
                infoBox.extend(info)
                #extract nested info  box
                while True:
                    if '{{' in lines[i]:
                        countBracket+=lines[i].count('{{')
                    if '}}' in lines[i]:
                        countBracket-=lines[i].count('}}')
                    if countBracket<=0:
                        break
                    i+=1
                    if i<numberOfLines:
                        infoBox.append(lines[i])
                    else:
                        break
            elif bodyStart:
                if '[[category' in lines[i] or '==external links==' in lines[i] or '== external links ==' in lines[i]:
                    bodyStart = False
                    break
                else:
                    body.append(lines[i])
#             else:
#                 category, index = self.categoryFromText(text)
#                 break
            i+=1
            #gc.enable()
        body = self.tokenize(' '.join(body))
        body = self.cleanTokenList(body)
        body = self.buildWordFreqDict(body)
        
        infoBox = self.tokenize(' '.join(infoBox))
        infoBox = self.cleanTokenList(infoBox)
        infoBox = self.buildWordFreqDict(infoBox)
        
#         category = self.buildWordFreqDict(category)
        
        return body, infoBox
    
    def getInfo(self,text):
        infoRegExp = r'{{infobox(.*?)}}'
        infobox = re.findall(infoRegExp,text,re.DOTALL)
        infoBox = self.tokenize(' '.join(infobox))
        infoBox = self.cleanTokenList(infoBox)
        infoBox = self.buildWordFreqDict(infoBox)
        print(infobox)
        
    def processText(self,text):
        
#         self.track+=1
        '''1. Case Folding'''
        #text = text.lower()
        # self.getInfo(text)
        externalLinks = self.externalLinksFromText(text)
        references = self.referenceFromText(text)
        text = text.replace('_','').replace(',','')
        category = self.categoryFromText(text)
        body, infoBox = self.extractFieldsFromText(text)
#         if(self.track %1000 ==0):
#             print("processed: ",self.track)
        return body, infoBox, category, externalLinks, references
        
        
        
        
        
        
        
        
        
        
        
