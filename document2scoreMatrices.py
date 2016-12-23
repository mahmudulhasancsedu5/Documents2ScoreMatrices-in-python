import gc
from bitarray import bitarray

def sent2vec(sentWordList,vecSize):
    #vec=[0 for x in range(vecSize)]
    vec=[False]*vecSize
    for word in sentWordList:
        vec[int(word)]=True
    return vec

def doc2vec(DocSentWordMap,vocaSize):
    vecList=[]
    vecStr=""
    wordList=[]
    
    for sentword in DocSentWordMap:
        print sentword[2:3]
        vec=[int(x) for x in sentword[:3]]
        vec+=sent2vec(sentword[3:],vocaSize)
        #gc.collect()
        vecList.append(vec)
        
        words=sentword[:]
        wordList.append(words)
        
        '''
        vec=[str(x) for x in vec]
        vecStr+=' '.join(vec)
        '''
        
     
    return vecList,vecStr,wordList

def seperateSentTweetVec(vecList,wordList):
    print "do work"
    vecList_len=len(vecList)
    
    newsvecList=[vecList[i] for i in range(vecList_len) if vecList[i][1]==1]
    newswordList=[wordList[i] for i in range(vecList_len) if wordList[i][1]=='1']

    tweetvecList=[vecList[i] for i in range(vecList_len) if vecList[i][1]==2]
    tweetwordList=[wordList[i] for i in range(vecList_len) if wordList[i][1]=='2']
    
    return newsvecList,newswordList,tweetvecList,tweetwordList


from rteScore import all_features 
def oneSentToManyTweet_score(sent_i_vec,sent_i_words,tweetVecSet,tweetWordSet):

    score_sent_i=0;

    tweetVecSet_len=len(tweetVecSet)

    sent_to_all_tweet_score=[]
    for i in range(tweetVecSet_len):
        tweet_vec=tweetVecSet[i]
        tweet_words=tweetWordSet[i]
        
        result = all_features(sent_i_vec,sent_i_words,tweet_vec,tweet_words)
        sent_to_all_tweet_score.append(result)
        print 'res = ',result
    #gc.collect()   
    return sent_to_all_tweet_score

def set2setScore(newsVecList,newsWordList,tweetVecList,tweetWordList):
    print 'set2setScore start'

    sentSet_tweetSet_2d_score=[]
    newsVecList_len=len(newsVecList)
    
    for ind in range(newsVecList_len):
        print 'sent = ',ind
        sent_to_tweetSet_score_arr = oneSentToManyTweet_score(newsVecList[ind],newsWordList[ind],tweetVecList,tweetWordList)
        sentSet_tweetSet_2d_score.append(sent_to_tweetSet_score_arr)
    #gc.collect()
    return sentSet_tweetSet_2d_score
    
    
    

def allSet2allSet_score(newsVecList,newsWordList,tweetVecList,tweetWordList):
    print 'doc2scoreMat start'

    
    #sentences to sentences score mat
    sentSet2sentSet_score_2d_List=set2setScore(newsVecList,newsWordList,newsVecList,newsWordList)
    
    #sentences to tweet score  mat
    sentSet2tweetSet_score_2d_List=set2setScore(newsVecList,newsWordList,tweetVecList,tweetWordList)
    
    #tweet to tweets score mat
    tweetSet2tweetSet_score_2d_List=set2setScore(tweetVecList,tweetWordList,tweetVecList,tweetWordList)


    #tweet to sentences score mat

    tweetSet2sentSet_score_2d_List=set2setScore(tweetVecList,tweetWordList,newsVecList,newsWordList)

    #gc.collect()
    return sentSet2sentSet_score_2d_List,sentSet2tweetSet_score_2d_List,tweetSet2tweetSet_score_2d_List,tweetSet2sentSet_score_2d_List
    
        
    
