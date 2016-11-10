import networkx as nx

def PreProcessingPageRankForFileInput(scoreFileName):
    inputFile=open(scoreFileName,'r')
    data=inputFile.readlines()
    dataArr=[]
    for line in data:
        dataArr.append(line.split())
    return dataArr

def createGraph(graphMat,typeMat):

    gr=nx.Graph()
    rowLen=len(graphMat)
    clmLen=len(graphMat[0])
    typeMat=typeMat[0]
    for i in range(rowLen):
        for j in range(clmLen):
            u=typeMat[0]+str(i)
            v=typeMat[1]+str(j)
            gr.add_nodes_from([u])
            gr.add_nodes_from([v])
            gr.add_edge(u,v,weight=float(graphMat[i][j]))
    return gr

def createGraphMultipleMatInput(graphMatArr,detectMatType):

    gr=nx.Graph()
    nodeSet=[]
    for graphMat in graphMatArr:
        rowLen=len(graphMat)
        print rowLen
        clmLen=len(graphMat[0])
        print clmLen
        MatType=detectMatType[0]
        del detectMatType[0]
        
        for i in range(rowLen):
            for j in range(clmLen):
                u=MatType[0]+str(i)
                v=MatType[1]+str(j)
                if u not in nodeSet:
                    nodeSet.append(u)
                    gr.add_nodes_from([u])
                if v not in nodeSet:
                    nodeSet.append(v)
                    gr.add_nodes_from([v])

                #print u,v,graphMat[i][j],'\n'
                gr.add_edge(u,v,weight=float(graphMat[i][j]))
    return gr

def TexRank(graphMat,typeMat):
    #gr=createGraph(graphMat,typeMat)
    gr=createGraphMultipleMatInput(graphMat,typeMat)
    gr_node_score=nx.pagerank(gr,weight='weight')
    return gr_node_score

def diff_sent_tweet_score(gr_node_score):
    tweetScore=[]
    sentScore=[]
    for key,val in gr_node_score.iteritems():
        temp=(float(val),int(key[1:]))
        if key[0]=='t':
            tweetScore.append(temp)
        else:
            sentScore.append(temp)
            
    SentScoreSorted=sorted(sentScore)
    SentScoreSorted.reverse()
    TweetScoreSorted=sorted(tweetScore)
    TweetScoreSorted.reverse()
    print 'Sent pagerank score',SentScoreSorted[:5]
    print 'Tweet page rank score = ',TweetScoreSorted[:5]
    return SentScoreSorted,TweetScoreSorted
    
#---------------------------------------------------------------------
scoreFileName='African runner murder(4)_sent2tweet_score_test.txt'

dataMat=PreProcessingPageRankForFileInput(scoreFileName)
dataMat=[dataMat]

typeMat=[('s','t')]
#node_score=TexRank(dataMat,typeMat)
node_score=TexRank(dataMat,typeMat)

sentScore,tweetScore=diff_sent_tweet_score(node_score)
#---------------------------------------------------------------------

'''
mat=[[1,0,1,7],[2,3,5,-10]]

inputFile=open('African runner murder(4)_sent2tweet_score_test.txt','r')
data=inputFile.readlines()
dataArr=[]
for line in data:
    dataArr.append(line.split())

gr=createGraph(dataArr)

node_ranking=nx.pagerank(gr,weight='weight')

tweetScore=[]
sentScore=[]
for key,val in node_ranking.iteritems():
    temp=(float(val),int(key[1:]))
    if key[0]=='t':
        tweetScore.append(temp)
    else:
        sentScore.append(temp)
        
SentScoreSorted=sorted(sentScore)
SentScoreSorted.reverse()
TweetScoreSorted=sorted(tweetScore)
TweetScoreSorted.reverse()
print 'Sent pagerank score',SentScoreSorted[:5]
print 'Tweet page rank score = ',TweetScoreSorted[:5]
'''
        
