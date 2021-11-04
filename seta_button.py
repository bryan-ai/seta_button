import csv
import os


def student_list_reader(file_path):
	with open(file_path, "r") as csvfile:
		rowreader = csv.reader(csvfile, delimiter = ',')
		student_dict = {}
		for row in rowreader:
			student_id = row[0]
			if student_id == "student_id":
				continue
			row.pop(0)
			student_dict[student_id] = row
	return student_dict

def evidence_items_reader(file_path):
	with open(file_path, "r") as csvfile:
		rowreader = csv.reader(csvfile, delimiter = ',')
		evidence_dict = {}
		for row in rowreader:
			test_name = row[1]
			if test_name == "item":
				continue
			row.pop(1)
			evidence_dict[test_name] = row
	return evidence_dict


def teams_list_reader(file_path):
	with open(file_path, "r") as csvfile:
		rowreader = csv.reader(csvfile, delimiter = ',')
		teams_dict = {}
		for row in rowreader:
			team_name = row[2]
			if team_name == "team_name":
				continue
			row.pop(2)
			teams_dict[team_name] = row
	return teams_dict

# student_dict = student_list_reader("User/bryan/a_workspace/seta_button_test/student_list.csv")
# evidence_dict = evidence_items_reader("User/bryan/a_workspace/seta_button_test/evidence_items.csv")
# teams_dict = teams_list_reader("User/bryan/a_workspace/seta_button_test/teams_list.csv")
# print(os.getcwd())
# print(os.path.relpath(__file__))