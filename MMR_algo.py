from scipy.spatial import distance
import numpy
import math
def MMR(Sent_ScoreList,SentVecList,summaryLen):

    Sent_ScoreListVal=[val for (val,ind) in Sent_ScoreList]
    Sent_ScoreListInd=[ind for (val,ind) in Sent_ScoreList]

    max_val=max(Sent_ScoreListVal)
    Sent_ScoreListVal=[max_val-val for val in Sent_ScoreListVal]
    Sent_ScoreList=[(Sent_ScoreListVal[0],Sent_ScoreListInd[i]) for i in range(len(Sent_ScoreListVal))]
    
    selectedVecSent.append(SentVecList[0])
    del SentVecList[0]
    selectedScore=[]
    selectedScore.append(Sent_ScoreList[0])
    del Sent_ScoreList[0]

    i=1
    while i<summaryLen:

        distMat=distance.cdist(selectedVecSent,SentVecList,'cosine')

        min_val=distMat.argmin()
        max_val=distMat.argmax()
        distMat=max_val-distMat
        row_column=numpy.unravel_index(max_val, distMat.shape)

        selectedSent_ind=row_column[0]
        newLySelected_ind=row_column[1]

        

        i+=1

def MMR2(SentScoreList,SentVecList,summaryLen):
    print 'MMR2 start'

    scors=[x[0] for x in SentScoreList]
    max_score=max(scors)
    new_scoreList=[(max_score-x[0],x[1]) for x in SentScoreList]
    
    SentScoreList=[x for x in new_scoreList]
    
    UnselectedScore=[x for x in SentScoreList]
    
    UnselectedScore=sorted(UnselectedScore)
    print UnselectedScore
    SelectedScore=[]
    SelectedScore.append(UnselectedScore[-1])
    del UnselectedScore[-1]

    


    while len(SelectedScore)<summaryLen and len(UnselectedScore)!=0:
        print 'selected before= ',SelectedScore
        print 'unselected before = ',UnselectedScore

        UnSelected_temp=[]
        for u in UnselectedScore:
            max_sim=0
            
            for v in SelectedScore:
                vec1=SentVecList[u[1]]
                vec2=SentVecList[v[1]]
                sim=0
                if numpy.linalg.norm(vec1)!=0 and numpy.linalg.norm(vec2)!=0:
                    sim=1-distance.cosine(vec1,vec2)

                #print u,v,sim
                if sim > max_sim:
                    max_sim=sim
             
            if max_sim>0.75:
                print 'big'
                new_score=0.0
            else:
                new_score=u[0]
            new_touple=(new_score,u[1])
            #print max_sim,new_touple
            
            UnSelected_temp.append(new_touple)
            #print 'temp = ',UnSelected_temp
            
        
        UnselectedScore= sorted(UnSelected_temp)
        if len(UnselectedScore)==0:
            break
        SelectedScore.append(UnselectedScore[-1])
        del UnselectedScore[-1]
        print 'selected after= ',SelectedScore
        print 'unselected after = ',UnselectedScore
        
    print 'MMR2 end'
    print SelectedScore
    return SelectedScore
    
            
def MMR3_sim(SentScoreList,SentVecList,summaryLen):
    print 'MMR2 start'

    scors=[x[0] for x in SentScoreList]
    max_score=max(scors)
    new_scoreList=[(max_score-x[0],x[1]) for x in SentScoreList]
    
    SentScoreList=[x for x in new_scoreList]
    
    UnselectedScore=[x for x in SentScoreList]
    
    UnselectedScore=sorted(UnselectedScore)
    print UnselectedScore
    SelectedScore=[]
    SelectedScore.append(UnselectedScore[-1])
    del UnselectedScore[-1]

    


    while len(SelectedScore)<summaryLen and len(UnselectedScore)!=0:
        print 'selected before= ',SelectedScore
        print 'unselected before = ',UnselectedScore

        UnSelected_temp=[]
        for u in UnselectedScore:
            max_sim=0
            
            for v in SelectedScore:
                vec1=SentVecList[u[1]]
                vec2=SentVecList[v[1]]
                sim=0
                
                if numpy.linalg.norm(vec1)!=0 and numpy.linalg.norm(vec2)!=0:
                    sim=1-distance.cosine(vec1,vec2)

                #print u,v,sim
                if sim > max_sim:
                    max_sim=sim
            '''
            if max_sim>0.75:
                print 'big'
                new_score=0.0
            else:
                new_score=u[0]
            '''
            new_score=u[0]-max_sim*u[0]
                
            new_touple=(new_score,u[1])
            #print max_sim,new_touple
            
            UnSelected_temp.append(new_touple)
            #print 'temp = ',UnSelected_temp
            
        
        UnselectedScore= sorted(UnSelected_temp)
        if len(UnselectedScore)==0:
            break
        SelectedScore.append(UnselectedScore[-1])
        del UnselectedScore[-1]
        print 'selected after= ',SelectedScore
        print 'unselected after = ',UnselectedScore
        
    print 'MMR2 end'
    print SelectedScore
    return SelectedScore


def MMR3_dist(SentScoreList,SentVecList,summaryLen):
    print 'MMR2 start'

    scors=[x[0] for x in SentScoreList]
    max_score=max(scors)
    new_scoreList=[(max_score-x[0],x[1]) for x in SentScoreList]
    
    SentScoreList=[x for x in new_scoreList]
    
    UnselectedScore=[x for x in SentScoreList]
    
    UnselectedScore=sorted(UnselectedScore)
    print UnselectedScore
    SelectedScore=[]
    SelectedScore.append(UnselectedScore[-1])
    del UnselectedScore[-1]

    


    while len(SelectedScore)<summaryLen and len(UnselectedScore)!=0:
        print 'selected before= ',SelectedScore
        print 'unselected before = ',UnselectedScore

        UnSelected_temp=[]
        for u in UnselectedScore:
            max_sim=0
            min_dist=1
            
            for v in SelectedScore:
                vec1=SentVecList[u[1]]
                vec2=SentVecList[v[1]]
                sim=0
                dist=0
                
                if numpy.linalg.norm(vec1)!=0 and numpy.linalg.norm(vec2)!=0:
                    dist=distance.cosine(vec1,vec2)

                #print u,v,sim
                if dist < min_dist:
                    min_dist=dist
            '''
            if max_sim>0.75:
                print 'big'
                new_score=0.0
            else:
                new_score=u[0]
            '''
            new_score=u[0]-min_dist*u[0]
                
            new_touple=(new_score,u[1])
            #print max_sim,new_touple
            
            UnSelected_temp.append(new_touple)
            #print 'temp = ',UnSelected_temp
            
        
        UnselectedScore= sorted(UnSelected_temp)
        if len(UnselectedScore)==0:
            break
        SelectedScore.append(UnselectedScore[-1])
        del UnselectedScore[-1]
        print 'selected after= ',SelectedScore
        print 'unselected after = ',UnselectedScore
        
    print 'MMR2 end'
    print SelectedScore
    return SelectedScore 
    

    
    
    
#--------------------------------test MMR--------------------------
'''
SentVecList=[[1,1,1,0],[0,0,0,0],[1,1,1,0],[1,1,0,0],[1,1,1,0]]
SentScoreList=[(6,0),(4,1),(1,2),(9,3),(0,4)]
SentScoreList=sorted(SentScoreList)
summaryLen=3
scores=MMR2(SentScoreList,SentVecList,summaryLen)
'''

#------------------------------------------------------------------
