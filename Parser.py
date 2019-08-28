import xml.sax.handler
from TextProcessor import TextProcessor
from IndexBuilder import IndexBuilder
import time
import gc
class DataHandler(xml.sax.handler.ContentHandler):

    '''
        SAX Parser
    '''
    flag = False
    
    def __init__(self):
        self.titleFound = False
        self.idFound = False
        self.textFound = False
        self.docId = ""
        self.title=""
        self.text=""
        self.indexFileNumber = 0
        self.offset = 0
        self.outputDir = ""
        self.index = {}
        self.titleTermFreq = {}
        self.infoBoxTermFreq={}
        self.bodyTermFreq = {}
        self.categoryTermFreq = {}
        self.externalLinkTermFreq = {}
        self.referenceTermFreq = {}
        self.docIdCounter = 0
        self.docIdTitleMapping = {}
        self.textProcessor = TextProcessor()
        self.indexBuilder = IndexBuilder()
        self.docIdToTextMapping = {}
        
    def startElement(self, name, attrs):
        
        '''
        Invoked when a start of a tag is seen by SAX API
        '''
        if name=="id" and not self.idFound:
            self.docId =""
            self.idFound = True
        
        if name =="title" and not self.titleFound:
            self.title=""
            self.titleFound = True
        
        if name == "text" and not self.textFound:
            self.text = ""
            self.textFound = True
    
    def characters(self, content):
        '''
        Invoked when characters inside a tag are found
        '''
        if self.idFound:
            self.docId+=content
        
        elif self.titleFound:
            self.title+=content
            self.docIdTitleMapping[self.docIdCounter] = content
#             if(self.docIdCounter%10==0):
#                 print(self.docIdTitleMapping)
        
        elif self.textFound:
            self.text+=content
            
    def endElement(self, name):
        '''
        Invoked when a tag end is encountered
        '''
        if name=="id":
            self.idFound = False
        elif name == "title":
            self.titleFound = False
            #self.titleTermFreq = self.textProcessor.processTitle(self.title)
            
        elif name=="text":
            self.textFound = False
            self.text = self.text.lower()
            self.docIdToTextMapping[self.docIdCounter] = self.text
            self.docIdCounter+=1
#             if(self.docIdCounter%50==0):
#                 processedTitleBulk = self.textProcessor.processTitleBulk(self.docIdTitleMapping)
#                 processedTextBulk = self.textProcessor.processTextBulk(self.docIdToTextMapping)
#                 self.indexBuilder.buildIndexBulk(processedTextBulk,processedTitleBulk,self.docIdTitleMapping)
#                 self.docIdToTextMapping={}
#                 self.docIdTitleMapping={}
#                 stopTime = timeit.default_timer()
#                 print(stopTime - startTime)
            #self.bodyTermFreq, self.infoBoxTermFreq, self.categoryTermFreq,self.externalLinkTermFreq, self.referenceTermFreq = self.textProcessor.processText(self.text)
            #self.indexBuilder.buildIndex(self.docIdCounter,self.titleTermFreq, self.bodyTermFreq, self.infoBoxTermFreq, self.categoryTermFreq, self.infoBoxTermFreq, self.referenceTermFreq,self.docIdTitleMapping)
           
            
        elif name=="page":
            DataHandler.flag = False

def main():
    
#     if len(sys.argv)!=3:
#         print("Invalid Input.\n Correct Usage: python Parser.py <path_of_xml_dump> <path_of_output>") 
    xmlparser = xml.sax.make_parser()
    handler = DataHandler()
    xmlparser.setContentHandler(handler)
    xmlparser.parse("dump.xml-p42567204p42663461")
    #xmlparser.parse("a.xml")
    processedTitleBulk = handler.textProcessor.processTitleBulk(handler.docIdTitleMapping)
    processedTextBulk = handler.textProcessor.processTextBulk(handler.docIdToTextMapping)
    handler.indexBuilder.buildIndexBulk(processedTextBulk,processedTitleBulk,handler.docIdTitleMapping)
    handler.docIdToTextMapping={}
    handler.docIdTitleMapping={}
    
    
if __name__ == "__main__":
    #gc.disable()
    startTime= time.clock()
    main()
    stopTime = time.clock()
    print(stopTime - startTime)   
            
            
            
            
            
            
            
            
