


def all_features(vec1,sent1,vec2,sent2):
    

    #dist1=distance.cdist(vecList,vecList,'euclidean')
    from scipy.spatial import distance
    eu_dist1=distance.euclidean(vec1,vec2)
    eu_dist2=distance.cityblock(vec1,vec2)
    eu_dist3=distance.cosine(vec1,vec2)
    #eu_dist4=distance.correlation(vec1,vec2)
    #eu_dist5=distance.chebyshev(vec1,vec2)

    eu_dist6=distance.dice(vec1,vec2)
    eu_dist7=distance.jaccard(vec1,vec2)
    #eu_dist8=distance.hamming(vec1,vec2)


    #print 'euclidean dist = ',eu_dist1
    #print 'cityblock dist = ',eu_dist2
    #print 'cosine dist = ',eu_dist3
    #print 'correlation dist = ',eu_dist4
    #print 'chebyshev dist = ',eu_dist5
    #print 'dice dist = ',eu_dist6
    #print 'jaccard dist = ',eu_dist7
    #print 'hamming dist = ',eu_dist8
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
    #-----------------------------------------------------------------
   
        
    #---------------------------------------------------------------------
    sent1=set(sent1)
    sent2=set(sent2)

    common=len(sent1.intersection(sent2))

    s1ins2=(common*1.00)/len(sent1)
    s2ins1=(common*1.00)/len(sent2)

    #print '% word of S1 in s2 = ',s1ins2
    #print '% word of S2 in s2 = ',s2ins1

    in_and_ex=common+(len(sent1)+len(sent2)-common)

    #print 'inclusion and exclution = ',in_and_ex

    word_overlap=(common*1.00)/min(len(sent1),len(sent2))

    #print 'word overlap coefficient = ',word_overlap


    v1=[str(x) for x in vec1]
    v2=[str(x) for x in vec2]

    v1=' '.join(v1)
    v2=' '.join(v2)

    from Levenshtein import distance
    Levenshtein_dist=distance(v1,v2)
    #print 'levenshtein distance',Levenshtein_dist

    lcs_dist=lcs_length(sent1,sent2)
    #print 'LCS =',lcs_dist

    v1=unicode(v1,'utf-8')
    v2=unicode(v2,'utf-8')
    import jellyfish
    jaro_dist=0
    #jaro_dist=jellyfish.jaro_distance(v1,v2)
    #print 'jaro distance',jaro_dist

    total_dist=(eu_dist1+eu_dist2+eu_dist3+eu_dist6+eu_dist7+s1ins2+s2ins1+in_and_ex+word_overlap+jaro_dist+Levenshtein_dist+lcs_dist)
    #print 'total dist = ',total_dist
    total_dist=(total_dist)/12

    #print 'total dist = ',total_dist

    return total_dist


    
    
