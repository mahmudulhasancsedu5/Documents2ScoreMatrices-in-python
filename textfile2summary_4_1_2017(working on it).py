from scipy.spatial import distance
import time
import os
import sys
import re
import numpy
import pageRank as pr
import gc
import math

def dist2simScore(Dist_2D_list):
    print "Dist2Simm start"

    Dist_2D_array=numpy.array(Dist_2D_list)
    max_dist_list=Dist_2D_array.max(axis=1)
    max_dist_val=max(max_dist_list)

    Dist_2D_array=max_dist_val-Dist_2D_array

    print 'Dist2Simm end'

    return Dist_2D_array.tolist()

def word_of_S_in_T_and_of_T_in_S_and_in_and_ex_word_overlap(vec1,vec2):
    vec1_len=len(vec1)
    vec2_len=len(vec2)
    sent1=[x for x in range(vec1_len) if vec1[x]==1]
    sent2=[x for x in range(vec1_len) if vec2[x]==1]
    sent1=set(sent1)
    sent2=set(sent2)
    sent1_len=len(sent1)
    sent2_len=len(sent2)

    common=len(sent1.intersection(sent2))

    s1ins2=(common*1.00)/sent1_len
    s2ins1=(common*1.00)/sent2_len

    #print '% word of S1 in s2 = ',s1ins2
    #print '% word of S2 in s2 = ',s2ins1
    in_and_ex=0
    #in_and_ex=common+(sent1_len+sent2_len-common)

    #print 'inclusion and exclution = ',in_and_ex

    word_overlap=(common*1.00)/min(sent1_len,sent2_len)

    #print 'word overlap coefficient = ',word_overlap
    res=float(s1ins2+s2ins1+in_and_ex+word_overlap)
    return res

    
def create_and_save_Summary(fileName,ScoreList,SentList,summaryLen):
    print 'sumary'
    saveToFile=open(fileName,'w')
    Summary=""
    for ind in range(summaryLen):
        
        Summary+=str(SentList[ScoreList[ind][1]])+'.\n'
        
    saveToFile.write(Summary)
    saveToFile.close()
    gc.collect()

def seperation_4scoreMat(total_dist,sentNum,tweetNum):
    print 'seperate'
    total_len=len(total_dist)
    s2sList=[]
    s2tList=[]
    t2sList=[]
    t2tList=[]
    for i in range(total_len):
        vec=total_dist[i]
        if i<sentNum:
            print 'sent'
            s2s=vec[:sentNum]
            s2sList.append(s2s)
            s2t=vec[sentNum:]
            s2tList.append(s2t)
        else:
            print 'tweet'
            t2s=vec[:sentNum]
            t2sList.append(t2s)
            t2t=vec[sentNum:]
            t2tList.append(t2t)
    return s2sList,s2tList,t2tList,t2sList
            

