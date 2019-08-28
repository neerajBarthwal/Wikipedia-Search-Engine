from nltk.corpus import stopwords
import re
from collections import defaultdict
import gc
from PorterStemmer import PorterStemmer
from absl.logging import info

class TextProcessor:
    
    STEMMER = PorterStemmer() 
    STOPWORDS = set(stopwords.words('english'))
    URL_STOP_WORDS = set(["http", "https", "www", "ftp", "com", "net", "org", "archives", "pdf", "html", "png", "txt", "redirect","web","htm","infobox","defaultsort"])
    #STEMMER = SnowballStemmer('english')
    REFERENCES_STOP_WORDS = set(["reflist","infobox", "refs","em","30em","|","90em","24em","refbegin","refend","cite","author","publisher","ref","title","=","isbn","book","archivedate","archiveurl","accessdate","deadurl","last","first","first1","last1","last2"," ",' ',"  ",''])
    def __init__(self):
        pass
    
    def removePunctuationsAndDigits(self,tokenList):
        tokenList = [re.sub('[^A-Za-z]+', '', token) for token in tokenList]
        return tokenList
    
    def removeStopWords(self,tokenList):
        f = lambda t: (t not in TextProcessor.STOPWORDS) and (t not in TextProcessor.URL_STOP_WORDS) and (t not in TextProcessor.REFERENCES_STOP_WORDS)
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
        
#         print(type(infobox))
#         print(infobox)
        infobox = list(filter(None, infobox)) 
        infobox = self.tokenize(' '.join(infobox))
        infobox = self.cleanTokenList(infobox)
        infobox = self.buildWordFreqDict(infobox)
        return infobox
    
    @staticmethod
    def find_infobox_end(text, start):
        search_pos = start + len('{{infobox')
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
    

    
    def extractBody(self,text):
        endIndex = text.find('==references')
        if endIndex == -1:
            endIndex = text.find('== references')
        else:
            endIndex = text.find('[[category')
        
        body = text[0:endIndex]
        body = self.tokenize(body)
        body = self.cleanTokenList(body)
        body = self.buildWordFreqDict(body)
        return body
    
    
    def process_body_text(self, text):
        infoRegExp = r'{{infobox(.*?)}}'
        # Regular Expression for References
        refRegExp = r'== ?references ?==(.*?)=='
        # Regular Expression to remove URLs
        
        regExp1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
        # Regular Expression to remove CSS
        regExp2 = re.compile(r'{\|(.*?)\|}',re.DOTALL)
        # Regular Expression to remove v?cite(.*?)}{{cite **}} or {{vcite **}}
        regExp3 = re.compile(r'{{}',re.DOTALL)
        # Regular Expression to remove Punctuation
        regExp4 = re.compile(r'[.,;_()"/\']',re.DOTALL)
        # Regular Expression to remove [[file:]]
        regExp5 = re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL)
        # Regular Expression to remove Brackets and other meta characters from title
        regExp6 = re.compile(r"[~`!@#$%-^*+{\[}\]\|\\<>/?]",re.DOTALL)
        # Regular Expression to remove Infobox
        regExp7 = re.compile(infoRegExp,re.DOTALL)
        # Regular Expression to remove references
        regExp8 = re.compile(refRegExp,re.DOTALL)
        # Regular Expression to remove {{.*}} from text
        regExp9 = re.compile(r'{{(.*?)}}',re.DOTALL)
        # Regular Expression to remove <..> tags from text
        regExp10 = re.compile(r'<(.*?)>',re.DOTALL)
        # Regular Expression to remove junk from text
        regExp11 = re.compile(r"[~`!@#$%-^*+{\[}\]\|\\<>/?]",re.DOTALL)
        
        text = regExp1.sub('',text)
        text = regExp2.sub('',text)
        text = regExp3.sub('',text)
        text = regExp4.sub(' ',text)
        text = regExp5.sub('',text)
        text = regExp6.sub('',text)
        text = regExp7.sub('',text)
        text = regExp8.sub('',text)
        text = regExp9.sub('',text)
        text = regExp10.sub('',text)
        text = regExp11.sub('',text)
        
        tokens = self.tokenize(text)
        tokens = list(filter(None, tokens)) 
        gc.disable()
        f = lambda t: (t not in TextProcessor.STOPWORDS) and (t not in TextProcessor.URL_STOP_WORDS) and (t not in TextProcessor.REFERENCES_STOP_WORDS)
        cleanTokens = [t for t in tokens if f(t)==1]
        stemmed = [TextProcessor.STEMMER.stem(t,0,len(t)-1) for t in cleanTokens]
        body = self.buildWordFreqDict(stemmed)
        gc.enable()
        return body
    
    def processText(self,text):
        
#         self.track+=1
        '''1. Case Folding'''
        #text = text.lower()
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
        processedTitleBulk = {}
        for docId, title in docIdTitleMapping.items():
            gc.disable()
            titleWordFreq = self.processTitle(title)
            processedTitleBulk[docId] = titleWordFreq
            gc.enable()
        return processedTitleBulk
              
        
        
        
        
        
        
        
        
        
        
