import os

data = open("courses.txt").read().splitlines()


# Result will be in the format:
#    <Course> : [Dependency Course 1, Dependency Course 2, ...]

result = {}
for line in data:
    strippedLine = line.split()
    result[ strippedLine[0] ] = strippedLine[2:]

output = "digraph TechnionCourses {" + os.linesep
for course,dependencies in result.iteritems():
    for d in dependencies:
        # Skip non-CS courses (as a test)
        if not (d.startswith("234") or course.startswith("234")):
            continue
        #output += "\t%s -> %s%s" % (course, d, os.linesep)
        # Reverse the arrows
        output += "\t%s -> %s%s" % (d, course, os.linesep)
output += "}"

open("courses.dot", "wb").write(output)