def NewsToTweetsScor_partitioning_2(newsVecList,newsWordList,tweetVecList,tweetWordList,scoreFile):
    print 'partitioning 2 start'
    elements_per_partition=600.0
    newsVecList_len=len(newsVecList)
    tweetVecList_len=len(tweetVecList)
    print 'tweet end = ',tweetVecList_len,'\n'
    tweetVecList_parts=tweetVecList_len*1.0/elements_per_partition
    tweetVecList_parts=math.ceil(tweetVecList_parts)

    newsVecList_parts=newsVecList_len*1.0/elements_per_partition
    newsVecList_parts=math.ceil(newsVecList_parts)




    row_combine=[]

    news_start=0
    if newsVecList_parts>1:
        news_end=(news_start+1)*elements_per_partition
    else:
        news_end=newsVecList_len

    for i in range(int(newsVecList_parts)):

        print i,'   ',news_start,'  ',news_end
        news_part=[newsVecList[ind] for ind in range(int(news_start),int(news_end))]
        
            
        

        row_in_part=int(news_end)-int(news_start)+1
        colm_combine=[[] for r in range(row_in_part)]
        tweet_start=0
        if tweetVecList_parts>1:
            tweet_end=(tweet_start+1)*elements_per_partition
        else:
            tweet_end=tweetVecList_len
        
        for j in range(int(tweetVecList_parts)):

            tweet_part=[tweetVecList[ind] for ind in range(int(tweet_start),int(tweet_end))]


            print '         j= ',j,'   ',tweet_start,'  ',tweet_end
            
            #--------------------------------------------------------------------------------------

            total_dist=distance.cdist(news_part,tweet_part,'cosine')
            #print cosine_dist
            total_dist+=distance.cdist(news_part,tweet_part,'euclidean')
            #print euclidean_dist
            total_dist+=distance.cdist(news_part,tweet_part,'dice')
            #print dice_dist
            total_dist+=distance.cdist(news_part,tweet_part,'cityblock')
            #print manhattan_dist
            correlation_dist=distance.cdist(news_part,tweet_part,'correlation')
            #print correlation_dist
            total_dist+=distance.cdist(news_part,tweet_part,'jaccard')
            total_dist+=distance.cdist(news_part,tweet_part, lambda u, v: word_of_S_in_T_and_of_T_in_S_and_in_and_ex_word_overlap(u,v))
            #print 'jaccard dist = ',jaccard_dist
            
            total_dist=total_dist.tolist()
            
            colm_combine=[colm_combine[ind]+total_dist[ind] for ind in range(len(news_part))]

        



            #---------------------------------------------------------------------------------------
            
            
            tweet_start=tweet_end+1
            if j==tweetVecList_parts-2:
                tweet_end=tweetVecList_len
            else:
                tweet_end=tweet_end+elements_per_partition


        row_combine+=colm_combine
        
        news_start=news_end+1
        if i==newsVecList_parts-2:
            news_end=newsVecList_len
        else:
            news_end=news_end+elements_per_partition       
        

    


    print 'partitioning 2 end'

    return row_combine



def NewsToTweetsScor_partitioning(newsVecList,newsWordList,tweetVecList,tweetWordList,scoreFile):

    print 'partition scorring start'
    elements_per_partition=1000.0
    newsVecList_len=len(newsVecList)
    tweetVecList_len=len(tweetVecList)
    print 'tweet end = ',tweetVecList_len,'\n'
    tweetVecList_parts=tweetVecList_len*1.0/elements_per_partition
    tweetVecList_parts=math.ceil(tweetVecList_parts)
    
    total_score=[[] for i in range(newsVecList_len)]

    start=0
    if tweetVecList_parts>0.0:
        end=(start+1)*elements_per_partition
    else:
        end=tweetVecList_len
        
    for i in range(int(tweetVecList_parts)):

        print 'start ',start,' end ',end,'\n'
        
        tweetVecList_part=[tweetVecList[ind]for ind in range(int(start),int(end))]
        #---------------------------------------------------------------
        total_dist=distance.cdist(newsVecList,tweetVecList_part,'cosine')
        #print cosine_dist
        total_dist+=distance.cdist(newsVecList,tweetVecList_part,'euclidean')
        #print euclidean_dist
        total_dist+=distance.cdist(newsVecList,tweetVecList_part,'dice')
        #print dice_dist
        total_dist+=distance.cdist(newsVecList,tweetVecList_part,'cityblock')
        #print manhattan_dist
        correlation_dist=distance.cdist(newsVecList,tweetVecList_part,'correlation')
        #print correlation_dist
        total_dist+=distance.cdist(newsVecList,tweetVecList_part,'jaccard')
        #print 'jaccard dist = ',jaccard_dist
        total_dist=total_dist.tolist()
        
        total_score=[total_score[ind]+total_dist[ind] for ind in range(newsVecList_len)]
        #---------------------------------------------------------------
        
        start=end+1
        if i==tweetVecList_parts-2:
            end=tweetVecList_len;
        else:
            end=end+elements_per_partition
    

    print 'partition scoring end'
    return total_score
    
    
def NewsToTweetsScor_pdist(newsVecList,newsWordList,tweetVecList,tweetWordList,scoreFile):
    print 'stat pdist'
    VecList=newsVecList+tweetVecList
    #VecList=[bitarray(x) for vec in VecList1]
    total_dist=distance.pdist(VecList,'cosine')
    #print cosine_dist
    total_dist+=distance.pdist(VecList,'euclidean')
    #print euclidean_dist
    total_dist+=distance.pdist(VecList,'dice')
    #print dice_dist
    total_dist+=distance.pdist(VecList,'cityblock')
    #print manhattan_dist
    correlation_dist=distance.pdist(VecList,'correlation')
    #print correlation_dist
    total_dist+=distance.pdist(VecList,'jaccard')
    #print 'jaccard dist = ',jaccard_dist
    print gc.collect()
    return total_dist.tolist()
    
    
def NewsToTweetsScor_pair(newsVecList,newsWordList,tweetVecList,tweetWordList,scoreFile):
    print 'Score pair wise start'
    newsVecList_len=len(newsVecList)
    tweetVecList_len=len(tweetVecList)
    total_dist=[]
    for i in range(newsVecList_len):
        u=newsVecList[i]
        print i,' = ',
        u_to_v=[]
        for j in range(tweetVecList_len):
            
            v=tweetVecList[j]
            val=distance.cosine(u,v)
            val+=distance.euclidean(u,v)
            val+=distance.dice(u,v)
            val+=distance.correlation(u,v)
            val+=distance.jaccard(u,v)
            val+=distance.cityblock(u,v)
            val=val/6.0
            u_to_v.append(val)
        total_dist.append(u_to_v)
        
    print 'pair wise end'
    return total_dist
            
            
    
    
     
    
def NewsToTweetsScor(newsVecList,newsWordList,tweetVecList,tweetWordList,scoreFile):
    
    print 'start NewsToTweetsScore'
    
    total_dist=distance.cdist(newsVecList,tweetVecList,'cosine')
    #print cosine_dist
    total_dist+=distance.cdist(newsVecList,tweetVecList,'euclidean')
    #print euclidean_dist
    total_dist+=distance.cdist(newsVecList,tweetVecList,'dice')
    #print dice_dist
    total_dist+=distance.cdist(newsVecList,tweetVecList,'cityblock')
    #print manhattan_dist
    correlation_dist=distance.cdist(newsVecList,tweetVecList,'correlation')
    #print correlation_dist
    total_dist+=distance.cdist(newsVecList,tweetVecList,'jaccard')
    #print 'jaccard dist = ',jaccard_dist

    lcs_dist=0
    #print 'lcs dist = ',lcs_dist
    #total_dist=cosine_dist+euclidean_dist+dice_dist+manhattan_dist+correlation_dist+jaccard_dist+lcs_dist
    total_dist =total_dist/6.0
    #print 'total dist = ',total_dist
    total_dist_list=total_dist.tolist()
    strScore=""
    print 'calculation finished'

    for x in total_dist:
        strScore+=' '.join(str(float(v)) for v in x)
        strScore+='\n'

    print 'End'

    scoreFile.write(strScore)
    scoreFile.close()

    #----total dist is a sipy array---
    return total_dist_list

    
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
    gc.collect()
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
    #-----------------------------------------------------scor find out-----

    ScoreMatList=[]
    ScoreMatTypeList=[]
    #--------------------------------------------------------------------------------------------------------------------
    a2b='sent2tweet'
    scoreFile=open(folderPath+fileName+'_'+a2b+'_score_test.txt','w+')
    ScoreSent2Tweet=NewsToTweetsScor_partitioning_2(newsVecList,newsWordList,tweetVecList,tweetWordList,scoreFile)
    print ScoreSent2Tweet[0]

    
    
    ScoreMatList.append(ScoreSent2Tweet)
    ScoreMatTypeList.append(('s','t'))
    gc.collect()
    #----------Save Score-------------
    ScoreString=""
    for itemlist in ScoreSent2Tweet:

        ScoreString+=' '.join(str(item) for item in itemlist)
        ScoreString+='\n'
    scoreFile.write(ScoreString)
    scoreFile.close()
    
        
    
    #-------------------------------
    
    
    #-----------------------------------------------------------------------------------------------------------------------
    
    
    a2b='sent2sent'
    scoreFile=open(folderPath+fileName+'_'+a2b+'_score_test.txt','w+')
    ScoreSent2Sent=NewsToTweetsScor_partitioning_2(newsVecList,newsWordList,newsVecList,newsWordList,scoreFile)

    
    
    
    ScoreMatList.append(ScoreSent2Sent)
    ScoreMatTypeList.append(('s','s'))
    gc.collect()
    #----------Save Score-------------
    ScoreString=""
    for itemlist in ScoreSent2Sent:

        ScoreString+=' '.join(str(item) for item in itemlist)
        ScoreString+='\n'
    scoreFile.write(ScoreString)
    scoreFile.close()
    
        
    
    #-------------------------------

    #-------------------------------------------------------------------------------------------------------------------------
    
    a2b='tweet2sent'
    scoreFile=open(folderPath+fileName+'_'+a2b+'_score_test.txt','w+')
    ScoreTweet2Sent=NewsToTweetsScor_partitioning_2(tweetVecList,tweetWordList,newsVecList,newsWordList,scoreFile)
    gc.collect()
    
    
    
    ScoreMatList.append(ScoreTweet2Sent)
    ScoreMatTypeList.append(('t','s'))
    #----------Save Score-------------
    ScoreString=""
    for itemlist in ScoreTweet2Sent:

        ScoreString+=' '.join(str(item) for item in itemlist)
        ScoreString+='\n'
    scoreFile.write(ScoreString)
    scoreFile.close()
    
        
    
    #-------------------------------
    #----------------------------------------------------------------------------------------------------------------------------
    
    a2b='tweet2tweet'
    scoreFile=open(folderPath+fileName+'_'+a2b+'_score_test.txt','w+')
    ScoreTweet2Tweet=NewsToTweetsScor_partitioning_2(tweetVecList,tweetWordList,tweetVecList,tweetWordList,scoreFile)
    gc.collect()
    
    
    ScoreMatList.append(ScoreTweet2Tweet)
    ScoreMatTypeList.append(('t','t'))
    #----------Save Score-------------
    ScoreString=""
    for itemlist in ScoreTweet2Tweet:

        ScoreString+=' '.join(str(item) for item in itemlist)
        ScoreString+='\n'
    scoreFile.write(ScoreString)
    scoreFile.close()
    #-------------------------------


    
    
    #-----------------------------------SORTESUM start--------------------------------------

    SentScoreSaveToFile=open(folderPath+fileName+'_SoRTE_sent_score.txt','w')
    TweetScoreSaveToFile=open(folderPath+fileName+'_SoRTE_tweet_score.txt','w')
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
    
    print 'SoRTE all Sentence score = ',sent_i_score_list[:10]
    
    strScore=[str(x[1])+' '+str(x[0])+'\n' for x in sent_i_score_list]
    scoreStr=''.join(strScore)
    
    SentScoreSaveToFile.write(scoreStr)
    SentScoreSaveToFile.close()


    tweet_i_score_list=[((1-alpha)*tweet_i_tweet_j[i]+alpha*tweet_i_sent_j[i],i) for i in range(1,TotalTweetNumber)]
    
    tweet_i_score_list=sorted(tweet_i_score_list)
    #tweet_i_score_list.reverse()
    
    print 'SoRTE all Tweet score = ',tweet_i_score_list[:10]
    
    strScore=[str(x[1])+' '+str(x[0])+'\n' for x in tweet_i_score_list]
    
    scoreStr=''.join(strScore)
    scoreStr+='\n'
    TweetScoreSaveToFile.write(scoreStr)
    TweetScoreSaveToFile.close()
    
