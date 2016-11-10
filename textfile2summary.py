from scipy.spatial import distance
import time
import os
import sys
import re
import numpy
import pageRank as pr
def MMR(Sent_ScoreList,SentVecList,summaryLen):

    Sent_ScoreListVal=[val for (val,ind) in Sent_ScoreList]
    Sent_ScoreListInd=[ind for (val,ind) in Sent_ScoreList]

    max_val=max(Sent_ScoreListVal)
    Sent_ScoreListVal=[max_val-val for val in Sent_ScoreListVal]
    Sent_ScoreList=[(Sent_ScoreListVal[0],Sent_ScoreListInd[i]) for i in range(len(Sent_ScoreListVal))]
    
    selectedVecSent.append(SentVecList[0])
    del SentVecList[0]
    selectedScore=[]
    selectedScore.append(Sent_ScoreList[0])
    del Sent_ScoreList[0]

    i=1
    while i<summaryLen:

        distMat=distance.cdist(selectedVecSent,SentVecList,'cosine')

        min_val=distMat.argmin()
        max_val=distMat.argmax()
        distMat=max_val-distMat
        row_column=numpy.unravel_index(max_val, distMat.shape)

        selectedSent_ind=row_column[0]
        newLySelected_ind=row_column[1]

        

        i+=1
        
                

            
            
        

        
        

        
    print 'start MMR'

def create_and_save_Summary(fileName,ScoreList,SentList,summaryLen):
    print 'sumary'
    saveToFile=open(fileName,'w')
    Summary=""
    for ind in range(summaryLen):
        
        Summary+=str(SentList[ScoreList[ind][1]])+'.\n'
        
    saveToFile.write(Summary)
    saveToFile.close()
    
    
def NewsToTweetsScor(newsVecList,newsWordList,tweetVecList,tweetWordList,scoreFile):
    
    print 'start NewsToTweetsScore'
    
    cosine_dist=distance.cdist(newsVecList,tweetVecList,'cosine')
    #print cosine_dist
    euclidean_dist=distance.cdist(newsVecList,tweetVecList,'euclidean')
    #print euclidean_dist
    dice_dist=distance.cdist(newsVecList,tweetVecList,'dice')
    #print dice_dist
    manhattan_dist=distance.cdist(newsVecList,tweetVecList,'cityblock')
    #print manhattan_dist
    correlation_dist=distance.cdist(newsVecList,tweetVecList,'correlation')
    #print correlation_dist
    jaccard_dist=distance.cdist(newsVecList,tweetVecList,'jaccard')
    #print 'jaccard dist = ',jaccard_dist

    lcs_dist=0
    #print 'lcs dist = ',lcs_dist
    total_dist=cosine_dist+euclidean_dist+dice_dist+manhattan_dist+correlation_dist+jaccard_dist+lcs_dist
    total_dist =total_dist/6.0
    #print 'total dist = ',total_dist
    total_dist=total_dist.tolist()
    strScore=""
    print 'calculation finished'

    for x in total_dist:
        strScore+=' '.join(str(float(v)) for v in x)
        strScore+='\n'

    print 'End'
    scoreFile.write(strScore)
    scoreFile.close()

    #----total dist is a sipy array---
    return list(total_dist)

    
