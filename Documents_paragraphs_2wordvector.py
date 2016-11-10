import os
import sys
import re



import preprocessor
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()

print 'ok'

stop_words=set(stopwords.words("english"))

mypath="C:\\Users\\mahmud\\workspace\\Socialcomp2016\\data\\"
mypath="F:\\Education\\4_2\\Thsis\\Dataset\\Dataset2_news_and_tweet\\"
#'C:\\Users\\mahmud\\workspace\\Socialcomp2016\\data\\'
doc_name_list = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]



docName_to_id_file=open('docNameToDocId.txt','w+')
sentenceMapFile=open('docSentMap.txt','w+')
tweetMapFile=open('doctweetMap.txt','w+')
vocaMapFile=open('vocaCorpus.txt','w+')
sentenceToWordNumMapFile=open('sentenceToWordNumMap.txt','w+')


voca_dict={}

Sentence_DocList=[]
Processed_DocList=[]
docNameToId_str=""

DocId=0
for name in doc_name_list:

    docFile=open(mypath+name,'r')
    text=docFile.read().split('\n\n')
    docFile.close()
    del text[3]
    Processed_DocList.append(text)
    Sentence_DocList.append(text)
    docNameToId_str+=str(name)+' '+str(DocId)+'\n'
    print DocId
    DocId+=1

docName_to_id_file.write(docNameToId_str) 
'''
for Doc in DocList:
    Doc.split('\n\n')
    Doc.replace('\n','')

'''
print 'Number of Doc = ',len(doc_name_list)
print 'Length of DocList = ',len(doc_name_list)
print 'Length of DocList each element = ',len(Processed_DocList[0])

sentStr=""
tweetStr=""
sentToWord_str=""


word_count=0

