import sys

import subprocess
import json


ROOT_DIR = "/home/bryan/a_workspace/"
CONTENT_DIR = ROOT_DIR + "3042020Gather/content/"
WORKING_DIR = ROOT_DIR + "2019_portfolios/"
TEMP_DIR = WORKING_DIR + "temp/"
MERGE_DIR = TEMP_DIR + "merged/"

log_string = ""

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
	test_name_file = open(WORKING_DIR + "48872 Students and Test(2019) - evidence items.csv", "r")
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
def txt_to_ipynb(report_string, student, test, mark):
	header_string = '{"cells": [{"cell_type": "markdown","metadata": {},"source": ["# Student Name: {{name}} \\n","# Test Name: {{test}}\\n","# Test Mark: {{mark}}"]},{"cell_type": "raw","metadata": {},"source": '
	header_string = header_string.replace("{{name}}", student)
	header_string = header_string.replace("{{test}}", test)
	header_string = header_string.replace("{{mark}}", mark)
	footer_string = '  } ], "metadata": {  "kernelspec": {   "display_name": "Python 3",   "language": "python",   "name": "python3"  },  "language_info": {   "codemirror_mode": {    "name": "ipython",    "version": 3   },   "file_extension": ".py",   "mimetype": "text/x-python",   "name": "python",   "nbconvert_exporter": "python",   "pygments_lexer": "ipython3",   "version": "3.7.4"  } }, "nbformat": 4, "nbformat_minor": 2}'
	return header_string + report_string + footer_string


def move_submission(filename, filenumbers):
	# move submission from original directory into temp directory

	''' Unzip submission zip from content directory to temp directory '''
	unzip_string = "unzip -jqq "+CONTENT_DIR+filenumbers+".zip -d"+TEMP_DIR
	subprocess.call(unzip_string, shell=True)
	# input("Unzipped to temp. Press Enter")

	''' Move only the ipynb file from temp to merge directory'''
	move_string = "mv "+TEMP_DIR+"*.ipynb \""+MERGE_DIR+filename+"_submission.ipynb\""
	subprocess.call(move_string, shell=True)
	# input("Moved to Merge. Press Enter")

def move_report(student_name, test_name, filename, filenumbers):
	''' REPORT CARD '''
	# open report card, and convert to ipynb
	# Copy Report Card from original directory into temp directory
	try:
		report = open(CONTENT_DIR+filenumbers+".txt", "r")
		lines = report.readlines()

		''' extract mark '''
		mark = lines[-7].split(" ")[2][1:-1]+"%"

		''' Convert reprot card lines to JSON format '''
		json_format = json.dumps(lines)
		# print(json_format)
		ipynb = txt_to_ipynb(str(json_format), student_name, test_name, mark)
		report_ipynb = open(MERGE_DIR+filename+"_report_card.ipynb", "w")
		report_ipynb.write(ipynb)
	except Exception as e:
		raise(e)
	try:
		report.close()
		report_ipynb.close()
	except Exception as e:
		raise(e)

def make_documents(student, test_list, directories):
	this_test_list = test_list
	this_student = student
	global log_string
	INDIVIDUAL_DIR = "Individual/"

	# there are 18 Notebooks. let's look at them all
	for test in this_test_list:
		# get the correct directory for this notebook: i.e. sumamtive, formative, or workbook
		REST_DIR = directories[test[2]]

		# create string variables to hold filename mappings e.g. filenumbers = "387_437" and filename = "Gregory Milner - Coding challenge 7 NLP Practical"
		filenumbers = this_student[0] + "_" + test[0]
		filename = this_student[1] + " - " + test[1]

		''' Set strings for subprocess.call() '''
		make_temp_string = "mkdir -p "+WORKING_DIR+"temp/merged"

		''' Print variables for debugging '''
		# print("filenumbers", filenumbers)
		# print("filename", filename)
		# print("make_temp_string", make_temp_string)
		# print("TEMP_DIR", TEMP_DIR)

		''' Make Temp directory'''
		subprocess.call(make_temp_string, shell=True)
		try:
			move_submission(filename, filenumbers)
			move_report(this_student[1], test[1], filename, filenumbers)
			# input("Repory in merged. Press Enter")
		except Exception as e:
			# print(e)
			# print("printing to log_file")
			log_string = log_string + str(e) + "\n" + filename + "\n"

		nbmerge_string = "nbmerge -o " + "\""+WORKING_DIR+REST_DIR+INDIVIDUAL_DIR+filename+".ipynb\" " + MERGE_DIR+"*.ipynb"
		# print("merge_string", nbmerge_string)
		subprocess.call(nbmerge_string, shell=True)
		# input("files merged to Individual. Press enter to remove temp")
		subprocess.call(["rm", "-rf", TEMP_DIR])

	# Capture to logs any issues
	try:
		log_file = open("Log.txt", "a")
		log_file.write(log_string + "\n **************\n **************\n **************\n")
		log_string = ""
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
