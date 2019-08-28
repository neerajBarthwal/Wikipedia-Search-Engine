import bz2
import time
from collections import defaultdict
from ast import literal_eval
import json
import re
def main():
    root = "/home/neeraj/IRE"
    test = defaultdict(dict) 
    test['a'] = {'15':16,'100':20}
    test['aa'] = {'13':16,'10':50}

#     with open('file.txt', 'w') as file:
#         file.write(json.dumps(test))
#         
#     with open('file.txt') as json_file:
#         data = json.load(json_file)
#         print(type(data))
#         print(data)

#########################################################################
#     with bz2.BZ2File(root+'/test.txt.bz2','wb') as indexHandle:
#         indexHandle.write(str(test).encode(encoding='utf_8'))
#         
#     file=bz2.BZ2File(root+'/test.txt.bz2','rb')
#     file = file.read()
#     file = file.decode()
#     
#     index = file.find('{')
#     file = file[index:]
#     file = file[:-1]
#     test_r = literal_eval(file)
#     print(test_r['a']['15'])
#######################################################################################
#     titleList = file.split('\n')
#     titleIndex = defaultdict(dict)
#     for entry in titleList:
#         entry = entry.split(' ')
        
#     test = defaultdict(dict)
#     
#     test['a'] = {'15':16,'100':20}
#     test['aa'] = {'13':16,'10':50}
#     print(test['a']['15'])
#     with bz2.BZ2File(root+'/test.txt.bz2','w') as indexHandle:
#         indexHandle.write(str(test).encode(encoding='utf_8'))
#     
#     file=bz2.BZ2File(root+'/test.txt.bz2','rb')
#     file = file.read()
#     file = file.decode()
#     retDict = literal_eval(file)
        
#     
#     print(retDict)
    q = "title:gandhi body:arjun infobox:gandhi category:gandhi ref:gandhi"
    if re.search('[titie|body|infobox|category|ref]:', q):
        print(q)
if __name__ == "__main__":
    #gc.disable()
    startTime= time.clock()
    main()
    stopTime = time.clock()
    print(stopTime - startTime)   
                
                