for doc_id in range(len(Processed_DocList)):
    print 'docunent = ',doc_id
    
    
    Doc_p=Processed_DocList[doc_id]
    Doc_ini=Sentence_DocList[doc_id]
    
    for  para_id in range(len(Doc_p)):
        if para_id==0:
            print 'Sentences of heading'
            
    
        if para_id==1:
            print 'Sentences of news'
            #doc_sen=Doc_p[para_id].replace('\n','').split('.')
            doc_sen=Doc_p[para_id].replace("\\","").split('\n')
            #doc_sen=[preprocessor.clean(sent) for sent in doc_sen]
            doc_sen=[preprocessor.clean(sent) for sent in doc_sen]
            doc_sen=[sent.encode('ascii','ignore') for sent in doc_sen]
            doc_sen=[re.sub('[~!@#$%^&*()_+\'\",\\-/|1234567890.=`]','',sent) for sent in doc_sen]
            
            Doc_p[para_id]=[x for x in doc_sen]
            Doc_ini[para_id]=[x for x in doc_sen]
            print 'news len = ',len(Doc_ini[para_id])
            #print Doc_ini[para_id]
            for sent_id in range(len(Doc_p[para_id])):
               
                ss=str(doc_id)+' '+str(para_id)+' '+str(sent_id)+' '+str(Doc_ini[para_id][sent_id])+'\n'
                sentStr+=ss;
                
                
                Doc_p[para_id][sent_id]=preprocessor.clean(Doc_p[para_id][sent_id])
                Doc_p[para_id][sent_id]=Doc_p[para_id][sent_id].lower()

                Doc_p[para_id][sent_id] = word_tokenize(Doc_p[para_id][sent_id])
                
                Doc_p[para_id][sent_id] = filter(lambda x: x not in string.punctuation, Doc_p[para_id][sent_id])

                Doc_p[para_id][sent_id] = filter(lambda x: x not in stop_words, Doc_p[para_id][sent_id])

                #print '--------',Doc_p[para_id][tweet_id]
                arr=[]
                for word in Doc_p[para_id][sent_id]:
                    #print word,type(word)
                    word=str(word.encode('ascii','ignore'))
                    x=str(porter.stem(str(word)))
                    #print x
                    arr.append(x)
                Doc_p[para_id][sent_id]=arr
                    

                
                #Doc_p[para_id][tweet_id]=[str(porter.stem(str(i))) for i in Doc_p[para_id][tweet_id]]

                #print Doc_p[para_id][sent_id]
                #Doc_p[para_id][tweet_id]=[str(porter.stem(i.lower())) for i in word_tokenize(Doc_p[para_id][tweet_id]) if i not in string.punctuation and  i.lower() not in stop_words ]
                sentToWord_str+=str(doc_id)+' '+str(para_id)+' '+str(sent_id)+' ';
                sent_word_numing=[]
                for word in Doc_p[para_id][sent_id]:
                    term=word in voca_dict
                    if term==False:
                        voca_dict[word]=word_count
                        print word,'----',voca_dict[word]
                        sent_word_numing.append(word_count)
                        word_count+=1
                        
                    else:
                        find_count=voca_dict[word]
                        sent_word_numing.append(find_count)

                xx=[str(x) for x in sent_word_numing]
                sentToWord_str+=' '.join(xx)+'\n'
                
                Doc_p[para_id][sent_id]=sent_word_numing
                
            
        if para_id==2:
            print 'Sentences of tweet',doc_name_list[doc_id]
            #Doc[para_id]='processed sent'
            doc_twt=Doc_p[para_id].replace("\\","").split('\n')
            Doc_p[para_id]=[x for x in doc_twt]
            Doc_ini[para_id]=[x for x in doc_twt]
            print 'tweet len = ',len(Doc_p[para_id])

            for tweet_id in range(len(Doc_p[para_id])):
                #Doc_p[para_id][tweet_id]=re.sub('[~!@#$%^&*()_+\'\",\\-/|1234567890.=`]','',Doc_p[para_id][tweet_id])
                #tt=str(doc_id)+' '+str(para_id)+' '+str(tweet_id)+' '+str(Doc_p[para_id][tweet_id])+'\n'
                #tweetStr+=tt
                
                Doc_p[para_id][tweet_id]=preprocessor.clean(Doc_p[para_id][tweet_id]).replace("\\","")
                Doc_p[para_id][tweet_id]=re.sub('[~!@#$%^&*()_+\'\",\\-/|1234567890.=`]','',Doc_p[para_id][tweet_id])

                tt=str(doc_id)+' '+str(para_id)+' '+str(tweet_id)+' '+str(Doc_p[para_id][tweet_id].encode('ascii','ignore'))+'\n'
                tweetStr+=tt
                sentStr+=tt
                
                Doc_p[para_id][tweet_id]=Doc_p[para_id][tweet_id].lower()
                

                Doc_p[para_id][tweet_id] = word_tokenize(Doc_p[para_id][tweet_id])
                
                Doc_p[para_id][tweet_id] = filter(lambda x: x not in string.punctuation, Doc_p[para_id][tweet_id])

                Doc_p[para_id][tweet_id] = filter(lambda x: x not in stop_words, Doc_p[para_id][tweet_id])

                #print '--------',Doc_p[para_id][tweet_id]
                arr=[]
                for word in Doc_p[para_id][tweet_id]:
                    #print word,type(word)
                    word=str(word.encode('ascii','ignore'))
                    x=str(porter.stem(str(word)))
                    #print x
                    arr.append(x)
                Doc_p[para_id][tweet_id]=arr
                    

                
                #Doc_p[para_id][tweet_id]=[str(porter.stem(str(i))) for i in Doc_p[para_id][tweet_id]]

                #print Doc_p[para_id][tweet_id]

                #Doc_p[para_id][tweet_id]=[str(porter.stem(i.lower())) for i in word_tokenize(Doc_p[para_id][tweet_id]) if i not in string.punctuation and  i.lower() not in stop_words ]
                sentToWord_str+=str(doc_id)+' '+str(para_id)+' '+str(tweet_id)+' ';
                #sentStr+=str(doc_id)+' '+str(para_id)+' '+str(tweet_id)+' '+str(Doc_p[para_id][tweet_id])+'\n';
                
                sent_word_numing=[]
                for word in Doc_p[para_id][tweet_id]:
                    term=word in voca_dict
                    if term==False:
                        voca_dict[word]=word_count
                        #print word,'----',word_count
                        sent_word_numing.append(word_count)
                        word_count+=1
                        
                    else: 
                        find_count=voca_dict[word]
                        sent_word_numing.append(find_count)
                
                Doc_p[para_id][tweet_id]=sent_word_numing     
                xx=[str(x) for x in sent_word_numing]
                sentToWord_str+=' '.join(xx)+'\n'        
                        

                    
                        
print voca_dict
#print sentToWord_str
print len(voca_dict)
print voca_dict['runner']

vocaStr=""
vocaList=[(k,v) for k,v in voca_dict.items()]
vocaList=sorted(vocaList)

vocaList=[str(vocaList[i][0])+' '+str(vocaList[i][1]) for i in range(len(vocaList))]
for x in vocaList:
    vocaStr+=x+'\n'

vocaMapFile.write(vocaStr) 
                
tweetMapFile.write(tweetStr)
sentenceMapFile.write(sentStr)

vocaNum=str(len(voca_dict))+'\n'
sentenceToWordNumMapFile.write(vocaNum)
sentenceToWordNumMapFile.write(sentToWord_str)

docName_to_id_file.close()
tweetMapFile.close()                               
sentenceMapFile.close()
sentenceToWordNumMapFile.close()
vocaMapFile.close()
        
