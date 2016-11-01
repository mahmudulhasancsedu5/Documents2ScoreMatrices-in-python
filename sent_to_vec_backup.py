docName_file=open('docNameToDocId.txt','r')



docName_data_list=docName_file.readlines()
docName_Map={}
for line in docName_data_list:
    line=line.split()
    strName=" ".join(line[0:len(line)-1])
    docId=int(line[-1])
    docName_Map[strName]=docId
    
#print docName_Map

sentenceToWordNumMap_file=open('sentenceToWordNumMap.txt','r')

sentenceToWordNumMap_list=sentenceToWordNumMap_file.readlines()


sentenceToWordNumMap_list=[line.split() for line in sentenceToWordNumMap_list]


vocaSize=int(sentenceToWordNumMap_list[0][0]) 
del sentenceToWordNumMap_list[0]


fileName="African runner murder(4)"
vecFile=open('African runner murder(4)_vec.txt','w')

#summaryFile=open(fileName,'r')
sentenceToWordNumMapFile=open('sentenceToWordNumMap.txt','r')
sentenceToWordNumMap_list=sentenceToWordNumMapFile.readlines()

sentenceToWordNumMap_list=[sentWord.split() for sentWord in sentenceToWordNumMap_list]
    
summaryFileID_int=docName_Map[fileName]

#print summaryFileID_int

DocSentWordMap=[sent for sent in sentenceToWordNumMap_list if sent[0]==str(summaryFileID_int)]



    
#----------------convert sentence to vector---------------------------
def sent2vec(sentWordList,vecSize):
    vec=[0 for x in range(vecSize)]
    for word in sentWordList:
        vec[int(word)]=1
    return vec
#---------------------test the code of sentence to vector-----------------

vecList=[]
vecStr=""
for sentword in DocSentWordMap:
    vec=sent2vec(sentword[3:],vocaSize)
    
    vecList.append(vec)
    
    vec=[str(x) for x in vec]
    vecStr+=' '.join(sentword[:3])
    vecStr+=' '
    vecStr+=' '.join(vec)
    vecStr+='\n'
    
#print vecList[0]
#print vecList[-1]
vecFile.write(vecStr)
from scipy.spatial import distance

#dist1=distance.cdist(vecList,vecList,'euclidean')

eu_dist1=distance.euclidean(vecList[0],vecList[1])
eu_dist2=distance.cityblock(vecList[0],vecList[1])
eu_dist3=distance.cosine(vecList[0],vecList[1])
eu_dist4=distance.correlation(vecList[0],vecList[1])
eu_dist5=distance.chebyshev(vecList[0],vecList[1])

eu_dist6=distance.dice(vecList[0],vecList[1])
eu_dist7=distance.jaccard(vecList[0],vecList[1])
eu_dist8=distance.hamming(vecList[0],vecList[1])


print 'euclidean dist = ',eu_dist1
print 'cityblock dist = ',eu_dist2
print 'cosine dist = ',eu_dist3
print 'correlation dist = ',eu_dist4
print 'chebyshev dist = ',eu_dist5
print 'dice dist = ',eu_dist6
print 'jaccard dist = ',eu_dist7
print 'hamming dist = ',eu_dist8
#print DocSentWordMap[-1]



#--------------------------------------------------------------
def lcs_length(a, b):
    table = [[0] * (len(b) + 1) for _ in xrange(len(a) + 1)]
    for i, ca in enumerate(a, 1):
        for j, cb in enumerate(b, 1):
            table[i][j] = (
                table[i - 1][j - 1] + 1 if ca == cb else
                max(table[i][j - 1], table[i - 1][j]))
    return table[-1][-1]
#---------------------------------------------------------------------
sent1=set(DocSentWordMap[0])
sent2=set(DocSentWordMap[1])

common=len(sent1.intersection(sent2))

print '% word of S1 in s2 = ',(common*1.00)/len(sent1)
print '% word of S2 in s2 = ',(common*1.00)/len(sent2)

print 'inclusion and exclution = ',common,len(sent1)+len(sent2)-common

print 'word overlap coefficient = ',(common*1.00)/min(len(sent1),len(sent2))





import jellyfish
#print vecList[:2]
v1=[str(x) for x in vecList[0]]
v2=[str(x) for x in vecList[1]]

v1=' '.join(v1)
v2=' '.join(v2)

from Levenshtein import distance
Levenshtein_dist=distance(v1,v2)
print 'levenshtein distance',Levenshtein_dist


print 'LCS =',lcs_length(DocSentWordMap[0],DocSentWordMap[1])

v1=unicode(v1,'utf-8')
v2=unicode(v2,'utf-8')
jaro_dist=jellyfish.jaro_distance(v1,v2)
print 'jaro distance',jaro_dist




#levenshtein_dist=jellyfish.levenshtein_distance(v1,v2)
#print 'levenshtein distance',levenshtein_dist

#damerau_levenshtein_dist=jellyfish.damerau_levenshtein_distance(v1,v2)
#print 'damerau_levenshtein distance',damerau_levenshtein_dist

#print dist1

docName_file.close()
vecFile.close()
sentenceToWordNumMapFile.close()
sentenceToWordNumMap_file.close()
    








