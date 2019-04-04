#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Eytan
#
# Python 2.7
#
# Created:     24/06/2014
# Copyright:   (c) Eytan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import requests
import bs4
from bs4 import BeautifulSoup
import re
import threading

import zipfile
import io

import  technion_faculties_parser
from get_page import get_page

def update_courses_points(out_file_name):
    req = requests.request('GET', r'http://ug3.technion.ac.il/rep//REPFILE.zip')
    zip_data = req.content

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


class TechnionParser(object):
    def __init__(self):
        self._main_url = r'http://ug.technion.ac.il/Catalog/CatalogEng/CatalogEngCurrent.html'
        self._base_course_ug = r'https://ug3.technion.ac.il/rishum/course/'


    def get_course_url(self, course_num, year = '', semester = ""):
        course_num_text = '{0:06d}'.format(course_num)
        res = self._base_course_ug + course_num_text
        if year != '' and semester != '':
            res += '/' + year + '0' + semester
        return  res

    #returns a beatifull soup object of requested page
    def get_page(self, address, times = 0):
        return get_page(address, times)

    def get_course_page(self, course_num, year = '', semester = ""):
        return self.get_page(self.get_course_url(course_num, year, semester))

    #get all course prequisits as list of Course nums
    def get_course_prequisite(self, course_soup = None):
        start = None
        #find the div of mikzoot kdam
        divisions = course_soup.findAll('div')
        for div in divisions:
            if div.string:
                if re.match("\s*"+kdam_in_unicode+"\s*", div.string):
                    #if kdam_in_unicode in div.string:
                    start = div
                    break

        #get the div of starting of all prequisets
        if start is None:
            return []
        else:
            start = start.nextSibling.nextSibling
            if not isinstance(start, bs4.Tag):
                return []

        my_as = [a for a in start.findAll('a') if a.string]
        return [re.search("\d{6}", a.string).group() for a in my_as ]

    #returns a course object
    def get_course_name(self, course_soup):
        preq = self.get_course_prequisite(course_soup = course_soup)

        start = None
        #find the div of shem mikzoa
        for div in course_soup.findAll('div'):
            if div.string:
                if re.match("\s*"+name_in_uni+"\s*", div.string):
                    #if name in div.string:
                    start = div.next.next.next
                    break

        #make sure start is ok
        if start is None or  not isinstance(start, bs4.Tag):
            return ""

        return start.string.strip()


kdam_in_unicode = u'\u05de\u05e7\u05e6\u05d5\u05e2\u05d5\u05ea \u05e7\u05d3\u05dd'
name_in_uni = u'\u05E9\u05DD \u05DE\u05E7\u05E6\u05D5\u05E2'

def main():
    technion_faculties_parser.create_faculties_file()
    parses_courses = set([])
    courses_points_file_name = r'courses_points.txt'
    update_courses_points(courses_points_file_name)
    courses_points = {}
    with open(courses_points_file_name, 'r') as courses_points_file:
        for line in courses_points_file.readlines():
            parses_courses.add(line.split(' ')[0])
            courses_points[int(line.split(' ')[0])] = line.split(' ')[-1].strip()

    tp = TechnionParser()
    faculties = set([])
    all = []
    out_db = open(r'courses_db.txt', 'w')
    with open('technion_faculties.txt', 'r') as facs_file:
        fac_nums = [fac_num.split('=')[1] for fac_num in facs_file.readlines() if 'fac_num' in fac_num]
        for fac_num in fac_nums:
            print('faculty: ' + fac_num)
            for i in xrange(1000):
                course_num = int(fac_num)*1000 + i
                course_num_text = '{0:06d}'.format(course_num)
                course_soup = tp.get_course_page(course_num)
                if course_soup is None:
                    continue
                name = tp.get_course_name(course_soup).encode('utf-8')
                if name == '' or name is None:
                    continue
                preq_courses = tp.get_course_prequisite(course_soup = course_soup)
                preq = " ".join(preq_courses)
                points = None
                if course_num in courses_points:
                    points = courses_points[course_num]
                url = tp.get_course_url(course_num).decode('utf-8')
                out_db.write('--coursestart--\n')
                out_db.write('-number ' + course_num_text + '\n')
                out_db.write('-name ' + name + '\n')
                out_db.write('-preq ' + preq + '\n')
                if points is not None:
                    out_db.write('-points ' + points + '\n')
                out_db.write('-url ' + url + '\n')
                out_db.write('--courseend--\n')

    out_db.close()

if __name__ == '__main__':
    main()
