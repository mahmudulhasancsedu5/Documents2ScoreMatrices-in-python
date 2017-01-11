from scipy.spatial import distance
import time
import os
import sys
import re
import numpy
import pageRank as pr
import gc
import math

def GetDocIdByDocName(DocName):
    print 'GetDocIdByDocName start DocName = ',DocName

    docName_file=open('docNameToDocId.txt','r')
   
    docName_data_list=docName_file.readlines()
    for line in docName_data_list:
        line=line.split()
        strName=" ".join(line[0:len(line)-1])
        docId=int(line[-1])
        print strName,DocName
        if strName==DocName:
            print 'GetDocIdByDocName end'
            return docId  #return int
        
    print 'No DocName Matched'


def DocSentWordListToBigramList(DocSentWordList):
    print 'DocSentWordListToBigramList start'

    DocSentBigramList=[]
    DocSentBigramMaxCount={}
    for line in DocSentWordList:
        line_len=len(line)
        line_bigram_list=[]
        
        for i in range(line_len-1):
            bigram=line[i]+' '+line[i+1]

            if bigram in DocSentBigramList:
                DocSentBigramMaxCount[bigram]+=1
            else:
                DocSentBigramMaxCount[bigram]=1
                
            
            line_bigram_list.append(bigram)
        DocSentBigramList.append(line_bigram_list)

    print 'DocSentBigramList',DocSentBigramList[:10]
    #print 'DocSentBigramMaxCount first 10 element = ',DocSentBigramMaxCount
    
    print 'number of bigram = ',len(DocSentBigramMaxCount)

    

    print 'DocSentWordListToBigramList end'

    return DocSentBigramList,DocSentBigramMaxCount




def ScoreSentByBigram(DocSentBigramList,DocSentBigramMaxCount):
    print 'SentScoreByBigram start'

    DocSentScore=[]
    i=0
    max_score=0
    for SentBigram in DocSentBigramList:

        score=0
        #print len(SentBigram)
        for Bigram in SentBigram:
            score+=DocSentBigramMaxCount[Bigram]
        temp=(score,i)
        if score>max_score:
            max_score=score
        i+=1
        
        DocSentScore.append(temp)
    print 'Max Score = ',max_score
    DocSentScore=sorted(DocSentScore)
    DocSentScore.reverse()

    #print DocSentScore
    return DocSentScore
        
            

    print 'SentScoreByBigram end'


def create_and_save_bigram_summary(FileName,DestDirectory,SentScore,TweetScore):

    directory=DestDirectory+FileName+"_bigram_summary_\\"
    #----------------------------
    if not os.path.exists(directory):
        print 'Not exist'
        os.makedirs(directory)
    else:
        print 'exist'

        
        
    docFile=open(FileName,'r')
    text=docFile.read().split('\n\n')
    docFile.close()
    
    del text[3]
    HighLight=text[0]
    News=text[1]
    NewsSentList=News.split('\n')
    print 'news sent num = ',len(NewsSentList)
    
    Tweets=re.sub('[~!@#$%^&*()_+\'\",\\-/|1234567890.=`]','',text[2])
    TweetList=Tweets.split('\n')
    print 'tweets sent num = ',len(TweetList)

    

    SummaryDir=DestDirectory+FileName+"_bigram_summary_\\"+FileName+"_bigram_\\"
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

    

    NewsSummaryFile=open(systemDir+FileName+'_SentBigramSummary.txt','w')
    TweetSummaryFile=open(systemDir+FileName+'_TweetBigramSummary.txt','w')
    referanceSummaryFile=open(referenceDir+FileName+'_reference1.txt','w')

    str_ref="";

    HighlightSentList=HighLight.split('\n')

    for line in HighlightSentList:
        
         str_ref+=str(line)
         str_ref+="\n"
    referanceSummaryFile.write(str_ref)
    referanceSummaryFile.close()




    
    summaryLen=4
    TweetSummary=""
    SentSummary=""
    for ind in range(4):
        
        SentSummary+=str(NewsSentList[SentScore[ind][1]])+'.\n'
        
    NewsSummaryFile.write(SentSummary)


    for ind in range(4):
        TweetSummary+=str(TweetList[TweetScore[ind][1]])+'.\n'
        
    TweetSummaryFile.write(TweetSummary)
    NewsSummaryFile.close()
    TweetSummaryFile.close()

    
    
    
    
    
    
    

        
    
    
def create_bigram(FileName):
    print 'create bigram start'

    SentToWordMapFile=open('sentenceToWordNumMap.txt','r')
    LineWordList=SentToWordMapFile.readlines()
    #print LineWordsList[2]
    LineWordList=[line.split() for line in LineWordList]


    DocId=GetDocIdByDocName(FileName)
    print DocId

    DocSentWordList=[line[3:] for line in LineWordList if line[0]==str(DocId) and line[1]=='1']
    DocTweetWordList=[line[3:] for line in LineWordList if line[0]==str(DocId) and line[1]=='2']

    print DocSentWordList[3:10]

    DocSentBigramList,DocSentBigramMaxCount=DocSentWordListToBigramList(DocSentWordList)
    DocTweetBigramList,DocTweetBigramMaxCount=DocSentWordListToBigramList(DocTweetWordList)

    DocSentScore=ScoreSentByBigram(DocSentBigramList,DocSentBigramMaxCount)
    print DocSentScore[:5]

    DocTweetScore=ScoreSentByBigram(DocTweetBigramList,DocTweetBigramMaxCount)
    print DocTweetScore[:5]

    print 'create bigram end'

    return DocSentScore,DocTweetScore


    

#----------------------main start---------------------




def doSummary():
    print ""
    DestDirectory="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\bigram Directory\\"
    FileName="African runner murder(1)"

    for i in range(1,15):
        FileName="Aurora shooting("+str(i)+")"
        DocSentScore,DocTweetScore=create_bigram(FileName)
        create_and_save_bigram_summary(FileName,DestDirectory,DocSentScore,DocTweetScore)
    
doSummary()

#--------------------main end
    