def textfile2summary(fileName):


    directory=fileName+'_summary_'
    folderPath=directory+"\\"
    #-------------------------------------
    
    mypath=""
    docFile=open(mypath+fileName,'r')
    text=docFile.read().split('\n\n')
    docFile.close()
    del text[3]
    HighLight=text[0]
    News=text[1]
    NewsSentList=News.split('\n')
    print 'news sent num = ',len(NewsSentList)
    cc=0
    for line in NewsSentList:

        print cc,'   ',line
        cc+=1
    
    Tweets=re.sub('[~!@#$%^&*()_+\'\",\\-/|1234567890.=`]','',text[2])
    TweetList=Tweets.split('\n')
    print 'tweets sent num = ',len(TweetList)
    
    
    
    
    
    #----------------------------
    if not os.path.exists(directory):
        print 'Not exist'
        os.makedirs(directory)
    else:
        print 'exist'
    
    print 'textfile2summary start'
    
    docName_file=open('docNameToDocId.txt','r')
    vecFile=open(fileName+'_vec.txt','w')
    docwordFile=open('African runner murder(4)_vec.txt','w')
    scoreFile=open(folderPath+'score_test.txt','w+')

    



    docName_data_list=docName_file.readlines()
    docName_Map={}
    for line in docName_data_list:
        line=line.split()
        strName=" ".join(line[0:len(line)-1])
        docId=int(line[-1])
        docName_Map[strName]=docId
    print docName_Map
        
    #print docName_Map

    #-----------------------------

    sentenceToWordNumMap_file=open('sentenceToWordNumMap.txt','r')

    sentenceToWordNumMap_list=sentenceToWordNumMap_file.readlines()


    sentenceToWordNumMap_list=[line.split() for line in sentenceToWordNumMap_list]


    vocaSize=int(sentenceToWordNumMap_list[0][0]) 
    del sentenceToWordNumMap_list[0]

    #summaryFile=open(fileName,'r')
    #sentenceToWordNumMapFile=open('sentenceToWordNumMap.txt','r')
    #sentenceToWordNumMap_list=sentenceToWordNumMapFile.readlines()

    #sentenceToWordNumMap_list=[sentWord.split() for sentWord in sentenceToWordNumMap_list]
        
    summaryFileID_int=docName_Map[fileName]

    print summaryFileID_int

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
    '''
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
    
    '''
    #-----------------------------------
    start_time=time.time()
    
    newsVecList=[x[3:] for x in newsVecList]
    newsWordList=[x[3:] for x in newsWordList]
    tweetVecList=[x[3:] for x in tweetVecList]
    tweetWordList=[x[3:] for x in tweetWordList]

    ScoreMatList=[]
    ScoreMatTypeList=[]
    
    a2b='sent2tweet'
    scoreFile=open(folderPath+fileName+'_'+a2b+'_score_test.txt','w+')
    ScoreSent2Tweet=NewsToTweetsScor(newsVecList,newsWordList,tweetVecList,tweetWordList,scoreFile)
    ScoreMatList.append(ScoreSent2Tweet)
    ScoreMatTypeList.append(('s','t'))
    
    a2b='sent2sent'
    scoreFile=open(folderPath+fileName+'_'+a2b+'_score_test.txt','w+')
    ScoreSent2Sent=NewsToTweetsScor(newsVecList,newsWordList,newsVecList,newsWordList,scoreFile)
    ScoreMatList.append(ScoreSent2Sent)
    ScoreMatTypeList.append(('s','s'))
    
    a2b='tweet2sent'
    scoreFile=open(folderPath+fileName+'_'+a2b+'_score_test.txt','w+')
    ScoreTweet2Sent=NewsToTweetsScor(tweetVecList,tweetWordList,newsVecList,newsWordList,scoreFile)
    ScoreMatList.append(ScoreTweet2Sent)
    ScoreMatTypeList.append(('t','s'))
    
    a2b='tweet2tweet'
    scoreFile=open(folderPath+fileName+'_'+a2b+'_score_test.txt','w+')
    ScoreTweet2Tweet=NewsToTweetsScor(tweetVecList,tweetWordList,tweetVecList,tweetWordList,scoreFile)
    ScoreMatList.append(ScoreTweet2Tweet)
    ScoreMatTypeList.append(('t','t'))

    #------------------TexRank Working------------------------------
    print 'TexRank start'
    typeMat=[('s','t')]
    print len(ScoreMatList)
    node_score=pr.TexRank(ScoreMatList,ScoreMatTypeList)
    TexRanksentScore,TexRanktweetScore=pr.diff_sent_tweet_score(node_score)
    print 'TexRank end'
    
    #TRNewsSummaryFile=open(folderPath+fileName+'_TexRank_sent_.txt','w')
    #TRTweetSummaryFile=open(folderPath+fileName+'_TexRank_tweet_.txt','w')
    TRNewsSummaryFileName=folderPath+fileName+'_TexRank_sent.txt'
    TRTweetSummaryFileName=folderPath+fileName+'_TexRank_tweet.txt'
    summaryLen=4
    
    create_and_save_Summary(TRNewsSummaryFileName,TexRanksentScore,NewsSentList,summaryLen)
    create_and_save_Summary(TRTweetSummaryFileName,TexRanktweetScore,TweetList,summaryLen)

    
    #------------------TexRank end-------------------
    
    print 'scoring end'
    #-----------------------------------sorte sum--------------------------------------
    TotalSentNumber=len(ScoreSent2Sent)
    TotalTweetNumber=len(ScoreTweet2Tweet)

    print 'sent and tweet = ',TotalSentNumber,TotalTweetNumber
    
    Sent_i_sent_j=[sum(x)*1.0/TotalSentNumber for x in ScoreSent2Sent]
    
    sent_i_tweet_j=[sum(x)*1.0/TotalSentNumber for x in ScoreSent2Tweet]

    tweet_i_tweet_j=[sum(x)*1.0/TotalTweetNumber for x in ScoreTweet2Tweet]
    tweet_i_sent_j=[sum(x)*1.0/TotalTweetNumber for x in ScoreTweet2Sent]

    alpha=0.85
    
    sent_i_score_list=[((1-alpha)*Sent_i_sent_j[i]+alpha*sent_i_tweet_j[i],i) for i in range(1,TotalSentNumber)]
    sent_i_score_list=sorted(sent_i_score_list)
    #sent_i_score_list.reverse()
    print 'all Sentence score = ',sent_i_score_list[:10]


    tweet_i_score_list=[((1-alpha)*tweet_i_tweet_j[i]+alpha*tweet_i_sent_j[i],i) for i in range(1,TotalTweetNumber)]
    tweet_i_score_list=sorted(tweet_i_score_list)
    print 'all Tweet score = ',tweet_i_score_list[:10]



    NewsSummaryFile=open(folderPath+fileName+'_sent_.txt','w')
    TweetSummaryFile=open(folderPath+fileName+'_tweet_.txt','w')
    summaryLen=4
    TweetSummary=""
    SentSummary=""
    for ind in range(4):
        
        SentSummary+=str(NewsSentList[sent_i_score_list[ind][1]])+'.\n'
        
    NewsSummaryFile.write(SentSummary)
    #-------------------
    '''
        calculate mmr
    '''
    

    #---------------------

    for ind in range(4):
        TweetSummary+=str(TweetList[tweet_i_score_list[ind][1]])+'.\n'
        
    TweetSummaryFile.write(TweetSummary)
    NewsSummaryFile.close()
    TweetSummaryFile.close()
    print 'ok ',time.time()-start_time
    
    #----------------------------------
   
    docName_file.close()
    docwordFile.close()
    vecFile.close()
    #sentenceToWordNumMapFile.close()
    sentenceToWordNumMap_file.close()
    #scoreFile.close()
    #--------------------------------------------------
'''
#------------main execution start from here--------------
'''
DocumentName="African runner murder(4)"
summarySize=4

textfile2summary(DocumentName)
        
