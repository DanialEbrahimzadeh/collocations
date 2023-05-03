import os

class WordsStem:
	def __init__(self):
		print(' ')
	def ReplaceBadWords(self,TextEn,temp):
		MyText = TextEn
		#MyText = MyText.replace(chr(8207),'')      #(right to left) dar inja be jaye character 8207 hichi nabayad begozarad
		#MyText = MyText.replace(chr(8206),'')      #(left to right) dar inja be jaye character 8207 hichi nabayad begozarad
		MyText = MyText.replace(chr(45),'')        # - character
		MyText = MyText.replace(chr(150),'')       # - character
		MyText = MyText.replace(chr(173)," ")       # - character
		MyText = MyText.replace("\\u200c"," ")
		MyText = MyText.replace("\\u200e"," ")
		MyText = MyText.replace("\\u200f"," ")
		MyText = MyText.replace("\\n", " ")
		MyText = MyText.replace("\\t", " ")
		MyText = MyText.replace("(u\"", " ")
		MyText = MyText.replace("(u\'", " ")
		MyText = MyText.replace("\')", " ")
		MyText = MyText.replace("(", '')
		MyText = MyText.replace(")", '')
		MyText = MyText.replace("\")", " ")
		MyText = MyText.replace("\",)", " ")
		MyText = MyText.replace("\',)", " ")
		MyText = MyText.replace("\'r"," ")
		MyText = MyText.replace("\'n"," ")
		MyText = MyText.replace("\\\\r"," ")
		MyText = MyText.replace("\\\\n"," ")
		MyText = MyText.replace("\\\\\"", " ")
		MyText = MyText.replace("\\\\", " ")
		MyText = MyText.replace("\'", " ")
		MyText = MyText.replace("\')", " ")
		MyText = MyText.replace("(       ", " ")
		MyText = MyText.replace("\n\t\t\n\n\n\n\n", " ")
		MyText = MyText.replace(",", " ")
		MyText = MyText.replace("  ", " ")
		MyText = MyText.replace("   ", " ")
		MyText = MyText.replace("    ", " ")
		MyText = MyText.replace("     ", " ")
		MyText = MyText.replace(":", " ")
		MyText = MyText.replace(" , ", " ")
		MyText = MyText.replace(", ", " ")
		MyText = MyText.replace(" ,", " ")
		if(temp == 0):
			MyText = MyText.replace(".", " ")
			MyText = MyText.replace("؟", " ")
			MyText = MyText.replace("!", " ")
			MyText = MyText.replace("،", " ")
			MyText = MyText.replace(" ،", " ")
			MyText = MyText.replace("، ", " ")
			MyText = MyText.replace(" ، ", " ")
		MyText = MyText.replace("                                                                                          ", " ")
		return MyText

FWSO = WordsStem()