#--------------------------------dual wing------------------------------

    NewsSummaryFile=open(folderPath+fileName+'_SoRTESentSummary.txt','w')
    TweetSummaryFile=open(folderPath+fileName+'_SoRTETweetSummary.txt','w')
    summaryLen=4
    TweetSummary=""
    SentSummary=""
    for ind in range(4):
        
        SentSummary+=str(NewsSentList[sent_i_score_list[ind][1]])+'.\n'
        
    NewsSummaryFile.write(SentSummary)


    for ind in range(4):
        TweetSummary+=str(TweetList[tweet_i_score_list[ind][1]])+'.\n'
        
    TweetSummaryFile.write(TweetSummary)
    NewsSummaryFile.close()
    TweetSummaryFile.close()
#------------------------------------------------------------------------
#----------------------------single wing------------------------------------

    sent_i_j_score=[(sent_i_tweet_j[i],i) for i in range(len(sent_i_tweet_j))]
    sent_i_j_score=sorted(sent_i_j_score)
    tweet_i_j_score=[(tweet_i_sent_j[i],i) for i in range(len(tweet_i_sent_j))]
    tweet_i_j_score=sorted(tweet_i_j_score)

    NewsSummaryFile=open(folderPath+fileName+'_SoRTESingleWingSentSummary.txt','w')
    TweetSummaryFile=open(folderPath+fileName+'_SoRTESingleWingTweetSummary.txt','w')
    summaryLen=4
    TweetSummary=""
    SentSummary=""
    for ind in range(4):
        
        SentSummary+=str(NewsSentList[sent_i_j_score[ind][1]])+'.\n'
        
    NewsSummaryFile.write(SentSummary)


    for ind in range(4):
        TweetSummary+=str(TweetList[tweet_i_j_score[ind][1]])+'.\n'
        
    TweetSummaryFile.write(TweetSummary)
    NewsSummaryFile.close()
    TweetSummaryFile.close()



