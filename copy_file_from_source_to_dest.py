import os
import sys
from shutil import copyfile


def createSummaryFolder(FileName,src,dst):

    
    SummaryDir=dst+"\\"+FileName+"_SoRTE_ROUGE\\"
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
    srcFolder=src+FileName+"_summary_\\"
    s1name=FileName+"_PRSentSummary.txt"
    s2name=FileName+"_PRTweetSummary.txt"
    s3name=FileName+"_SoRTESentSummary.txt"
    s4name=FileName+"_SoRTETweetSummary.txt"
    s5name=FileName+"_SoRTESingleWingSentSummary.txt"
    s6name=FileName+"_SoRTESingleWingTweetSummary.txt"
    copyfile(srcFolder+s1name, systemDir+s1name)
    copyfile(srcFolder+s2name, systemDir+s2name)
    copyfile(srcFolder+s3name, systemDir+s3name)
    copyfile(srcFolder+s4name, systemDir+s4name)
    copyfile(srcFolder+s5name, systemDir+s5name)
    copyfile(srcFolder+s6name, systemDir+s6name)

    database="F:\\Education\\4_2\\Thsis\\Dataset\\Dataset2_news_and_tweet\\"
    docFile=open(database+FileName,'r')
    text=docFile.read().split('\n\n')
    docFile.close()
    
    HighLight=text[0]
    referanceSummaryFile=open(referenceDir+FileName+'_reference1.txt','w')

    str_ref="";

    HighlightSentList=HighLight.split('\n')

    for line in HighlightSentList:
        
         str_ref+=str(line)
         str_ref+="\n"
    referanceSummaryFile.write(str_ref)
    referanceSummaryFile.close()
    
    
    





destFolder="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\SoRTE results\\SoRTE_ROUGE-1\\"
srcFolder="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\SoRTE results\\"

if not os.path.exists(destFolder):
    print 'Not exist'
    os.makedirs(destFolder)
else:
    print 'exist'
    
for i in range(2,9):
    FileName="African runner murder("+str(i)+")"
    createSummaryFolder(FileName,srcFolder,destFolder)
    
