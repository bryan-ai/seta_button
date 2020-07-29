import json

# friends_list = [
#     'John','Rambo','Sam',
# ]
# json_format = json.dumps(friends_list)
# print(json_format)
# print(type(json_format))

def txt_to_ipynb(report_string):
	header_string = '{"cells": [{"cell_type": "markdown","metadata": {},"source": ["# {{name}} \\n","# {{test}}"]},{"cell_type": "raw","metadata": {},"source": '
	header_string = header_string.replace("{{name}}", "Bryan")
	header_string = header_string.replace("{{test}}", "challenge 2")
	footer_string = '  } ], "metadata": {  "kernelspec": {   "display_name": "Python 3",   "language": "python",   "name": "python3"  },  "language_info": {   "codemirror_mode": {    "name": "ipython",    "version": 3   },   "file_extension": ".py",   "mimetype": "text/x-python",   "name": "python",   "nbconvert_exporter": "python",   "pygments_lexer": "ipython3",   "version": "3.7.4"  } }, "nbformat": 4, "nbformat_minor": 2}'
	return header_string + report_string + footer_string

try:
	report = open("test.txt", "r")
	lines = report.readlines()
	json_format = json.dumps(lines)
	# print(json_format)
	ipynb = txt_to_ipynb(str(json_format))
except Exception as e:
	raise(e)
finally:
	report.close()

try:
	report_ipynb = open("report.ipynb", "w")
	report_ipynb.write(ipynb)

except Exception as e:
	raise(e)
finally:
	report_ipynb.close()
