def NewsToTweetsScor(newsVecList,newsWordList,tweetVecList,tweetWordList,scoreFile):
    print 'start NewsToTweetsScore'
    cosine_dist=distance.cdist(newsVecList,tweetVecList,'cosine')
    print cosine_dist
    euclidean_dist=distance.cdist(newsVecList,tweetVecList,'euclidean')
    print euclidean_dist
    dice_dist=distance.cdist(newsVecList,tweetVecList,'dice')
    print dice_dist
    manhattan_dist=distance.cdist(newsVecList,tweetVecList,'cityblock')
    print manhattan_dist
    correlation_dist=distance.cdist(newsVecList,tweetVecList,'correlation')
    print correlation_dist
    jaccard_dist=distance.cdist(newsVecList,tweetVecList,'jaccard')
    print 'jaccard dist = ',jaccard_dist

    lcs_dist=0
    print 'lcs dist = ',lcs_dist
    total_dist=cosine_dist+euclidean_dist+dice_dist+manhattan_dist+correlation_dist+jaccard_dist+lcs_dist
    total_dist =total_dist*-1.0/6.0
    print 'total dist = ',total_dist
    total_dist=total_dist.tolist()
    strScore=""

    for x in total_dist:
        strScore+=' '.join(str(v) for v in x)
        strScore+='\n'
    
    scoreFile.write(strScore)

    
    return total_dist

    
def textfile2summary(fileName):

    print 'textfile2summary start'
    
    docName_file=open('docNameToDocId.txt','r')
    vecFile=open('African runner murder(4)_vec.txt','w')
    docwordFile=open('African runner murder(4)_vec.txt','w')
    scoreFile=open('score_test.txt','w+')



    docName_data_list=docName_file.readlines()
    docName_Map={}
    for line in docName_data_list:
        line=line.split()
        strName=" ".join(line[0:len(line)-1])
        docId=int(line[-1])
        docName_Map[strName]=docId
    print docName_Map
        
    #print docName_Map

    sentenceToWordNumMap_file=open('sentenceToWordNumMap.txt','r')

    sentenceToWordNumMap_list=sentenceToWordNumMap_file.readlines()


    sentenceToWordNumMap_list=[line.split() for line in sentenceToWordNumMap_list]


    vocaSize=int(sentenceToWordNumMap_list[0][0]) 
    del sentenceToWordNumMap_list[0]

    #summaryFile=open(fileName,'r')
    sentenceToWordNumMapFile=open('sentenceToWordNumMap.txt','r')
    sentenceToWordNumMap_list=sentenceToWordNumMapFile.readlines()

    sentenceToWordNumMap_list=[sentWord.split() for sentWord in sentenceToWordNumMap_list]
        
    summaryFileID_int=docName_Map[fileName]

    #print summaryFileID_int

    DocSentWordMap=[sent for sent in sentenceToWordNumMap_list if sent[0]==str(summaryFileID_int)and len(sent[3:])!=0]
    
    print 'vocaSize = ',vocaSize
    from document2scoreMatrices import doc2vec,seperateSentTweetVec
    vecList,vecStr,wordList=doc2vec(DocSentWordMap,vocaSize)#---no zero word lines---

    #-----------------------seperate sentence from tweets-------------
    
    #vecList=[[3 ,1, 0, 0, 0, 1],[3, 1, 1, 1, 0, 1],[3, 2, 0, 1, 1, 0],[3, 2, 0, 1, 1, 1]]
    #wordList=[['3','1','0','r','y','a'],['3','1','1','e','g'],['3','2','0','b'],['3','2','0','d']]
    
    newsVecList,newsWordList,tweetVecList,tweetWordList=seperateSentTweetVec(vecList,wordList)

    #--------------------------------
    from document2scoreMatrices import set2setScore,allSet2allSet_score
    '''
    s2s,s2t,t2t,t2s=allSet2allSet_score(newsVecList,newsWordList,tweetVecList,tweetWordList)
    print s2s
    print s2t
    print t2t
    print t2s
    '''
    def lcs_length(a, b):
        table = [[0] * (len(b) + 1) for _ in xrange(len(a) + 1)]
        for i, ca in enumerate(a, 1):
            for j, cb in enumerate(b, 1):
                table[i][j] = (
                    table[i - 1][j - 1] + 1 if ca == cb else
                    max(table[i][j - 1], table[i - 1][j]))
        print 'len = ',table[-1][-1]
        return table[-1][-1]
    #------------------------------------------------------------------------
    from scipy.spatial import distance
    
    cosine_dist=distance.cdist(newsVecList,tweetVecList,'cosine')
    print cosine_dist
    euclidean_dist=distance.cdist(newsVecList,tweetVecList,'euclidean')
    print euclidean_dist
    dice_dist=distance.cdist(newsVecList,tweetVecList,'dice')
    print dice_dist
    manhattan_dist=distance.cdist(newsVecList,tweetVecList,'cityblock')
    print manhattan_dist
    correlation_dist=distance.cdist(newsVecList,tweetVecList,'correlation')
    print correlation_dist
    jaccard_dist=distance.cdist(newsVecList,tweetVecList,'jaccard')
    print 'jaccard dist = ',jaccard_dist
    #-------------------------------------------------------------------------
    #ff=lcs_length('uuuu','iouiui')
    #lcs_dist=distance.cdist(newsVecList,tweetVecList, lambda u, v: lcs_length(u,v))
    lcs_dist=0
    print 'lcs dist = ',lcs_dist
    total_dist=cosine_dist+euclidean_dist+dice_dist+manhattan_dist+correlation_dist+jaccard_dist+lcs_dist
    total_dist =total_dist*-1.0/6.0
    print 'total dist = ',total_dist
    total_dist=total_dist.tolist()
    strScor=""

    for x in total_dist:
        strScor+=' '.join(str(v) for v in x)
        strScor+='\n'
    
    scoreFile.write(strScor)
    #s2t=set2setScore(newsVecList,newsWordList,tweetVecList,tweetWordList)
    #print s2t
    
    #----------------------------------
   
    docName_file.close()
    docwordFile.close()
    vecFile.close()
    sentenceToWordNumMapFile.close()
    sentenceToWordNumMap_file.close()
    scoreFile.close()
#--------------------------------------------------
fileName="African runner murder(4)"

textfile2summary(fileName)
        
