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
        
    return sent_to_all_tweet_score

    
    
    
    
