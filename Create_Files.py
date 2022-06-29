from ij import IJ
from ij.measure import ResultsTable
import os
import re
import csv

directory1 = "C://Users//rober//OneDrive//Desktop//ESCOLA//Mestrado//Semestre2//Projeto//TO_TEST//all_images"
directory2 = "C://Users//rober//OneDrive//Desktop//ESCOLA//Mestrado//Semestre2//Projeto//TO_TEST"
directory3 = "C:\\Users\\rober\\OneDrive\\Desktop\\ESCOLA\\Mestrado\\Semestre2\\Projeto\\TO_TEST\\all_images"



def file_names_numbers(directory):
	all_files = os.listdir(directory)
	result = []
	for al in all_files:
		al = str(al)
		result.append((al,int(re.findall(r"\d+",al)[0])))
	return result


files = file_names_numbers(directory1)



# REAL RESULTS #
file1 = open(directory2+"//all_info.csv")
csvreader = csv.reader(file1)
rows = {}
for ix,row in enumerate(csvreader):
	if ix == 0:
			titles = row
	else:
			rows[ix] = {titles[i]:row[i] for i in range(1,len(row)-1)}
file1.close()





# SAVE RESULTS #

# Type of surface #

results_surface = []
first = True

for ix,f in enumerate(files):
	f,i = f

	imp = IJ.openImage(directory3 + "\\" + str(f));
	IJ.run(imp, "8-bit", "");
	IJ.run(imp, "GLCM Texture", "enter=1 select=[0 degrees] angular contrast correlation inverse entropy");
	table = ResultsTable.getResultsTable()
	#print(table.getRowAsString(ix))

	#Save heading
	if first:
		head = [str(elem).strip() for elem in table.getHeadings()] + ["Result"]
		results_surface.append(head)
		first = False

	res = [str(elem).strip() for elem in table.getRowAsString(0).split("\t")] + [rows[i]["surface"]]
	results_surface.append(res[1:]) #First element of the results is the line number, and should be removed

	IJ.selectWindow("Results")
	IJ.run("Close")


with open("Surface_Results.csv", "wb") as f:
	res_file = csv.writer(f)
	res_file.writerows(results_surface)





# Form #

results_form = []
first = True

for ix,f in enumerate(files):
	f,i = f

	imp = IJ.openImage(directory3 + "\\" + str(f));
	IJ.run(imp, "Measure", "");
	table = ResultsTable.getResultsTable()
	#print(table.getRowAsString(ix))

	#Save heading
	if first:
		head = [str(elem).strip() for elem in table.getHeadings()] + ["Result"]
		results_form.append(head)
		first = False

	res = [str(elem).strip() for elem in table.getRowAsString(0).split("\t")] + [rows[i]["form"]]
	results_form.append(res[1:])
	
	IJ.selectWindow("Results")
	IJ.run("Close")


with open("Form_Results.csv", "wb") as f:
	res_file = csv.writer(f)
	res_file.writerows(results_form)



