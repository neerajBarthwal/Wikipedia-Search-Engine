import xml.sax.handler
from TextProcessor import TextProcessor
from IndexBuilder import IndexBuilder
import time

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
            if(self.docIdCounter%5000==0):
                processedTitleBulk = self.textProcessor.processTitleBulk(self.docIdTitleMapping)
                processedTextBulk = self.textProcessor.processTextBulk(self.docIdToTextMapping)
                self.indexBuilder.buildIndexBulk(processedTextBulk,processedTitleBulk,self.docIdTitleMapping)
                print("Total docs parsed: ",self.docIdCounter)
                self.docIdToTextMapping={}
                self.docIdTitleMapping={} 
                              
            
        elif name=="page":
            DataHandler.flag = False

def main():
    
    
#     if len(sys.argv)!=3:
#         print("Invalid Input.\n Correct Usage: python Parser.py <path_of_xml_dump> <path_of_output>") 
    xmlparser = xml.sax.make_parser()
    handler = DataHandler()
    xmlparser.setContentHandler(handler)
    xmlparser.parse("enwiki-latest-pages-articles.xml")
    #xmlparser.parse("a.xml")
    processedTitleBulk = handler.textProcessor.processTitleBulk(handler.docIdTitleMapping)
    processedTextBulk = handler.textProcessor.processTextBulk(handler.docIdToTextMapping)
    totalIndexFiles = handler.indexBuilder.buildIndexBulk(processedTextBulk,processedTitleBulk,handler.docIdTitleMapping)
    handler.docIdToTextMapping={}
    handler.docIdTitleMapping={}
    
    handler.indexBuilder.fileIO.mergeIndexes('/home/aman/neeraj/run/index',totalIndexFiles)
     
    with open('/home/aman/neeraj/run/index/numberOfFiles.txt','w') as nof:
        nof.write(str(handler.docIdCounter))
     
    docIdTitleOffset = []
    with open('/home/aman/neeraj/run/index/title.txt','r') as titleHandle:
        docIdTitleOffset.append('0')
        for line in titleHandle:
            docIdTitleOffset.append(str(int(docIdTitleOffset[-1]) + len(line.encode('utf-8'))))
    docIdTitleOffset = docIdTitleOffset[:-1]
     
    with open('/home/aman/neeraj/run/index/titleOffset.txt','w') as offsetHandle:
        offsetHandle.write('\n'.join(docIdTitleOffset)) 
    
if __name__ == "__main__":
    #gc.disable()
    startTime= time.clock()
    main()
    stopTime = time.clock()
    print(stopTime - startTime)   
            
            
            
            
            
            
            
            
