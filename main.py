__author__ = 'Mohammad Mollaahmadi & Danial Ebrahimzadeh'

import os
import stem
import stemming
import csv
import sqlite3
import datetime
#database1 = sqlite3.connect('base.sqlite')
#database = database1.cursor()
''' ---------------------------- Global Var ---------------------------- '''
''' Int Var '''
CollocLimit = 20
LenText = 0

''' String Var '''
print('start project in time: ', datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
if not os.path.exists('output-files'):
    os.makedirs('output-files')
path_of_input_file = 'news-input/fulltexttable2.csv'
path_of_output_file = 'output-files'
AllText = ' '
AllTextStemmed = ' '
TextSplit = ''
TextTempG = ''

''' List Var '''
CollArr2 = []
CollStemArr2 = []
CollArr3 = []
CollStemArr3 = []
RecordsWithTagArray = []
ListAllText = []
ListAllTextTags = []
ListAllTextStem = []
ListAllTextStemTags = []
ListAllTextAndMyword = []

''' Class Var '''

FWSO = stem.WordsStem()
SRFWO= stemming.Stemming()

'''..........................................................................'''
def Select_DeleteBadRecord():
	databaseRow = []
	RecordWithTagArrayTemp = []
	with open(path_of_input_file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			databaseRow.append((row['fulltext'],))
    #print('database records = ',databaseRow)
    #databaseRow=DBCO.randomid()
	print('\n Please wait. The Selecting and Remove Bad Records takes several Minutes ...')
	for row in databaseRow:
		if (len( str(row) ) > 200 and (str(row)).count("**") <= 1):
			MyText = FWSO.ReplaceBadWords(str(row),1)
			#if (len( MyText ) > 150 and ind<10):
			if (len( MyText ) > 150 ):
				RecordsWithTagArray.append(MyText)
				RecordWithTagArrayTemp.append(MyText)
	with open(path_of_output_file + '/BestRecordTL.csv', 'w') as f:
		fieldnames = [['Text']]
		writer = csv.writer(f)
		writer.writerows(fieldnames)
		writer.writerows(RecordWithTagArrayTemp)
	del RecordWithTagArrayTemp
	#print('database record first change = ' , RecordsWithTagArray)
	path_of_input_directory = 'input-stemming-files'
	os.mkdir(path_of_input_directory)
	input_file = open(path_of_input_directory + '/input.txt', "w+", encoding="utf8")
	for sentence in RecordsWithTagArray:
		# if sentence have \n then replace it with whitespace
		#if sentence.find("\n") > -1:
		sentence = sentence.replace("\n", " ")
		#print('sentence = ',sentence)
		# print result of process sentence into output file
		input_file.write(sentence)
	input_file.close()
	print('start stemming part of project in = ', datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
	SRFWO.StemmingFile()
	print('finish stemming part of project in = ', datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
	
	
''' ----------------  Select best record from output database  -------------'''
def SelectBestRecordFunc():
	global AllText
	output_file= open('output-stemming-files/stemming-output-of-input.txt',"r",encoding="utf8")
	BestRDRow = output_file.readlines()
	output_file.close()
	if len(BestRDRow) > 1:
		BestRDRow = [''.join(BestRDRow)]
	with open(path_of_output_file + '/BestRecordStemmingTL.csv', 'w') as f:
		fieldnames = [['Text']]
		writer = csv.writer(f)
		writer.writerows(fieldnames)
		writer.writerows(BestRDRow)
	temp_str = ''
	for row in BestRDRow:
		MyText = str(row)
		MyText = FWSO.ReplaceBadWords(str(row),0)
		temp_str=temp_str+MyText
		RecordsWithTagArray.append(MyText)
	#print('bestRDRow = ', BestRDRow)
	print('\n Please wait. The Selecting Database takes several Minutes ...')
	AllText = FWSO.ReplaceBadWords(temp_str,0)
	#print('temp_str = ',temp_str)
	#print('AllText = ',AllText)
    #print('database record second change = ',RecordsWithTagArray)

''' ----------------  Make Alltext And AllTextStem and use tagger and chunker function to make WordTag array  -------------'''
def MakeAllTextFunc():
	global AllText
	global ListAllText
	global ListAllTextAndMyword
	
	LenStr = str(len(RecordsWithTagArray))
	#print('record with tag arr = ', RecordsWithTagArray , 'len = ',LenStr)
	i = 0
	for row in  RecordsWithTagArray:
		MyText = row
		MyText = FWSO.ReplaceBadWords(str(row),0)
		AllText = AllText + MyText
		i = i + 1
    #print('alltext = ', AllText)
	TaggerFunc(1)
	print( '\n The Tagger Function is finished.')
	#AllText = ''
	TempText = ''
	jj = 0

	ListLen = len(ListAllText)
	while jj < ListLen-1:
		Myword = ''
		list_temp = []
        #print('listalltext[jj] = [',jj ,']',ListAllText[jj])
		for subword in ListAllText[jj]:
			Myword = Myword + subword
            #print('subword = ',subword)
            #print('myword = ',Myword)
        #TempText = TempText + Myword
		list_temp.extend((Myword,ListAllText[jj]))
		ListAllTextAndMyword.append(list_temp)
        #DBCO.InsertWord_TagTL(Myword,ListAllTextTags[jj])
		jj = jj + 1
        #if(jj% 20000==0):
           # AllText = AllText + TempText
            #TempText = ''
	with open(path_of_output_file + '/Word_TagTL.csv', 'w') as f:
		fieldnames = [['Word', 'Tag']]
		writer = csv.writer(f)
		writer.writerows(fieldnames)
		writer.writerows(ListAllTextAndMyword)
	AllText = AllText + TempText
	with open(path_of_output_file + '/AllTextTL.csv', 'w') as f:
		writer = csv.writer(f)
		fieldnames = [['Text']]
		writer.writerows(fieldnames)
		l = []
		l.append(AllText)
		writer.writerows(l)
	del l

''' ----------------  Select AllText And WordTag from output database  -------------'''
def SelectAllTextFunc():
	global AllText
	global AllTextStemmed
	global ListAllText
	global ListAllTextTags
	global ListAllTextStem
	global ListAllTextStemTags
	global ListAllTextAndMyword
	print( '\n Please wait. The Selecting Database takes several Minutes ... \n\tNote:Your free memory should be about than 2GB. ')
    # select Alltext
	for row in  ListAllTextAndMyword:
		MyWord = str(row[0]).split()
		MyTag = str(row[1])
		ListAllText.append(MyWord)
		ListAllTextTags.append(MyTag)
	print (' \nFinish selecting Word_Tag from database')
    #print('ListAllText = ',ListAllText)
    #print('ListAllTextTags = ',ListAllTextTags)


''' ----------------  Call Collcations functions  -------------'''
def MakeCollocationsFunc():
	print('start collocation 2 version = ' , datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
	MakeCollV2(0)
	print('finish collocation 2 version and start 3 version in time = ' , datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
	MakeCollV3(0)
	print('finish collocation 3 version and all collocation in = ' , datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))


''' ----------------  Detect Collocation in V2 And insert to output database  -------------'''
def MakeCollV2(stem):
	global AllText
	global AllTextStemmed
	global ListAllText
	global ListAllTextTags
	global ListAllTextStem
	global ListAllTextStemTags
	if(stem == 0):
		ResultCollocation2 = []
		print ('\nStarting Make CollV2 With Original Text')
		TextTemp = AllText
		TextL = ListAllText
		TextTagL = ListAllTextTags
		TextSplitL = ListAllText
		LenTextL = len(ListAllText)
		#print('AAAAAAAAAAALtext = ',AllText)
        #print('TextTemp = ',TextTemp)
        #print('ListAllText = ',ListAllText)
        #print('TextL = ',TextL)
        #print('ListAllTextTag = ',ListAllTextTags)
        #print('TextTagL = ',TextTagL)
		#print('TextSplitL = ',TextSplitL)
		#print('Len = ',LenTextL)
	coll_count = 0
	colar = []
	i = 0
	j=0
	while i < LenTextL -1:
		word1 = TextSplitL[i]
		word2 = TextSplitL[i+1]
        #print(i,'    word1 = ',word1,'   word2 = ',word2)
		if(not (word1 + word2) in colar):
            #if(TextTagL[i+1]=='X'):
                #if(not (TextTagL[i]=='S' or TextTagL[i]=='X')):
					coll_count = coll_count + 1
					www1 = ''
					www2 = ''
					for subword in word1:
						www1 = www1 + subword
                    #print(www1)
					for subword in word2:
						www2 = www2 + subword
					jj = 0
					o11 = 0
					o12 = 0
					o21 = 0
					o11 = TextTemp.count(www1 + ' ' + www2)
                    #print('   www1 = ',www1,'   www2 = ',www2)
					if (o11 > CollocLimit):
						o12 = TextTemp.count(' ' +www1)
						o21 = TextTemp.count(' ' +www2)
                        #print ('In Coll2 ==> Word :: ' , i , '\tFrom :: ',LenTextL)
						o12 = o12 - o11
						o21 = o21 - o11
						o22 = LenTextL - (o11 + o12 + o21)
						colar.append(word1 + word2)
						#if ((word1+word2) in colar):
							#print('111111111')
						ListCollocation2Temp = []
						ListCollocation2Temp.extend((o11,o12,o21,o22,www1,www2))
						ResultCollocation2.append(ListCollocation2Temp)
		i = i + 1
	with open(path_of_output_file + '/CollV2TL.csv', 'w') as f:
		fieldnames = [["O11", "O12", "O21", "O22", "Word1", "Word2"]]
		writer = csv.writer(f)
		writer.writerows(fieldnames)
		writer.writerows(ResultCollocation2)
	del ResultCollocation2


''' ----------------  Detect Collocation in V3 And insert to output database  -------------'''
def MakeCollV3(stem):
	i = 0
	colar = []
	coll_count = 0
	global ListAllText
	global ListAllTextTags
	global ListAllTextStem
	global ListAllTextStemTags
	global LenText
	global TextSplit
	global TextTagSplit
	global AllTextStemmed
	global AllText
	global TextTempG
	if(stem == 0):
		ResultCollocation3 = []
		print ('\nStarting Make CollV3 With Original Text')
		TextTempG = AllText
		TextSplit = ListAllText
		TextTagSplit = ListAllTextTags
		LenText = len(ListAllText)
		#print('TextTempG = ',TextTempG)
		#print('TextSplit = ',TextSplit)

	while i < LenText - 2:
		word1 = TextSplit[i]
		word2 = TextSplit[i+1]
		word3 = TextSplit[i+2]
		if(not (word1 + word2 + word3) in colar):
            #if( TextTagSplit[i+2]=='X'):
                #StopRes = IsStopWords2(TextTagSplit[i],TextTagSplit[i+1])
                #if(StopRes == 0 or StopRes == 1):
					coll_count = coll_count + 1
                    #print('')
                    #Stop2Bool = False
                    #if (StopRes == 1):
                        #Stop2Bool = True
                        #i = i + 1
					jj = 0
					O111 = 0
					www1 = ''
					www2 = ''
					www3 = ''
					for subword in word1:
						www1 = www1 + subword
					for subword in word2:
						www2 = www2 + subword
					for subword in word3:
						www3 = www3 + subword
					O111 = TextTempG.count(www1 + ' ' + www2 + ' ' + www3)
					if (O111 > CollocLimit):
                        #print ('In Coll3 ==> Word :: ' , i , '\tFrom :: ',LenText)
						O111Temp,O112,O121,O122,O211,O212,O221,O222  = NumberOfWordComplete(www1,www2,www3,word1,word2,word3)
						ListCollcation3Temp = []
						ListCollcation3Temp.extend((O111, O112, O121, O122, O211, O212, O221, O222, www1, www2, www3))
						ResultCollocation3.append(ListCollcation3Temp)
						colar.append(word1 + word2 + word3)
                #else:
                    #if(StopRes == 3):
                        #i = i + 1
            #else:
                #i = i + 2
		i = i + 1
	with open(path_of_output_file + '/CollV3TL.csv', 'w') as f:
            fieldnames = [["O111", "O112", "O121", "O122", "O211", "O212", "O221", "O222", "Word1", "Word2", "Word3"]]
            writer = csv.writer(f)
            writer.writerows(fieldnames)
            writer.writerows(ResultCollocation3)
	del ResultCollocation3

''' ----------------  Detect StopWords  -------------'''
def IsStopWords2(Tagword1,Tagword2):
    if (Tagword2=='X'):
        return 3
    res = 0
    if ((Tagword1=='S' or Tagword1=='X')):
        res = res + 2
    if ((Tagword2=='S')):
        res = res + 1
    return res

''' ----------------  Detect Oijk For Coll in V3  -------------'''
def NumberOfWordComplete(www1,www2,www3,word1,word2,word3):
    Lindex = 0
    O111 = 0
    O112 = 0
    O121 = 0
    O122 = 0
    O211 = 0
    O212 = 0
    O221 = 0
    O222 = 0
    global TextSplit
    global TextTempG
    global LenText
    MyText = TextSplit
    LenTextL = LenText
    index = 0
    while Lindex <= LenTextL - 3:
        if(TextSplit[Lindex]==word1):
            if(TextSplit[Lindex+2]==word3):
                if(TextSplit[Lindex+1]!=word2):
                    O121 = O121 + 1
        Lindex = Lindex + 1

    O111 = TextTempG.count(' '+www1+www2+www3)
    O112 = TextTempG.count(' '+www1+www2) - O111
    O122 = TextTempG.count(' '+www1) - O111 - O112 - O121
    O211 = TextTempG.count(' '+www2+www3) - O111
    O212 = TextTempG.count(' '+www2) - O111 - O112 - O211
    O221 = TextTempG.count(' '+www3) - O111 - O211 - O121
    O222 = LenText - O111 - O112 - O121 - O122 - O211 - O212 - O221
    return O111,O112,O121,O122,O211,O212,O221,O222
''' ***************************************  Tagger And Chunker Function  *************************************'''
def TaggerFunc(Vers):
    global AllText
    global ListAllText
    global ListAllTextTags
    
    #print('tagfunc****Alltext = ' , AllText)
    #print('tagfunc****listAlltext = ' , ListAllText)
    #print('tagfunc****listAlltexttag = ' , ListAllTextTags)
    
    ListTempText = []
    ListTempTag = []
    List = []
    tag = []
    t = 0
    i = 0
    j = 0
    ibool = False
    jbool = False
    Text_Token = AllText
    TextChunked=Text_Token.split()
    #print('tagfunc****TextChunked = ',TextChunked)
    for row in TextChunked:
            NameNp = []
            j = 0
            #print('tagfunc**** row = ',row)

            if (type(row)==tuple or len(row.split()) > 1):
                for row2 in row:
					
                    if(jbool == False):
                        jbool = True
                        NameNp.append(row2)
                        #print('tagfunc****row2 = ',row2)
                    else:
                        jbool = False
                        #print('tagfunc****row2 = ',row2)
            else:
                if(ibool == False):
                    ibool = True
                NameNp.append(row)

                #else:
                    #ibool = False
                #j = j + 1
            i = i + 1
            ListTempText.append(NameNp)
            List.append(NameNp)
    #print('tagfunc****NameNp = ',NameNp)
    #print('tagfunc****ListTempText = ',ListTempText)
    #print('tagfunc****List = ',List)
    print('final')
    t=len(List)
    s =0
    while s < t:
        ListTempTag.append('X')
        s = s + 1
    index = 0
    for row in List:
        #ListAllText.append(FWSO.ReplaceBadWords(str(row),0))
        ListAllText.append(row)
        ListAllTextTags.append(ListTempTag[index])
        index = index + 1
    #print('tagfunc****ListAllText = ',ListAllText)
    #print('tagfunc****ListAllTextTags = ',ListAllTextTags)




''' ----------------  Good Finish  -------------'''
def GoodFinish():
    print( '\t Finish')

''' ----------------  Select Collocation from output database  -------------'''
def SelectCollsFromDB():
    DatabaseRow = DBCO.SelectCollV2TL()
    for row in DatabaseRow:
        CollArr2.append(row)

    DatabaseRow = DBCO.SelectCollV3TL()
    for row in DatabaseRow:
        CollArr3.append(row)




''' ************************************     Main Code        *********************************** '''
Select_DeleteBadRecord()
SelectBestRecordFunc()
MakeAllTextFunc()
SelectAllTextFunc()
MakeCollocationsFunc()
print('finish project in time = ' , datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

''' Close Database Connect '''

#database1.commit()


