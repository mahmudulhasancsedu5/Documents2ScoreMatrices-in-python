from scipy.spatial import distance
import numpy
import math


import time
import os
import sys
import re

import pageRank as pr
import gc

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

def MMR2(SentScoreList,SentVecList,summaryLen):
    print 'MMR2 start'

    scors=[x[0] for x in SentScoreList]
    max_score=max(scors)
    new_scoreList=[(max_score-x[0],x[1]) for x in SentScoreList]
    
    SentScoreList=[x for x in new_scoreList]
    
    UnselectedScore=[x for x in SentScoreList]
    
    UnselectedScore=sorted(UnselectedScore)
    print UnselectedScore
    SelectedScore=[]
    SelectedScore.append(UnselectedScore[-1])
    del UnselectedScore[-1]

    


    while len(SelectedScore)<summaryLen and len(UnselectedScore)!=0:
        print 'selected before= ',SelectedScore
        print 'unselected before = ',UnselectedScore

        UnSelected_temp=[]
        for u in UnselectedScore:
            max_sim=0
            
            for v in SelectedScore:
                vec1=SentVecList[u[1]]
                vec2=SentVecList[v[1]]
                sim=0
                if numpy.linalg.norm(vec1)!=0 and numpy.linalg.norm(vec2)!=0:
                    sim=1-distance.cosine(vec1,vec2)

                #print u,v,sim
                if sim > max_sim:
                    max_sim=sim
             
            if max_sim>0.75:
                print 'big'
                new_score=0.0
            else:
                new_score=u[0]
            new_touple=(new_score,u[1])
            #print max_sim,new_touple
            
            UnSelected_temp.append(new_touple)
            #print 'temp = ',UnSelected_temp
            
        
        UnselectedScore= sorted(UnSelected_temp)
        if len(UnselectedScore)==0:
            break
        SelectedScore.append(UnselectedScore[-1])
        del UnselectedScore[-1]
        print 'selected after= ',SelectedScore
        print 'unselected after = ',UnselectedScore
        
    print 'MMR2 end'
    print SelectedScore
    return SelectedScore
    
            
def MMR3_sim(SentScoreList,SentVecList,summaryLen):
    print 'MMR2 start'

    scors=[x[0] for x in SentScoreList]
    max_score=max(scors)+1
    new_scoreList=[(1.0*(max_score-x[0])/max_score,x[1]) for x in SentScoreList]
    
    SentScoreList=[x for x in new_scoreList]
    
    UnselectedScore=[x for x in SentScoreList]
    
    UnselectedScore=sorted(UnselectedScore)
    #print UnselectedScore
    SelectedScore=[]
    #SelectedScore.append(UnselectedScore[-1])
    #del UnselectedScore[-1]

    


    while len(SelectedScore)<summaryLen and len(UnselectedScore)!=0:
        #print 'selected before= ',SelectedScore
        #print 'unselected before = ',UnselectedScore

        UnSelected_temp=[]
        for u in UnselectedScore:
            
            max_sim=0
            vec1=SentVecList[u[1]]
            
            
            for v in SelectedScore:
                #print u,"<----->",v,"\n"
                vec2=SentVecList[v[1]]
                sim=0
                
                if numpy.linalg.norm(vec1)!=0 and numpy.linalg.norm(vec2)!=0:
                    sim=1-distance.cosine(vec1,vec2)
                    #print "--------------------------------------------------------------------sim = ",sim,"\n"

                #print u,v,sim
                if sim > max_sim:
                    max_sim=sim
            '''
            if max_sim>0.75:
                print 'big'
                new_score=0.0
            else:
                new_score=u[0]
            '''
            new_score=1.0*u[0]-max_sim*u[0]
            #print u[1]," new score = ",new_score," max_sim = ",max_sim,"\n"
            new_touple=(new_score,u[1])
            #print max_sim,new_touple
            
            UnSelected_temp.append(new_touple)
            #print 'temp = ',UnSelected_temp
            
        
        UnselectedScore= sorted(UnSelected_temp)
        if len(UnselectedScore)==0:
            break
        SelectedScore.append(UnselectedScore[-1])
        del UnselectedScore[-1]
        #print 'selected after= ',SelectedScore
        #print 'unselected after = ',UnselectedScore
        #print '----------------------------------------------------------------------------------------------------',"\n"
    print 'MMR2 end'
    #print SelectedScore
    return SelectedScore


