import os
mypath="C:\\Users\\mahmud\\workspace\\Socialcomp2016\\data\\"
mypath="F:\\Education\\4_2\\Thsis\\Dataset\\Dataset2_news_and_tweet\\"
#'C:\\Users\\mahmud\\workspace\\Socialcomp2016\\data\\'
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
print onlyfiles
