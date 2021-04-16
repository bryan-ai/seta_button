import csv

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


student_dict = student_list_reader("student_list.csv")
print(student_dict)