#-------------------------------------------------------------------------
    #-------------------
    
        #calculate mmr
    
    

    #---------------------



    #--------------------------------------------------------------
    '''
    import MMR_algo
    tweet_i_score_list=MMR_algo.MMR2(tweet_i_score_list,tweetVecList,4)
    print tweet_i_score_list
    '''
    #--------------------------------------------------------------
   


    #--------------------------------------------------------------------------------------------------------------------------------

    #---------------------------------------------------------------------------


    ScoreSent2Tweet=dist2simScore(ScoreSent2Tweet)#distance---------------->similarity
    ScoreSent2Sent=dist2simScore(ScoreSent2Sent)#distance---------------->similarity
    ScoreTweet2Sent=dist2simScore(ScoreTweet2Sent)#distance---------------->similarity
    ScoreTweet2Tweet=dist2simScore(ScoreTweet2Tweet)#distance---------------->similarity

    #---------------------------------------------------------------------------

    #------------------PageRank Working------------------------------
    
    print 'PageRank start'

    PRSentScoreSaveToFile=open(folderPath+fileName+'_PR_sent_score.txt','w')
    PRTweetScoreSaveToFile=open(folderPath+fileName+'_PR_tweet_score.txt','w')
    
    #typeMat=[('s','t')]
    print len(ScoreMatList)
    
    
    node_score=pr.TexRank(ScoreMatList,ScoreMatTypeList)
    TexRanksentScore,TexRanktweetScore=pr.diff_sent_tweet_score(node_score)

    
    #----------------------------

    strScore=[str(x[1])+' '+str(x[0])+'\n' for x in TexRanksentScore]
    scoreStr=''.join(strScore)
    
    PRSentScoreSaveToFile.write(scoreStr)
    PRSentScoreSaveToFile.close()

    strScore=[str(x[1])+' '+str(x[0])+'\n' for x in TexRanktweetScore]
    scoreStr=''.join(strScore)
    
    PRTweetScoreSaveToFile.write(scoreStr)
    PRTweetScoreSaveToFile.close()


    #----------------------------

    
    print 'TexRank end'
    gc.collect()
    
    #TRNewsSummaryFile=open(folderPath+fileName+'_TexRank_sent_.txt','w')
    #TRTweetSummaryFile=open(folderPath+fileName+'_TexRank_tweet_.txt','w')
    PRNewsSummaryFileName=folderPath+fileName+'_PRSentSummary.txt'
    PRTweetSummaryFileName=folderPath+fileName+'_PRTweetSummary.txt'
    summaryLen=4
    
    create_and_save_Summary(PRNewsSummaryFileName,TexRanksentScore,NewsSentList,summaryLen)
    create_and_save_Summary(PRTweetSummaryFileName,TexRanktweetScore,TweetList,summaryLen)
    gc.collect()
    
    #------------------TexRank end-------------------
    
    print 'scoring end'



    
    print 'Time = ',time.time()-start_time
    
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

#----------------------------

#-------------------------------main ---------------------------------------


#DocumentName="Aurora shooting(1)"


#textfile2summary(DocumentName)


#---------------------------

i=11
while i>0:

    DocumentName="Asiana Airlines Flight 214("+str(i)+")"
    print "------------------",DocumentName,"-----------------------------------------\n"
    textfile2summary(DocumentName)
    i=i-1
    




        
