all in python 2.7.8
might work in 2.6 but not under and not 3

the courses is a list of all the courses in the following format:
<course num> - [<dependency course num> .......]
if dependency list is empty there are no dependencies for the course
  *dependencies sometimes come as 123 and 124 or 125 and 126, i do not parse that, i take everything
 

(Tomer) About the graphs:
    I created a python script (MakeDotFile.py) that creates a file in
    GraphViz's dot format. Install GraphViz and run the command in
    CompileDotToGraph.bat to get the graph. I ran the command myself and got a
    huge graph that isn't visible (Courses-All.png), so I generated another
    file in which only courses that start with "234" appear (Courses-CS.png).

	
technion_parser will create 2 files:
	1. courses_names.txt
	2. courses_preq.txt
which have similar format as specified above
	dependencies:
		a. requests
		b. BeautifulSoup

course graph maker.py has 2 modes:
	gui - one argument no arguments
	commandline tool - one argument:
		1. course num
	in both modes if dot.exe isnt in path use -d or --dot "<path to dot.exe>"
	dependecies:
		a. Tkinter (i think its default)
		b. installed GraphViz
		
(Daniel) About the web GUI and API:
The web version of the program uses a slightly altered version of the original
program. The web interface includes a basic textbox and a button (thrown together
with some basic JavaScript and CSS3) which enables the user to communicate with
the program over HTTP inside his web browser. When the user presses the "Graph it"
button, the course ID is transmitted to the API (api.php?course_id=<the_id>) which
is responsible of handling the communication with the Python script. If the input
is valid and the script's execution was successful, the API returns the PNG image
data back into the <img> by reading <dot>'s raw byte output and redirecting it 
to the web GUI without actually creating a local persistent copy of the image.
Any error returned by the script (which should be written to stderr) will be 
displayed as text to the user instead of displaying the expected image.


Platform Dependant Settings
===========================
api.php BASE_PATH
install dot - need to have expat library installed for svg
BASE_DIR/config - should contain path to dot bin



WEBSITE
=======
http://eytans-ras.no-ip.org/courses-tree/