def MMR3_dist(SentScoreList,SentVecList,summaryLen):
    print 'MMR2 start'
    print 'MMR get = ',SentScoreList,"\n"

    scors=[x[0] for x in SentScoreList]
    max_score=max(scors)
    new_scoreList=[(max_score-x[0],x[1]) for x in SentScoreList]
    
    SentScoreList=[x for x in new_scoreList]
    
    UnselectedScore=[x for x in SentScoreList]
    
    UnselectedScore=sorted(UnselectedScore)
    print UnselectedScore
    SelectedScore=[]
    SelectedScore.append(UnselectedScore[-1])
    del UnselectedScore[-1]

    


    while len(SelectedScore)<summaryLen and len(UnselectedScore)!=0:
        print 'selected before= ',SelectedScore
        print 'unselected before = ',UnselectedScore

        UnSelected_temp=[]
        for u in UnselectedScore:
            max_sim=0
            min_dist=1
            
            for v in SelectedScore:
                vec1=SentVecList[u[1]]
                vec2=SentVecList[v[1]]
                sim=0
                dist=0
                
                if numpy.linalg.norm(vec1)!=0 and numpy.linalg.norm(vec2)!=0:
                    dist=distance.cosine(vec1,vec2)

                #print u,v,sim
                if dist < min_dist:
                    min_dist=dist
            '''
            if max_sim>0.75:
                print 'big'
                new_score=0.0
            else:
                new_score=u[0]
            '''
            new_score=u[0]-min_dist*u[0]
                
            new_touple=(new_score,u[1])
            #print max_sim,new_touple
            
            UnSelected_temp.append(new_touple)
            #print 'temp = ',UnSelected_temp
            
        
        UnselectedScore= sorted(UnSelected_temp)
        if len(UnselectedScore)==0:
            break
        SelectedScore.append(UnselectedScore[-1])
        del UnselectedScore[-1]
        
        print 'selected after= ',SelectedScore
        print 'unselected after = ',UnselectedScore
       
        
    print 'MMR2 end'
    print SelectedScore
    return SelectedScore 
    
def getVectoreList(FileName):

    docName_file=open('docNameToDocId.txt','r')
    docName_data_list=docName_file.readlines()
    docName_Map={}
    for line in docName_data_list:
        line=line.split()
        strName=" ".join(line[0:len(line)-1])
        docId=int(line[-1])
        docName_Map[strName]=docId
    #print docName_Map
    #-----------------------------

    sentenceToWordNumMap_file=open('sentenceToWordNumMap.txt','r')

    sentenceToWordNumMap_list=sentenceToWordNumMap_file.readlines()


    sentenceToWordNumMap_list=[line.split() for line in sentenceToWordNumMap_list]


    vocaSize=int(sentenceToWordNumMap_list[0][0]) 
    del sentenceToWordNumMap_list[0]
    summaryFileID_int=docName_Map[FileName]

    print summaryFileID_int

    TweetWordMap=[sent for sent in sentenceToWordNumMap_list if sent[0]==str(summaryFileID_int) and sent[1]=='2' and len(sent[3:])!=0]

    
    print 'vocaSize = ',vocaSize
    from document2scoreMatrices import doc2vec,seperateSentTweetVec
    TweetVecList,vecStr,wordList=doc2vec(TweetWordMap,vocaSize)#---no zero word lines---
    gc.collect()
    #-----------------------seperate sentence from tweets-------------
    
    #vecList=[[3 ,1, 0, 0, 0, 1],[3, 1, 1, 1, 0, 1],[3, 2, 0, 1, 1, 0],[3, 2, 0, 1, 1, 1]]
    #wordList=[['3','1','0','r','y','a'],['3','1','1','e','g'],['3','2','0','b'],['3','2','0','d']]
    
    #newsVecList,newsWordList,tweetVecList,tweetWordList=seperateSentTweetVec(vecList,wordList)

    TweetVecList=[(int(vecList[2]),vecList[3:]) for vecList in TweetVecList]

    return TweetVecList
    

