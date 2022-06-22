from ij import IJ
from ij.measure import ResultsTable as RT
from ij.process.ImageProcessor import drawLine
import os
import re
import csv
import cmath # For the get_width function
import sys

directory1 = "C://Users//rober//OneDrive//Desktop//ESCOLA//Mestrado//Semestre2//Projeto//TO_TEST//all_images"
directory2 = "C://Users//rober//OneDrive//Desktop//ESCOLA//Mestrado//Semestre2//Projeto//TO_TEST"
directory3 = "C:\\Users\\rober\\OneDrive\\Desktop\\ESCOLA\\Mestrado\\Semestre2\\Projeto\\TO_TEST\\all_images"


# Auxiliary Functions #

# Function to retrieve image file names and their associated number
def file_names_numbers(directory):
	all_files = os.listdir(directory)
	result = []
	for al in all_files:
		al = str(al)
		result.append((al,int(re.findall(r"\d+",al)[0])))
	return result


files = file_names_numbers(directory1)




# Real Results #
file1 = open(directory2+"//all_info.csv")
csvreader = csv.reader(file1)
rows = {}
for ix,row in enumerate(csvreader):
	if ix == 0:
			titles = row
	else:
    		rows[ix] = {titles[i]:row[i] for i in range(1,len(row)-1)}
file1.close()





########## TEXTURE ##########

correct0 = []
incorrect0 = []

correct1 = []
incorrect1 = []

correct2 = []
incorrect2 = []

correct3 = []
incorrect3 = []


for f,n in files:
	imp = IJ.openImage(directory3 + "\\" + str(f))
	IJ.run(imp, "8-bit", "")
	
	IJ.run(imp, "GLCM Texture", "enter=1 select=[0 degrees] angular contrast correlation inverse entropy")
	table = RT.getResultsTable()
	#print(table.getRowAsString(0))
	entropy = table.getValue("Entropy", 0)



	# First attempt
	if entropy >= 7:
		res0 = "heterogeneous"
	else:
		res0 = "homogeneous"


	# With decision trees (1 parameter)
	if entropy < 6.9:
		res1 = "homogeneous"
	else:
		if entropy >= 7.7:
			res1 = "heterogeneous"
		else:
			if entropy >= 7.4:
				res1 = "homogeneous"
			else:
				if entropy < 7.2:
					res1 = "homogeneous"
				else:
					res1 = "heterogeneous"


	# With more parameters
	#print(table.getHeadings())
	inverse = table.getValue("Inverse Difference Moment   ", 0)
	contrast = table.getValue("Contrast", 0)

	# First model
	if inverse >= 0.41:
		if entropy < 7.2:
			res2 = "homogeneous"
		else:
			res2 = "heterogeneous"
	else:
		if contrast >= 281:
			res2 = "homogeneous"
		else:
			if contrast < 139:
				res2 = "homogeneous"
			else:
				res2 = "heterogeneous"

	
	# Second model
	if entropy < 7.1:
		res3 = "homogeneous"
	else:
		if contrast < 140:
			res3 = "homogeneous"
		else:
			if contrast < 230:
				res3 = "heterogeneous"
			else:
				res3 = "homogeneous"
				
				
	real = rows[n]["surface"]

	if str(res0) == real:
		correct0.append(n)
	else:
		incorrect0.append((n, [real, entropy]))
	
	if str(res1) == real:
		correct1.append(n)
	else:
		incorrect1.append((n, [real, entropy]))

	if str(res2) == real:
		correct2.append(n)
	else:
		incorrect2.append((n, [real, entropy]))

	if str(res3) == real:
		correct3.append(n)
	else:
		incorrect3.append((n, [real, entropy]))

print("Texture\n#######\n")
print("First attempt:\n--------------") #108 correct, 27 incorrect
print("Correct:")
print(len(correct0))
print("")
print("Incorrect:")
print(len(incorrect0))
print("")
print("With decision tree:\n-------------------") #113 correct, 22 incorrect
print("Correct:")
print(len(correct1))
print("")
print("Incorrect:")
print(len(incorrect1))
print("")
print("With more parameters (model 1):\n-------------------------------") #123 correct, 12 incorrect
print("Correct:")
print(len(correct2))
print("")
print("Incorrect:")
print(len(incorrect2))
print("")
print("With more parameters (model 2):\n-------------------------------") #123 correct, 12 incorrect
print("Correct:")
print(len(correct3))
print("")
print("Incorrect:")
print(len(incorrect3))





########## FORM ##########

correct = []
incorrect = []

for f,n in files:
	imp = IJ.openImage(directory3 + "\\" + str(f))
    
	IJ.run(imp, "Measure", "")
    
	table = RT.getResultsTable()
    
	roundness = table.getValue("Round", 0)

	if roundness < 0.905:
		res = "irregular"
	else:
		res = "circular"
    
	real = rows[n]["form"]

	if res == real:
		correct.append(n)
	else:
		incorrect.append((n, [real, roundness]))

	IJ.selectWindow("Results")
	IJ.run("Close")
	
print("")
print("")
print("Form\n####\n")
print("Correct:")
print(len(correct))
print("")
print("Incorrect:")
print(len(incorrect))
# 132 correct, 3 incorrect






########## DIAMETER ##########


# Auxiliary function to determine the following equation system:

# w = (P/2) - l
# l^2 - l*(P/2) + A = 0

# w = width, l = length, P = perimeter, A = area

 
  
def get_width(A, P):
    """
    Calculates the longest side of a rectangle,
    given its area and perimeter.
    
    Parameters
    ----------
    :param A: Area of the rectangle
    :param P: Perimeter of the rectangle
    """
    #Determine l:
    a = 1
    b = -P/2
    c = A
    d = (b**2) - (4*a*c)  #discriminant

    #Determine w:
    w = (-b+cmath.sqrt(d))/(2*a)

    #To get height:
    #h = (P/2) - w
    
    return w.real




res = []
wrong = []

for ix,f in enumerate(files):
	f,n = f
	imp = IJ.openImage(directory3 + "_orig\\" + str(f))


	# Limit the search space for the scale bar selection
	# (lacking scale adjustment after cropping)
	
	#w,h = imp.getWidth(), imp.getHeight()

	#IJ.setTool("rectangle");

	#if rows[n]["location"] == "BR":
		#imp.setRoi(int(w*18/30), int(h*25/30), int(w*11/30), int(h*4/30));
		#imp = imp.resize(int(w*10/30), int(h*3/30), "bilinear");
	#elif rows[n]["location"] == "BL":
		#imp.setRoi(int(w*1/30), int(h*25/30), int(w*11/30), int(h*4/30));
		#imp = imp.resize(int(w*7/20), int(h*4/20), "bilinear");
	#elif rows[n]["location"] == "TR":
		#imp.setRoi(int(w*18/30), int(h*1/30), int(w*11/30), int(h*4/30));
		#imp = imp.resize(int(w*7/20), int(h*4/20), "bilinear");
	#elif rows[n]["location"] == "TL":
		#imp.setRoi(int(w*1/30), int(h*1/30), int(w*11/30), int(h*4/30));
		#imp = imp.resize(int(w*7/20), int(h*4/20), "bilinear");

	imp.show()

    #scale value should be defined by the user
	if rows[n]["scale"] == "white":
		IJ.runMacroFile("WhiteScaleThreshold.fiji.ijm")
		scale = "0.5"
	else:
		IJ.runMacroFile("BlackScaleThreshold.fiji.ijm")
		scale = "1"
	
	
	IJ.run(imp, "Select Bounding Box (guess background color)", "")
	IJ.run(imp, "Measure", "")
	tab = RT.getResultsTable()
	A,P = tab.getValue("Area", 0), tab.getValue("Perim.", 0)
	Sw = get_width(A,P) #Scale width
	
	IJ.runMacroFile("Close_All_Windows.fiji.ijm")
	
	# Get cropped image to determine perimeter
	imp = IJ.openImage(directory3 + "\\" + str(f))
	imp.show()

	Iw = imp.getWidth() #Image width
	scale = float(scale)

	# Perimeter calculation
	perimeter = (Iw*scale)/Sw
	
	if abs(perimeter - float(rows[n]["diameter"][:-3].replace(",","."))) > 1:
		wrong.append((perimeter, rows[n]["diameter"], n))
	
	IJ.runMacroFile("Close_All_Windows.fiji.ijm")
	IJ.selectWindow("Results")
	IJ.run("Close")


print("")
print("")
print("Diameter\n########\n")
print("Estimations that differ 1mm:")
print("")
for w in wrong:
	print(w)





