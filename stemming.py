import datetime
import os
import glob
import sentence_class
import sentence_processor_class
class Stemming:
	def __init__(self):
		print(' ')
	def StemmingFile(self):
		# create a directory for output files
		if not os.path.exists('output-stemming-files'):
			os.makedirs('output-stemming-files')
		path_of_output_directory = 'output-stemming-files'
		# create a list of input files from input-files directory
		list_of_input_files_path = glob.glob(os.path.join('input-stemming-files/', '*.txt'))
		list_of_input_files_path.sort()
		# create from sentence_processor_class
		_sentence_processor = sentence_processor_class.SentenceProcessor()

		# process each input file in a loop
		for input_file_path in list_of_input_files_path:

			# get name of input file
			name_of_input_file = input_file_path.split("/")[1]
			# create and open the output file
			output_file = open(path_of_output_directory + '/output-of-' + name_of_input_file, "w", encoding="utf8")
			output_file_stemming = open(path_of_output_directory + '/stemming-output-of-' + name_of_input_file, "w", encoding="utf8")
			# open the input file and read all of the file and close the input file
			input_file = open(input_file_path, "r", encoding="utf8")
			content_of_input_file = input_file.readlines()
			input_file.close()
			# create one string from content of input file
			if len(content_of_input_file) > 1:
				content_of_input_file = [''.join(content_of_input_file)]

			# split string with . sign
			sentences = content_of_input_file[0].split(".")
			sentences.pop()
			# write time of starting process in output file
			output_file.write(str(datetime.datetime.now().time()) + " start to process" + name_of_input_file + "\n")
			output_file.write("-" * 130 + "\n")
			output_file.write("-" * 130 + "\n")

			list_sentence_processed_of_input_file = []
			for sentence in sentences:
				# if sentence have \n then replace it with whitespace
				if sentence.find("\n") > -1:
					sentence = sentence.replace("\n", " ")
				# create sentence_class and process sentence
				_sentence = sentence_class.Sentence(sentence)
				_sentence.inner_process()

				# Process the sentence.
				_sentence.processed_sentence = _sentence_processor.process(_sentence.sentence)

				# add processed sentence to a list
				list_sentence_processed_of_input_file.append(_sentence)

			# print result of process sentence into output file
			for item in list_sentence_processed_of_input_file:
				output_file.write(item.__str__())
				output_file_stemming.write(item.stemming_str())

			# end of process of an input file
			output_file.write("-" * 130 + "\n")
			output_file.write(str(datetime.datetime.now().time()) + " end of process" + name_of_input_file + "\n")

			# close the output file
			output_file.close()
			output_file_stemming.close()
