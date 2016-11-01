docName_file=open('docNameToDocId.txt','r')

docName_data_list=docName_file.readlines()
docName_Map={}
for line in docName_data_list:
    line=line.split()
    strName=" ".join(line[0:len(line)-1])
    docId=int(line[-1])
    docName_Map[strName]=docId
    
print docName_Map


