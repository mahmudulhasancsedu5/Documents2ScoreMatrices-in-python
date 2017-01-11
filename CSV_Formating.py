import csv


allResults=[]
dicT={}
dicInt2Str1={}
dicInt2Str2={}
'''
'SORTESENTSUMMARY.TXT'
'SORTETWEETSUMMARY.TXT'
'SORTESINGLEWINGSENTSUMMARY.TXT'
'SORTESINGLEWINGTWEETSUMMARY.TXT'
'PRSENTSUMMARY.TXT'
'PRTWEETSUMMARY.TXT'
'MMRPRTWEETSUMMARY.TXT'
'MMRSORTETWEETSUMMARY.TXT'

'SENTLEADNEWSSUMMARY.TXT'
'RANDOMTWEETSUMMARY.TXT'
'RANDOMNEWSSUMMARY.TXT'
'TWEETLEADNEWSSUMMARY.TXT'


'Avg_Recall'
'Avg_Precision'
'Avg_F-Score'

'''
dicT['Avg_Recall']=1
dicT['Avg_Precision']=0
dicT['Avg_F-Score']=2

dicInt2Str2[1]='Avg_Recall'
dicInt2Str2[0]='Avg_Precision'
dicInt2Str2[2]='Avg_F-Score'

dicT['SORTESENTSUMMARY.TXT']=0
dicT['SORTETWEETSUMMARY.TXT']=1
dicT['SORTESINGLEWINGSENTSUMMARY.TXT']=2
dicT['SORTESINGLEWINGTWEETSUMMARY.TXT']=3
dicT['PRSENTSUMMARY.TXT']=4
dicT['PRTWEETSUMMARY.TXT']=5

dicT['MMRSORTETWEETSUMMARY.TXT']=6
dicT['MMRPRTWEETSUMMARY.TXT']=7

dicT['SENTLEADNEWSSUMMARY.TXT']=8
dicT['RANDOMTWEETSUMMARY.TXT']=9
dicT['RANDOMNEWSSUMMARY.TXT']=10
dicT['TWEETLEADNEWSSUMMARY.TXT']=11

dicInt2Str1[0]='SORTESENTSUMMARY.TXT'
dicInt2Str1[1]='SORTETWEETSUMMARY.TXT'
dicInt2Str1[2]='SORTESINGLEWINGSENTSUMMARY.TXT'
dicInt2Str1[3]='SORTESINGLEWINGTWEETSUMMARY.TXT'
dicInt2Str1[4]='PRSENTSUMMARY.TXT'
dicInt2Str1[5]='PRTWEETSUMMARY.TXT'

dicInt2Str1[6]='MMRSORTETWEETSUMMARY.TXT'
dicInt2Str1[7]='MMRPRTWEETSUMMARY.TXT'

dicInt2Str1[8]='SENTLEADNEWSSUMMARY.TXT'
dicInt2Str1[9]='RANDOMTWEETSUMMARY.TXT'
dicInt2Str1[10]='RANDOMNEWSSUMMARY.TXT'
dicInt2Str1[11]='TWEETLEADNEWSSUMMARY.TXT'

TotalResult=[[[],[],[]]
             ,[[],[],[]]
             ,[[],[],[]]
             ,[[],[],[]]
             ,[[],[],[]]
             ,[[],[],[]]
             ,[[],[],[]]
             ,[[],[],[]]
             ,[[],[],[]]
             ,[[],[],[]]
             ,[[],[],[]]
             ,[[],[],[]]]


def csvFormat(Directory,FileName):
    print ""
    csvFile=open(Directory+FileName,'rb')

    Data=csv.reader(csvFile,delimiter=',',quotechar='|')



    i=0

    ColumnRow=[]
    pairList=[]
    
    dr=[]
    for row in Data:
        if i==0:
            ColumnRow=row[2:-1]
            #print ColumnRow
        else:
            dr.append(row[2:-1])

            row_small=row[2:-1]
            
            TotalResult[dicT[row_small[0]]][dicT[ColumnRow[1]]].append(float(row_small[1]))
            TotalResult[dicT[row_small[0]]][dicT[ColumnRow[2]]].append(float(row_small[2]))
            TotalResult[dicT[row_small[0]]][dicT[ColumnRow[3]]].append(float(row_small[3]))
        
            pair=( row_small[0], row_small[1], row_small[2], row_small[3])
            #print pair
            
        i=i+1
    allResults.append(dr)
    
    print TotalResult
    
        


#Directory="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\SoRTE results\\SoRTE_ROUGE-1\\"
#Directory="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\SoRTE results\\MMR Summary Results\\"
Directory="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\Sentence Lead\\"
from os import listdir

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

files=find_csv_filenames( Directory, suffix=".csv" )
print files
for FileName in files:
    print FileName
    #FileName="Aurora shooting("+str(i)+")_results.csv"
    print FileName
    csvFormat(Directory,FileName)





S="Summary Type"
p='Avg_Precision'
r='Avg_Recall'
f='Avg_F-Score'
res_res=""
res_res+="%-50s"%(S)
res_res+="%20s"%(p)
res_res+="%20s"%(r)
res_res+="%20s"%(f)
res_res=str(res_res)+"\n"
i=0
for s3 in TotalResult:

    res_line=""
    #res_line+=dicInt2Str1[i]

    res_line+="%-50s"%(dicInt2Str1[i])
    j=0
    for s in s3:

        #res_line+=" "+dicInt2Str2[j]+"      "+str(sum(s)/len(s))+"  "
        #res_line+="      "+str(sum(s)/len(s))+"  "
        if len(s)!=0:
            res_line+="%20f"%(sum(s)/len(s))
        
        j=j+1
    
    #print res_line,"\n"

    res_res+=str(res_line)+"\n"
    
    i=i+1
print res_res

resFile=open(Directory+"ROUGE-1_RESULT_AVG.txt","w")
resFile.write(res_res)
resFile.close()
