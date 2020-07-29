import sys
print (sys.version)
print (sys.version_info)

import subprocess
import json


ROOT_DIR = "/home/bryan/a_workspace/"
CONTENT_DIR = ROOT_DIR + "3042020Gather/content/"
WORKING_DIR = ROOT_DIR + "2019_portfolios/"
TEMP_DIR = WORKING_DIR + "temp/"

''' here we read student numbers and names into a usable list'''
def read_names():
	name_file = open(WORKING_DIR + "48872 Students and Test(2019) - Student List.csv", "r")
	lines = name_file.readlines()
	student_list = []
	for line in lines:
		words = line.split(",")
		# remove from our list the first line of data in the csv, and all students that are withdrawn
		if words[2] == "WITHDRAWN" or words[0] == "Student Name":
			continue
		# Create list like [student_number, student_name]
		words = words[1::-1]
		student_list.append(words)
		name_file.close()
	return(student_list)

''' here we read numbers, names, and evidence type into a usable list'''
def read_tests():
	test_name_file = open("48872 Students and Test(2019) - evidence items.csv", "r")
	lines = test_name_file.readlines()
	test_list = []
	for line in lines:
		words = line.split(",")
		# remove from our list the first line of data in the csv, and all items that are not Notebooks
		if words[2] == "TYPE" or words[3] != "Notebook\n":
			continue
		# Create list like [test_number, test_name, evidence_location]
		words = words[:3]
		test_list.append(words)
		test_name_file.close()
	return(test_list)
	''' SET VARIABLES '''
	# set file path appropriate to workbooks, formatives, and summatives

''' Here we set up the file paths for a student '''
def set_directories(student):
	STUDENT_DIR = "Student Documents/"+student[1]
	WORKBOOK_DIR = STUDENT_DIR+"/Workbook/"
	FORMATIVE_DIR = STUDENT_DIR+"/Formative Assessments/"
	SUMMATIVE_DIR = STUDENT_DIR+"/Summative Assessments/"
	feedback_location = STUDENT_DIR+"/Feedback/"
	portfolio_location = STUDENT_DIR+"/Portfolio Document/"
	return {"Workbook" : WORKBOOK_DIR, "Formative": FORMATIVE_DIR, "Summative": SUMMATIVE_DIR}

''' Here build a ipynb of the report card'''
def txt_to_ipynb(report_string, student, test):
	header_string = '{"cells": [{"cell_type": "markdown","metadata": {},"source": ["# {{name}} \\n","# {{test}}"]},{"cell_type": "raw","metadata": {},"source": '
	header_string = header_string.replace("{{name}}", student)
	header_string = header_string.replace("{{test}}", test)
	footer_string = '  } ], "metadata": {  "kernelspec": {   "display_name": "Python 3",   "language": "python",   "name": "python3"  },  "language_info": {   "codemirror_mode": {    "name": "ipython",    "version": 3   },   "file_extension": ".py",   "mimetype": "text/x-python",   "name": "python",   "nbconvert_exporter": "python",   "pygments_lexer": "ipython3",   "version": "3.7.4"  } }, "nbformat": 4, "nbformat_minor": 2}'
	return header_string + report_string + footer_string


def move_submission(student, ):
	# move submission from original directory into temp directory
	move_string = "mv "+TEMP_DIR+"*.ipynb \""+WORKING_DIR+REST_DIR+filename+"_submission.ipynb\""
	pass

def move_report():
	# Copy Report Card from original directory into temp directory
	pass

def make_documents(student, test_list, directories):
	this_test = test_list
	log_string = "No submissions for:\n"
	INDIVIDUAL_DIR = "Indivual/"

	# there are 18 Notebooks. let's look at them all
	for test in this_test:
		REST_DIR = directories[test[2]]
		# create variable for number:name instances "387_437" and "Gregory Milner - Coding challenge 7 NLP Practical"
		filenumbers = student[0] + "_" + test[0]
		filename = student[1] + " - " + test[1]

		''' Set strings for subprocess.call() '''
		make_temp_string = "mkdir -p "+WORKING_DIR+"temp/merged"
		unzip_string = "unzip -j "+CONTENT_DIR+filenumbers+".zip -d"+TEMP_DIR
		move_string = "mv "+TEMP_DIR+"*.ipynb \""+WORKING_DIR+REST_DIR+filename+"_submission.ipynb\""
		nbmerge_string = "nbmerge -o "+WORKING_DIR+REST_DIR+INDIVIDUAL_DIR+filename+".ipynb " + WORKING_DIR+REST_DIR+"*.ipynb"

		''' Print variables for debugging '''
		print("filenumbers", filenumbers)
		print("filename", filename)
		print("make_temp_string", make_temp_string)
		print("TEMP_DIR", TEMP_DIR)

		''' UNZIP make sure to run make_directories.py '''
		subprocess.call(make_temp_string, shell=True)
		subprocess.call(unzip_string, shell=True)
		input("Press Enter")
		subprocess.call(move_string, shell=True)
		input("Press Enter")
		subprocess.call(move_string, shell=True)
		subprocess.call(["rm", "-rf", TEMP_DIR])

		''' REPORT CARD '''
		# open report card, and convert to ipynb
		try:
			report = open(CONTENT_DIR+filenumbers+".txt", "r")
			lines = report.readlines()
			json_format = json.dumps(lines)
			# print(json_format)
			ipynb = txt_to_ipynb(str(json_format), student[1], test[1])
			report_ipynb = open(REST_DIR+filename+"_report_card.ipynb", "w")
			report_ipynb.write(ipynb)

		except Exception as e:
			# print(e)
			print("printing to log_file")
			log_string = log_string + filename + "\n"
		try:
			report.close()
			report_ipynb.close()
		except Exception as e:
			pass
			# print(e)



	# Capture logs of missing files
	try:
		log_file = open("Log.txt", "a")
		log_file.write(log_string)
		log_file.close()
	except Exception as e:
		raise(e)




student_list = read_names()
test_list = read_tests()

for student in student_list:
	make_directories = set_directories(student)
	make_documents(student, test_list, make_directories)

# print(make_directories)
# for student in student_list:
