
# Type of Surface #

def _get_surface(filename:str) -> str:
	"""
	Returns an estimation of the "Type of Surface" CMO group.

	Parameters
	----------
	:param filename: Name of the cropped colony image's file (use "\\" when using the full path to file)
	"""
	imp = IJ.openImage(filename);
	IJ.run(imp, "8-bit", "");
	IJ.run(imp, "GLCM Texture", "enter=1 select=[0 degrees] angular contrast correlation inverse entropy");
	table = RT.getResultsTable();
	entropy = table.getValue("Entropy", 0);

	#Close "Results" table window
	IJ.selectWindow("Results");
	IJ.run("Close");

	#Estimation
	if entropy < 7.1:
		return = "homogeneous"
	else:
		if contrast < 140:
			return = "homogeneous"
		else:
			if contrast < 230:
				return = "heterogeneous"
			else:
				return = "homogeneous"



# Form #

def _get_form(filename:str) -> str:
	"""
	Returns an estimation of the "Form" CMO group.

	Parameters
	----------
	:param filename: Name of the cropped colony image's file (use "\\" when using the full path to file)
	"""
	imp = IJ.openImage(filename);
	IJ.run(imp, "Measure", "");
	table = RT.getResultsTable();
	roundness = table.getValue("Round", 0);

	#Close "Results" table window
	IJ.selectWindow("Results");
	IJ.run("Close");

	#Estimation
	if roundness < 0.905:
		return = "irregular"
	else:
		return = "circular"




# Width calculation (auxiliary function) #

def _get_width(A:float, P:float) -> float:
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
    
    l = (-b+cmath.sqrt(d))/(2*a)
    
    #Determine w:
    w = (P/2) - l
    
    return max(l.real, w.real)



# Diameter #

def _get_diameter(filename_orig:str, filename_crop:str) -> str:
	"""
	Returns the calculation of the diameter of the colony.

	Parameters
	----------
	:param filename_orig: Name of the original colony image's file (use "\\" when using the full path to file)
	:param filename_crop: Name of the cropped colony image's file (use "\\" when using the full path to file)
	"""
	imp = IJ.openImage(filename1)
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
	W = _get_width(A,P) #Scale width
	IJ.runMacroFile("Close_All_Windows.fiji.ijm")
	
	# Get cropped image to determine perimeter
	imp = IJ.openImage(filename_crop)
	imp.show()

	width = imp.getWidth()
	scale = float(scale)

	#Close all open windows
	IJ.runMacroFile("Close_All_Windows.fiji.ijm")
	IJ.selectWindow("Results")
	IJ.run("Close")

	# Perimeter calculation
	return = (width*scale)/W


def morphotype(filename_orig:str, filename_crop:str) -> dict:
	"""
	Returns a dictionary the "Type of Surface", "Form" and diameter estimations for the selected colony image.

	Parameters
	----------
	:param filename_orig: Name of the original colony image's file (use "\\" when using the full path to file)
	:param filename_crop: Name of the cropped colony image's file (use "\\" when using the full path to file)
	"""
	result = {}
	
	result["Type of Surface"] = _get_surface(filename_crop)
	result["Form"] = _get_form(filename_crop)
	result["Diameter"] = _get_diameter(filename_orig, filename_crop)

	for k,v in result:
		print(k,v)
	
	return result



	