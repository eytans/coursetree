__author__ = 'eytan'

from get_page import get_page
from bs4 import BeautifulSoup

base_url = r'http://ug3.technion.ac.il/Catalog/CatalogEng/'

def get_faculties(catalog_soup):
    faculties = [fac for fac in catalog_soup.findAll('a') if 'fac' in fac['href'].lower()]
    for i in range(len(faculties)):
        print(i)
        faculties[i] = (faculties[i].text , faculties[i]['href'])
    return faculties

def get_faculties_nums(faculties):
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

def create_faculties_file():
    catalog_url = base_url
    catalog_soup = get_page(catalog_url)
    if catalog_soup is None:
        return
    facs = get_faculties(catalog_soup)
    print('got facs, len: ' + str(len(facs)))
    faculties_nums = get_faculties_nums(facs)
    with open('technion_faculties.txt', 'w') as fac_file:
        for fac_text, fac_nums in faculties_nums.iteritems():
            fac_file.write('--startfaculty--\n')
            fac_file.write('fac_name=' + fac_text + '\n')
            for num in fac_nums:
                fac_file.write('fac_num=' + num + '\n')
            fac_file.write('--endfaculty--\n')

def main():
    create_faculties_file()

if __name__ == '__main__':
    main()
