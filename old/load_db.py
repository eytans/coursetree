__author__ = 'eytan'
from Course import Course

def main():
    pass

def get_courses(db_path):
    courses = {}
    preq = {}
    with open(db_path, 'r') as db:
        for line in db.readlines():
            if line.startswith('--coursestart--'):
                number = ''
                name = ''
                pre = None
                points = None
                url = None
            elif line.startswith('-number'):
                number = " ".join(line.split()[1:])
            elif line.startswith('-name'):
                name = "_".join(line.split()[1:])
            elif line.startswith('-preq'):
                pre = line.split()[1:]
            elif line.startswith('-points'):
                points = line.split()[1]
            elif line.startswith('-url'):
                url = " ".join(line.split()[1:])
            elif line.startswith('--courseend--'):
                if number == '' or name == '' or len(number) != 6:
                    continue
                courses[number] = Course(number, name, url=url, points=points)
                if pre is not None:
                    preq[number] = pre
    for course_num, preq_list in preq.iteritems():
        for prequisite in preq_list:
            if prequisite not in courses:
                continue
            courses[prequisite].add_next_course(courses[course_num])
    return courses

if __name__ == '__main__':
    main()


