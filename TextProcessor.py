from nltk.corpus import stopwords
import re
from collections import defaultdict
import gc
from PorterStemmer import PorterStemmer

class TextProcessor:
    
    STEMMER = PorterStemmer() 
    STOPWORDS = set(stopwords.words('english'))
    URL_STOP_WORDS = set(["http", "https", "www", "ftp", "com", "net", "org", "archives", "pdf", "html", "png", "txt", "redirect","web","htm","infobox","defaultsort"])
    REFERENCES_STOP_WORDS = set(["reflist","infobox", "refs","em","30em","|","90em","24em","refbegin","refend","cite","author","publisher","ref","title","=","isbn","book","archivedate","archiveurl","accessdate","deadurl","last","first","first1","last1","last2"," ",' ',"  ",'',"aaaaaa","b","aaa",'a'])
    
    # Regular Expression to remove URLs
    removeURL = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
    # Regular Expression to remove CSS
    removeCSS = re.compile(r'{\|(.*?)\|}',re.DOTALL)
    # Regular Expression to remove v?cite(.*?)}{{cite **}} or {{vcite **}}
    removeCite = re.compile(r'{{}',re.DOTALL)
    # Regular Expression to remove Punctuation
    removePunctuation = re.compile(r'[.,;_()"/\']',re.DOTALL)
    # Regular Expression to remove [[file:]]
    removeFile = re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL)
    # Regular Expression to remove Brackets and other meta characters from title
    removeBracket = re.compile(r"[~`!@#$%-^*+{\[}\]\|\\<>/?]",re.DOTALL)
    # Regular Expression to remove Infobox
    removeInfobox = re.compile(r'{{infobox(.*?)}}',re.DOTALL)
    # Regular Expression to remove references
    removeReferences = re.compile(r'== ?references ?==(.*?)==',re.DOTALL)
    # Regular Expression to remove {{.*}} from text
    removeCurlyBraces = re.compile(r'{{(.*?)}}',re.DOTALL)
    # Regular Expression to remove <..> tags from text
    removeAngleBracket = re.compile(r'<(.*?)>',re.DOTALL)
    # Regular Expression to remove junk from text
    removeJunk = re.compile(r"[~`!@#$%-^*+{\[}\]\|\\<>/?]",re.DOTALL)
    
    def __init__(self):
        pass
    
    def isEnglish(self,text):
        return all(ord(ch) < 128 for ch in text)
    
    def removePunctuationsAndDigits(self,tokenList):
        tokenList = [re.sub('[^A-Za-z]+', '', token) for token in tokenList]
        return tokenList
    
    def removeStopWords(self,tokenList):
