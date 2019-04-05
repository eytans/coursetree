import zc.lockfile
import os
import json

from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from collections import defaultdict

from api.data import Course
from api import lockfile_path, db_path


app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute", "1 per second"],
)

courses = {course.number: course for course in Course.select()}
forward_courses = defaultdict(list)
for course in Course.select():
    for preq in json.loads(course.prequisits):
        forward_courses[preq].append(course.number)


@app.route('/')
def root():
    print("Sending root")
    return app.send_static_file('html/index.html')


@app.route('/db/<coursenum>')
def get_course_data(coursenum):
    emptyres = {"nodes": set(), "edges": list()}
    if not isinstance(coursenum, str) or len(coursenum) > 10 or not coursenum.isdigit():
        return jsonify(emptyres)

    def build_edges(num, visited=None):        
        if visited is None:
            visited = set()
        if num not in courses or num in visited:
            return emptyres
        visited.add(num)
        forward = [e for nxt in forward_courses[num] for e in build_edges(nxt, visited)]
        visited.remove(num)
        return [(num, nxt) for nxt in forward_courses[num]] + forward

    try:
        edges = build_edges(coursenum)
        nodes = set([courses[key[0]] for key in edges] + [courses[key[1]] for key in edges])
        return jsonify({"nodes": nodes, "edges": edges})
    except:
        return jsonify(emptyres)



if __name__ == "__main__":
    lock = zc.lockfile.LockFile(lockfile_path)
    try:
        print("starting")
        app.run()
        print("finished")
    except expression as identifier:
        lock.close()
        os.remove(lockfile_path)
