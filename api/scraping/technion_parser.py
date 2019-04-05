# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Eytan
#
# Python 3.7
#
# Created:     24/06/2014
# Copyright:   (c) Eytan 2014
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import requests
import re
import zipfile
import io
import json
import bs4
import os
import zc.lockfile

from bs4 import BeautifulSoup
from api.scraping import get_page, clean_name
from api.data import Faculty, Course
from api import lockfile_path, db_path


class FacultiesParser:
    base_url = r'http://ug3.technion.ac.il/Catalog/CatalogEng2016/'

    def __init__(self, remove_old=False, fill_from_db=True):
        if remove_old:
            Faculty.delete().execute()
        self.initialized = False
        self.faculties = []
        if fill_from_db:
            self.faculties = list(Faculty.select())
            self.initialized = True

    def scrape(self):
        facs = self._get_faculties(get_page(self.base_url))
        faculties_nums = self._get_faculties_nums(facs)
        for fac_text, fac_nums in faculties_nums.items():
            self.faculties.append(Faculty.create(name=clean_name(fac_text), nums=json.dumps(list(fac_nums))))
        self.initialized = True
        return self.faculties

    def _get_faculties(self, catalog_soup: BeautifulSoup):
        faculties = [fac for fac in catalog_soup.findAll('a') if 'fac' in fac['href'].lower()]
        for i in range(len(faculties)):
            faculties[i] = (faculties[i].text, 'CatalogEng2016'.join(faculties[i]['href'].split('CatalogEng')))
        return faculties

    def _get_faculties_nums(self, faculties):
        faculty_nums = {}
        for fac in faculties:
            fac_page = get_page(fac[1])
            nums = [r.text.strip()[:3] for r in fac_page.findAll('a') if r.get('href') and 'index' not in r.get('href')]
            if fac[0] not in faculty_nums:
                faculty_nums[fac[0]] = set([])
            for num in nums:
                faculty_nums[fac[0]].add(num)
            print(fac[0] + ': ' + str(faculty_nums[fac[0]]))
        return faculty_nums


class TechnionParser:
    base_course_ug = r'https://ug3.technion.ac.il/rishum/course/'
    kdam_in_unicode = u'\u05de\u05e7\u05e6\u05d5\u05e2\u05d5\u05ea \u05e7\u05d3\u05dd'
    name_in_uni = u'\u05E9\u05DD \u05DE\u05E7\u05E6\u05D5\u05E2'

    def __init__(self, faculties=None):
        if faculties is None:
            faculties = list(Faculty.select())
        self.faculties = faculties
        self.courses = []

    def _get_course_url(self, course_num, year='', semester=''):
        course_num_text = '{0:06d}'.format(course_num)
        res = self.base_course_ug + course_num_text
        if year != '' and semester != '':
            res += '/' + year + '0' + semester
        return res

    def _get_course_page(self, course_num, year='', semester=''):
        return get_page(self._get_course_url(course_num, year, semester))

    # get all course prequisits as list of Course nums
    def get_course_prequisite(self, course_soup=None):
        start = None
        # find the div of mikzoot kdam
        divisions = course_soup.findAll('div')
        for div in divisions:
            if div.string:
                if re.match("\s*" + self.kdam_in_unicode + "\s*", div.string):
                    # if kdam_in_unicode in div.string:
                    start = div
                    break

        # get the div of starting of all prequisets
        if start is None:
            return []
        else:
            start = start.nextSibling.nextSibling
            if not isinstance(start, bs4.Tag):
                return []

        my_as = [a for a in start.findAll('a') if a.string]
        return [re.search("\d{6}", a.string).group() for a in my_as]

    # returns a course object
    def get_course_name(self, course_soup):
        start = None
        # find the div of shem mikzoa
        for div in course_soup.findAll('div'):
            if div.string:
                if re.match("\s*" + self.name_in_uni + "\s*", div.string):
                    # if name in div.string:
                    start = div.next.next.next
                    break

        # make sure start is ok
        if start is None or not isinstance(start, bs4.Tag):
            return ""

        return clean_name(start.string.strip())

    def scrape(self):
        for num in [num for fac in self.faculties for num in json.loads(fac.nums)]:
            for i in range(1000):
                course_num = int(num) * 1000 + i
                page = self._get_course_page(course_num)
                name = self.get_course_name(page)
                if not name:
                    continue
                preqs = self.get_course_prequisite(page)
                self.courses.append(Course.create(name=name, number=course_num, prequisits=json.dumps(preqs), points=None))
        return self.courses


def main():
    lock = zc.lockfile.LockFile(lockfile_path)
    try:
        print("starting")
        Course.delete().execute()
        courses = TechnionParser().scrape()
        print("finished")
    except expression as identifier:
        lock.close()
        os.remove(lockfile_path)


if __name__ == '__main__':
    main()
