import sys
print (sys.version)
print (sys.version_info)

import subprocess
ROOT_DIR = "/home/bryan/a_workspace/"
CONTENT_DIR = ROOT_DIR + "3042020Gather/content/"
WORKING_DIR = ROOT_DIR + "2019_portfolios/"
STUDENT_DIR = WORKING_DIR+"Student Documents/"
TEMP_DIR = WORKING_DIR + "temp/"

def read_names():
	name_file = open(WORKING_DIR+"48872 Students and Test(2019) - Student List.csv", "r")
	lines = name_file.readlines()
	student_list = []
	for line in lines:
		words = line.split(",")
		# remove from our list the first line of data in the csv, and all students that are withdrawn
		if words[2] == "WITHDRAWN" or words[0] == "Student Name":
			continue
		words = words[1::-1]
		student_list.append(words)
	return(student_list)
	name_file.close()

def make_directory(student_list):
	this_list = student_list
	for student in this_list:
		location = STUDENT_DIR+student[1]
		subprocess.call(["mkdir", location])
		workbook_location = location+"/Workbook/Individual"
		formative_location = location+"/Formative Assessments/Individual"
		summative_location = location+"/Summative Assessments/Individual"
		feedback_location = location+"/Feedback/Individual"
		portfolio_location = location+"/Portfolio Document/Individual"
		subprocess.call(["mkdir","-p", workbook_location])
		subprocess.call(["mkdir","-p", formative_location])
		subprocess.call(["mkdir","-p", summative_location])
		subprocess.call(["mkdir","-p", feedback_location])
		subprocess.call(["mkdir","-p", portfolio_location])

student_list = read_names()
make_directory(student_list)
