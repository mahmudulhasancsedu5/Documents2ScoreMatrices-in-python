
f1="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\SoRTE results\\African runner murder(3)_summary_\\African runner murder(3)_SoRTE_tweet_score.txt"
sFile1=open(f1,"r")
#sFile2=open(ScoreFileDir+Filename+"_PR_tweet_score.txt","r")

sData=sFile1.read().split('\n');
print sData
sData=[line.split() for line in sData if len(line)!=0]
print sData
TweetScoreList=[(float(line[1]),int(line[0])) for line in  sData]

print TweetScoreList
