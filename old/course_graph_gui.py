#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Eytan
#
# Created:     12/07/2014
# Copyright:   (c) Eytan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import Tk, BOTH, Entry
import tkMessageBox
from ttk import Frame, Button
import sys
import subprocess
from optparse import OptionParser
import load_db


COURSE_NOT_FOUND = "Course not in database"


def get_dot_exec():
    dot_exec = "dot.exe"
    return dot_exec

class CoursePickWindow(Frame):
    def __init__(self, parent, courses):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()

        self._courses = courses

    def initUI(self):
        #make frame fill the rot window
        self.parent.title("Simple")
        self.pack(fill=BOTH, expand=1)

        #add text box to get course number
        self.entry_text = Entry(self)
        self.entry_text.pack()

        #add a button that will create a graph
        create_graph_button = Button(self, text="Create PNG Graph", command=self.create_PNG_graph)
        create_graph_button.pack()

        create_graph_button = Button(self, text="Create SVG Graph", command=self.create_SVG_graph)
        create_graph_button.pack()

    def create_graph(self):
        try:
            course_num = self.entry_text.get().strip()
        except ValueError:
            tkMessageBox.showerror("not a valid num", "Please enter a valid "+
            "number with no letters")
            return

        if course_num not in self._courses:
            tkMessageBox.showerror("course not in database")
            return

        return course_num

    def create_PNG_graph(self):
        course_num = self.create_graph()
        #collect nodes and edges
        if course_num:
            self._courses[course_num].write_nexts_to_png(get_dot_exec())

    def create_SVG_graph(self):
        course_num = self.create_graph()
        #collect nodes and edges
        if course_num:
            self._courses[course_num].write_nexts_to_svg(get_dot_exec())

def main(argv):
    dot_exec = get_dot_exec()
    #create a dictionary of courses
    courses = load_db.get_courses("courses_db.txt")
    #commmand line parsing done right ;P
    parser = OptionParser()
    parser.add_option("-d", "--dot", dest="dot" )

    (options, args) = parser.parse_args(argv)
    if options.dot:
        dot_exec = options.dot

    if len(args) > 1:
        if not courses[args[1]]:
            print COURSE_NOT_FOUND
            exit(1)
        if len(args) > 2:
            courses[args[1]].write_nexts_to_png(dot_exec, args[2])
        else:
            courses[args[1]].write_nexts_to_png(dot_exec)

    #gui if no args
    else:
        root = Tk()
        root.geometry("350x250+300+300")
        app = CoursePickWindow(root, courses)
        root.mainloop()

if __name__ == '__main__':
        main(sys.argv[0:])