database="F:\\Education\\4_2\\Thsis\\Dataset\\Dataset2_news_and_tweet\\"
def createMMRsummary(ScoreFileDir,FileName,systemDir,referenceDir):
    #-------------------Tweet string selection----------------------

        
    docFile=open(database+FileName,'r')
    text=docFile.read().split('\n\n')
    docFile.close()
    del text[3]
    HighLight=text[0]
    HighlightSentList=HighLight.split('\n')
     
    News=text[1]
    NewsSentList=News.split('\n')
    print 'news sent num = ',len(NewsSentList)
        
    Tweets=re.sub('[~!@#$%^&*()_+\'\",\\-/|1234567890.=`]','',text[2])
    TweetList=Tweets.split('\n')
    print 'tweets sent num = ',len(TweetList)

    scoreType=["SoRTE","PR"]
    for st in scoreType:
        
        sFile1=open(ScoreFileDir+FileName+"_"+st+"_tweet_score.txt","r")
        
        sData=sFile1.read().split('\n');
        sFile1.close()
        sData=[line.split() for line in sData if len(line)!=0]
        TweetScoreList=[(float(line[1]),int(line[0])) for line in  sData]

        #---------------get document tweet vector list-------------------
        TweetVecList= getVectoreList(FileName)
        TweetVecList=[vec[1] for vec in TweetVecList]
        #----------------MMR Selection algo--------------------
        
        ScoredSentence=MMR3_sim(TweetScoreList,TweetVecList,4)
        
        #---------------create system MMR tweet summary----------
        systemMMRsummary=systemDir+FileName+"_MMR"+st+"tweetsummary.txt"
        TweetSummaryFile=open(systemMMRsummary,"w")
        TweetSummary=""
        
        for ind in range(4):
            TweetSummary+=str(TweetList[ScoredSentence[ind][1]])+'.\n'
        
        TweetSummaryFile.write(TweetSummary)
        TweetSummaryFile.close()



    referenceSummary=referenceDir+FileName+"_reference1.txt"
    referanceSummaryFile=open(referenceSummary,"w")

    str_ref="";
    for line in HighlightSentList:
         str_ref+=str(line)
         str_ref+="\n"
    referanceSummaryFile.write(str_ref)
    referanceSummaryFile.close()
    
        

        


    
    
def doMMR(srcDir,dstDir,FileName):

    SummaryDir=dstDir+"\\"+FileName+"_MMR_ROUGE\\"
    if not os.path.exists(SummaryDir):
        print 'Not exist'
        os.makedirs(SummaryDir)
    else:
        print 'exist'
    
    systemDir= SummaryDir+"system\\"
    if not os.path.exists(systemDir):
        print 'Not exist'
        os.makedirs(systemDir)
    else:
        print 'exist'
    referenceDir=SummaryDir+"reference\\"
    if not os.path.exists(referenceDir):
        print 'Not exist'
        os.makedirs(referenceDir)
    else:
        print 'exist'

    scoreFileDir=srcDir+FileName+"_summary_\\"
    createMMRsummary(scoreFileDir,FileName,systemDir,referenceDir)
    
    
    
    
    
    
#--------------------------------test MMR--------------------------
'''
SentVecList=[[1,1,1,0],[0,0,0,0],[1,1,1,0],[1,1,0,0],[1,1,1,0]]
SentScoreList=[(6,0),(4,1),(6,2),(9,3),(5,4)]
SentScoreList=sorted(SentScoreList)
summaryLen=3
scores=MMR3_sim(SentScoreList,SentVecList,summaryLen)
'''

#------------------------------------------------------------------

srcDir="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\SoRTE results\\"
dstDir="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\SoRTE results\\MMR Summary Results\\"
if not os.path.exists(dstDir):
    print 'Not exist'
    os.makedirs(dstDir)
else:
    print 'exist'

for i in range(2,15):
    FileName="Aurora shooting("+str(i)+")"
    print FileName
    doMMR(srcDir,dstDir,FileName)