#         f = lambda t: (t not in TextProcessor.STOPWORDS) and (t not in TextProcessor.URL_STOP_WORDS) and (t not in TextProcessor.REFERENCES_STOP_WORDS) and self.isEnglish(t)
#         cleanTokens = [t for t in tokenList if f(t)==1]
        tokenSet = set(tokenList)
        tokenSet = tokenSet - TextProcessor.STOPWORDS
        tokenSet = tokenSet - TextProcessor.URL_STOP_WORDS
        tokenSet = tokenSet - TextProcessor.REFERENCES_STOP_WORDS
        cleanTokens = list(tokenSet)
        return cleanTokens
    
    def checkLen(self,tokenList):
        f = lambda t: (len(t)>=3 and len(t)<=15)
        cleanTokens = [t for t in tokenList if f(t)==1]
        return cleanTokens
    
    def performStemming(self,tokenList):
        stemmed = [TextProcessor.STEMMER.stem(t,0,len(t)-1) for t in tokenList]
        return stemmed
    
    
    def cleanTokenList(self,tokenList):
        
        ''' 1. Remove punctuations and digits'''
        tokenList = self.removePunctuationsAndDigits(tokenList)
        
        ''' 2. Remove STOP WORDS'''
        tokenList = self.removeStopWords(tokenList)
        
        tokenList = self.checkLen(tokenList)
        
        '''3. Perform Stemming using SnowBall PorterStemmer'''
        tokenList = self.performStemming(tokenList)
        
        return tokenList
    
    def tokenize(self,data):
        tokenizedWords = re.findall("\d+|[\w]+",data)
        tokenizedWords = [key for key in tokenizedWords]
        return tokenizedWords
    
    
    def buildWordFreqDict(self,tokenList):
        wordFreqDict = defaultdict(int)
        for t in tokenList:
            gc.disable()
            wordFreqDict[t]+=1
            gc.enable()
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
        external = list(filter(None, external)) 
        external = self.tokenize(' '.join(external))
        external = self.cleanTokenList(external)
        return self.buildWordFreqDict(external)
    
    def referenceFromText(self,text):
        refRegExp = r'== ?references ?==(.*?)=='
        references = re.findall(refRegExp,text,flags=re.DOTALL)
        references = list(filter(None, references)) 
        references = self.tokenize(' '.join(references))
        references = self.cleanTokenList(references)
        return self.buildWordFreqDict(references)
    
    def categoryFromText(self,text):

        catRegExp = r'\[\[category:(.*?)\]\]'
        category = re.findall(catRegExp,text,flags=re.MULTILINE)
        category = list(filter(None, category)) 
        category = self.tokenize(' '.join(category))
        category = self.cleanTokenList(category)
        return self.buildWordFreqDict(category)
   
    def extract_infobox(self, text):
        # find  all infoboxes
        text = re.sub("&gt", ">", text)
        text = re.sub("&lt;", "<", text)
        text = re.sub("<ref.?>.?</ref>", " ", text)
        text = re.sub("</?.*?>", " ", text)

        infobox = []
        start = 0
        end = 0
        while True:
            start = text.find('{{infobox', start)
            if start == -1:
                break
            end = self.find_infobox_end(text, start)
            if end < start:
                # invalid infobox. eg: on page with title: "Wikipedia:Templates for discussion/Log/2014 May 2"
                break
            infobox.append(text[start:end])
            start = end + 1  # look for other infoboxes

        infobox = list(filter(None, infobox)) 
        infobox = self.tokenize(' '.join(infobox))
        infobox = self.cleanTokenList(infobox)
        infobox = self.buildWordFreqDict(infobox)
        return infobox
    
    @staticmethod
    def find_infobox_end(text, start):
        startOffset = len('{{infobox')
        search_pos = start + startOffset
        end = search_pos

        while True:
            # if we encounter closing braces before any new opening braces
            # then it means infobox closed
            next_opening_pos = text.find("{{", search_pos)
            next_closing_pos = text.find("}}", search_pos)

            if next_closing_pos <= next_opening_pos or next_opening_pos == -1:
                # if closing braces come before opening braces (or) opening braces do not exist
                end = next_closing_pos + 2
                break
            search_pos = next_closing_pos + 2
        return end
        
    def process_body_text(self, text):
         
        text = TextProcessor.removeURL.sub('',text)
        text = TextProcessor.removeCSS.sub('',text)
        text = TextProcessor.removeCite.sub('',text)
        text = TextProcessor.removePunctuation.sub(' ',text)
        text = TextProcessor.removeFile.sub('',text)
        text = TextProcessor.removeBracket.sub('',text)
        text = TextProcessor.removeInfobox.sub('',text)
        text = TextProcessor.removeCurlyBraces.sub('',text)
        text = TextProcessor.removeReferences.sub('',text)
        text = TextProcessor.removeAngleBracket.sub('',text)
        text = TextProcessor.removeJunk.sub('',text)
        
        tokens = self.tokenize(text)
        tokens = list(filter(None, tokens)) 
        gc.disable()
        tokenSet = set(tokens)
        tokenSet = tokenSet - TextProcessor.STOPWORDS
        tokenSet = tokenSet - TextProcessor.URL_STOP_WORDS
        tokenSet = tokenSet - TextProcessor.REFERENCES_STOP_WORDS
        cleanTokens = list(tokenSet)
        l = lambda t: (len(t)>=3 and len(t)<=15)
        cleanTokens = [t for t in cleanTokens if l(t)==1 and self.isEnglish(t)]
        
        stemmed = [TextProcessor.STEMMER.stem(t,0,len(t)-1) for t in cleanTokens]
        
        body = self.buildWordFreqDict(stemmed)
        gc.enable()
        return body
    
    def processText(self,text):
        
        externalLinks = self.externalLinksFromText(text)
        references = self.referenceFromText(text)
        text = text.replace('_','').replace(',','')
        category = self.categoryFromText(text)
        infoBox = self.extract_infobox(text)
        body = self.process_body_text(text)

        return body, infoBox, category, externalLinks, references
    
    def processTextBulk(self,docIdTextMapping):
        processedTextBulk = defaultdict()
        for docId, text in docIdTextMapping.items():
            #print("parsing docId: ",docId)
            gc.disable()
            inner = defaultdict()
            body, infoBox, category, externalLinks, references = self.processText(text)
            inner['b'] = body 
            inner['i'] = infoBox
            inner['c'] = category
            inner['e'] = externalLinks
            inner['r'] = references
            processedTextBulk[docId] = inner
            gc.enable()
        return processedTextBulk
            
    def processTitleBulk(self,docIdTitleMapping):
        processedTitleBulk = defaultdict()
        for docId, title in docIdTitleMapping.items():
            gc.disable()
            titleWordFreq = self.processTitle(title)
            processedTitleBulk[docId] = titleWordFreq
            gc.enable()
        return processedTitleBulk
