docName_file=open('docNameToDocId.txt','r')



docName_data_list=docName_file.readlines()
docName_Map={}
for line in docName_data_list:
    line=line.split()
    strName=" ".join(line[0:len(line)-1])
    docId=int(line[-1])
    docName_Map[strName]=docId
    
#print docName_Map

sentenceToWordNumMap_file=open('sentenceToWordNumMap.txt','r')

sentenceToWordNumMap_list=sentenceToWordNumMap_file.readlines()


sentenceToWordNumMap_list=[line.split() for line in sentenceToWordNumMap_list]


vocaSize=int(sentenceToWordNumMap_list[0][0]) 
del sentenceToWordNumMap_list[0]


fileName="African runner murder(4)"
vecFile=open('African runner murder(4)_vec.txt','w')

#summaryFile=open(fileName,'r')
sentenceToWordNumMapFile=open('sentenceToWordNumMap.txt','r')
sentenceToWordNumMap_list=sentenceToWordNumMapFile.readlines()

sentenceToWordNumMap_list=[sentWord.split() for sentWord in sentenceToWordNumMap_list]
    
summaryFileID_int=docName_Map[fileName]

#print summaryFileID_int

DocSentWordMap=[sent for sent in sentenceToWordNumMap_list if sent[0]==str(summaryFileID_int)and len(sent[3:])!=0]



    
#----------------convert sentence to vector---------------------------
def sent2vec(sentWordList,vecSize):
    vec=[0 for x in range(vecSize)]
    for word in sentWordList:
        vec[int(word)]=1
    return vec
#---------------------test the code of sentence to vector-----------------


vecList=[]
vecStr=""
wordList=[]

for sentword in DocSentWordMap:
    vec=sent2vec(sentword[3:],vocaSize)
    words=sentword[3:]
    wordList.append(words)
    
    vecList.append(vec)
    
    vec=[str(x) for x in vec]
    vecStr+=' '.join(sentword[:3])
    vecStr+=' '
    vecStr+=' '.join(vec)
    vecStr+='\n'

#-----------------------



#------------------------
#print vecList[0]
#print vecList[-1]
vecFile.write(vecStr)

#from rteScore import all_features
#result = all_features(vecList[0],vecList[1],DocSentWordMap[0][3:],DocSentWordMap[1][3:])



from oneSentToManyTweet_score import oneSentToManyTweet_score
#val = oneSentToManyTweet_score(vecList[0],DocSentWordMap[0][3:],vecList,wordList)#-----------working on-------------

vecList_len=len(vecList)

sentences_Tweets_score=[]
for ind in range(vecList_len):
    score_arr = oneSentToManyTweet_score(vecList[ind],wordList[ind],vecList,wordList)
    sentences_Tweets_score.append(score_arr)
    print 'sent no = ',ind,score_arr
    
    



#print dist1

docName_file.close()
vecFile.close()
sentenceToWordNumMapFile.close()
sentenceToWordNumMap_file.close()
    








