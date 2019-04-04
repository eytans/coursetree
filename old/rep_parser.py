# coding: utf-8
import zipfile
import urllib.request
import io
import sys

def update_courses_points(out_file_name):
	req = urllib.request.urlopen(r'http://ug3.technion.ac.il/rep//REPFILE.zip')
	zip_data = req.read()

	zipf = io.BytesIO(zip_data)
	opened_zip = zipfile.ZipFile(zipf)
	files = opened_zip.filelist
	rep_file_name = ''

	for f in files:
		if 'repfile' in f.filename.lower():
			rep_file_name = f.filename

	if rep_file_name == '':
		exit(1)

	rep_file = opened_zip.open(rep_file_name)

	courses = []

	line_num = 0
	for line in rep_file:
		line = line.decode('ascii')
		if (not line.startswith('+-')) and line_num == 0:
			continue
		if line_num == 2:
			if (len(line.split(' ')) < 2):
				continue
			courses.append((str(course), line.split('|')[1].split(' ')[0]))
			line_num = -1
			continue
		if line_num == 1:
			if (len(line.split(' ')) < 2):
				continue
			course = line.split(' ')[-2]
		line_num += 1

	with open(out_file_name, 'w') as out:
		for course_num, points in courses:
			if points == '':
				continue
			try:
				int(course_num)
			except:
				continue
			out.write(course_num +' - ' + points +'\n')

def main():
	if len(sys.argv) < 2:
		print('please enter out file path')
		exit(1)
	update_courses_points(sys.argv[1])