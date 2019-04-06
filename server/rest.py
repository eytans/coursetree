import zc.lockfile
import os
import json
import logging

from flask import Flask, jsonify, send_from_directory, send_file, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from collections import defaultdict
from flask.helpers import safe_join
from playhouse.shortcuts import model_to_dict
from argparse import ArgumentParser

from api.data import Course
from api import lockfile_path, db_path

parser = ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', default=False)
args = parser.parse_args()

logger = logging.getLogger("server")
ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

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
        if course.number not in forward_courses[int(preq)]:
            forward_courses[int(preq)].append(course.number)
logger.debug("forward courses:")
for k, v in forward_courses.items():
    logger.debug(k, v)


@app.route('/')
def root():
    logger.debug("Sending root")
    return app.send_static_file('html/index.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/db/', methods=['GET'])
def get_course_data():
    coursenum = request.args['coursenum']
    emptyres = {"nodes": list(), "edges": list()}
    if not isinstance(coursenum, str) or len(coursenum) > 10 or not coursenum.isdigit():
        return jsonify(emptyres)

    def build_edges(num, visited=None):        
        if visited is None:
            visited = set()
        if int(num) not in courses or num in visited:
            return list()
        visited.add(num)
        forward = [e for nxt in forward_courses[int(num)] for e in build_edges(nxt, visited)]
        visited.remove(num)
        return list(set([(int(num), nxt) for nxt in forward_courses[int(num)]] + forward))

    try:
        edges = build_edges(coursenum)
        logger.debug(edges)
        nodes = [model_to_dict(n) for n in set([courses[int(key[0])] for key in edges] + [courses[int(key[1])] for key in edges])]
        return jsonify({"nodes": nodes, "edges": edges})
    except Exception as identifier:
        print(identifier)
        return jsonify(emptyres)



if __name__ == "__main__":
    lock = zc.lockfile.LockFile(lockfile_path)
    try:
        print("starting")
        app.run()
        print("finished")
    except Exception as identifier:
        lock.close()
        os.remove(lockfile_path)
