from scipy.spatial import distance
import numpy
import math


import time
import os
import sys
import re

import random


database="F:\\Education\\4_2\\Thsis\\Dataset\\Dataset2_news_and_tweet\\"



def SentLeadSummary(SentArr):
    print"sent lead start\n"
    summary=""
    for i in range(1,5):
        summary+=str(SentArr[i])+'\n'
    return summary

def RandomSummary(SentArr):

    print "random start\n"
    summary=""
    arrLen=len(SentArr)

    dicCheck={}

    i=1
    while True:
        if i==5:
            break;
        
        rand_num=random.randint(1,arrLen-1)
        if rand_num not in dicCheck:
            print rand_num,' '
            dicCheck[rand_num]=1
            summary+=SentArr[rand_num]+'\n'
            
            i=i+1
            
    return str(summary)
       
        

    

    
def createSentLeadAndRandomSummary(srcDir,dstDir,FileName):

    SummaryDir=dstDir+"\\"+FileName+"_SentLeadAndRandom\\"
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
    #-----------------------create referance summary--------------------------
    referenceSummary=referenceDir+FileName+"_reference1.txt"
    referanceSummaryFile=open(referenceSummary,"w")

    str_ref="";
    for line in HighlightSentList:
         str_ref+=str(line)
         str_ref+="\n"
    referanceSummaryFile.write(str_ref)
    referanceSummaryFile.close()
    #------------------------create sentence lead and random summary----------------

    SentLeadSummaryFile=open(systemDir+FileName+"_SentLeadNewsSummary.txt","w")
    TweetLeadSummaryFile=open(systemDir+FileName+"_TweetLeadNewsSummary.txt","w")
    RandomSentSummaryFile=open(systemDir+FileName+"_RandomNewsSummary.txt","w")
    RandomTweetSummaryFile=open(systemDir+FileName+"_RandomTweetSummary.txt","w")

    

    SentLeadSummaryFile.write(SentLeadSummary(NewsSentList))
    TweetLeadSummaryFile.write(SentLeadSummary(TweetList))
    RandomSentSummaryFile.write(RandomSummary(NewsSentList))
    RandomTweetSummaryFile.write(RandomSummary(TweetList))
    
    SentLeadSummaryFile.close()
    TweetLeadSummaryFile.close()
    RandomSentSummaryFile.close()
    RandomTweetSummaryFile.close()
    
    
        
    


dstDir="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\Sentence Lead\\"
NameArr=[['African runner murder(',2,9],['Asiana Airlines Flight 214(',2,12],['Aurora shooting(',2,15]]
for File in NameArr:

    a=File[1]
    b=File[2]
    for i in range(a,b):
        FileName=File[0]+str(i)+")"
        print FileName
        createSentLeadAndRandomSummary(database,dstDir,FileName)
        
