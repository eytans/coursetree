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

import subprocess
import traceback
import xml.etree.ElementTree as ET
import color

illegal_dot_chars = "[().-'#\":,+/]"
debug = False

def main():
    pass

if __name__ == '__main__':
    main()

def get_all_g_tagged_children(elem):
    res = {}
    while not elem.tag.endswith("}g"):
        elem = elem[0]

    for child in elem:
        if 'class' in child.attrib and \
                (child.attrib['class'].lower() == 'node' or child.attrib['class'].lower() == 'edge'):
            res[child[0].text] = child
    return res

def get_root_elem(g_tree):
    names = {}
    arrows = set([])
    for e in g_tree.itervalues():
        if '->' in e[0].text:
            arrows.add(e)
        else:
            names[e[0].text] = e
    for arrow in arrows:
        #delete if its not first
        if arrow[0].text.split('->')[1] in names:
            del names[arrow[0].text.split('->')[1]]
    if 'G' in names:
        del names['G']
    if len(names.items()) != 1:
        raise StandardError("illegal state")
    return names.popitem() #first is key second is item


class Course(object):
    ##########################general object funcs##############################
    def __init__(self, nid, name, url=None, points=None, color = ""):
        self._id = nid
        self._name = name.translate(None, illegal_dot_chars)
        self._name = self._name.decode('utf-8')
        self._next_courses = set([])
        self._parents = set([])
        self._color = color
        self.url = url
        self.points = points

    def __eq__(self, other):
        return self._id == other._id

    def __ne__(self, other):
        return not self==other

    def __hash__(self):
        return int(self._id)

    #####################################################################################

    def edge_name(self, edge1_text, edge2_text):
        return edge1_text + u" -> " + edge2_text

    def add_parent(self, course):
        self._parents.add(course)

    def add_next_course(self, course):
        self._next_courses.add(course)

    def add_courses_to_graph(self, edges, faculties = []):
        used_courses = set([])
        to_do = set([])
        to_do.add(self)
        while len(to_do) > 0:
            current_course = to_do.pop()
            for course in current_course._next_courses:
                if faculties and len(faculties) > 0:
                    if len([fac for fac in faculties if course._id.startswith(fac)]) == 0:
                        continue
                edges.add( (current_course, course) )
                if course not in used_courses:
                    to_do.add(course)
                used_courses.add(course)

    def color_all_children(self):
        for node in self._next_courses:
            if len(node._parents) == 1:
                node._color = self._color
            else:
                node._color = color.get_random_color()
            node.color_all_children()

    #creates a tempfile and writes the dot info into it
    def create_dot_file(self, faculties = []):
        edges = set([])
        self.add_courses_to_graph(edges, faculties)

        nodes = set([])
        for edge in edges:
            nodes.add(edge[0])
            nodes.add(edge[1])

        for node in nodes:
            for course in node._next_courses:
                course.add_parent(node)

        test = False
        first_line_nodes = set([])
        for node in nodes:
            if len(node._parents) == 0:
                if test is True:
                    exit(100)
                test = True
                node._color = "white"
                for course in node._next_courses:
                    first_line_nodes.add(course)
                break


        for node in first_line_nodes:
            node._color = color.get_random_color()
            node.color_all_children()

        #now create directed graph and show it
        dot = u""
        dot += u"digraph G {\n"
        if debug:
            print "digraph G {"
        for node in nodes:
            dot += u"\t" + node._name \
                   + u" [style = filled ,fillcolor = " + node._color + u"];\n"
            if debug:
                print("\t"+node._name +
                      " [style = filled ,fillcolor = " + node._color + "];\n")

        for edge in edges:
            dot += u"\t" + self.edge_name(edge[0]._name, edge[1]._name) + u"\n"
            if debug:
                print ("\t" + self.edge_name(edge[0]._name, edge[1]._name)+ "\n")
        dot += u"}"
        if debug:
            print "}"
        return dot.encode('utf-8')

    def _build_group(self, elem, used_id, id_num, url):
        group = ET.Element('g')

        ellipse = elem[1]
        text = elem[2]

        if text.text not in used_id:
            used_id[text.text] = id_num
            id_num += 1

        go_to_text = ET.Element('text')
        go_to_text.text = 'go to page'
        go_to_text.set('text-anchor',"middle")
        go_to_text.set('fill',"blue")
        go_to_text.set('x', ellipse.get('cx'))
        go_to_text.set('y', str(int(ellipse.get('cy'))+ (1.5*float(ellipse.get('ry')))))
        go_to_text.set('width', ellipse.get('rx'))
        go_to_text.set('height', ellipse.get('ry'))
        if url is not None:
            go_to_text.set('onclick', 'window.open("' + url + '")')
        group.set('name', 'coursegroup'+str(used_id[text.text]))
        text.set('id', 'coursetext'+str(used_id[text.text]))
        ellipse.set('onclick', "changeVisibility('"+ str(used_id[text.text]) + "')")
        ellipse.set('oncontextmenu', "alert('Custom menu');return false")
        text.set('onclick', "changeVisibility('"+ str(used_id[text.text]) + "')")
        return (group, id_num, ellipse, text, go_to_text)

    def rebuild_tree(self, root_elem, gs, depth = 0, faculties = []):
        layers = [set([])]
        layer_id = 1
        layers[0].add(self)

        groups_by_node_names = {}

        used_id = {}
        id_num = 0

        res = self._build_group(gs[self._name], used_id, id_num, self.url)
        id_num = res[1]
        groups_by_node_names[self._name] = (res[0], layer_id, res[2], res[3], res[4])

        while len(layers[layer_id-1]) > 0:
            layers.append(set([]))
            to_remove = set([])
            for obj in layers[layer_id-1]:
                for child in obj._next_courses:
                    if faculties and len(faculties) > 0:
                        if len([fac for fac in faculties if child._id.startswith(fac)]) == 0:
                            continue
                    elem = gs[child._name]
                    res = child._build_group(elem, used_id, id_num, child.url)
                    group = res[0]
                    id_num = res[1]
                    layers[layer_id].add(child)
                    groups_by_node_names[child._name] = (group, layer_id, res[2], res[3], res[4])
            layer_id += 1


        # get all arrows into right groups
        arrows = {}
        for arrow_name, arrow in gs.iteritems():
            if u'->' in arrow_name:
                arrow_start = arrow_name.split(u'->')[0]
                if arrow_start not in arrows:
                    arrows[arrow_start] = set([])
                arrows[arrow_start].add(arrow)

        for arrow_start, arrow_set in arrows.iteritems():
            for item in arrow_set:
                if item[0].text.split(u'->')[1] in groups_by_node_names and arrow_start in groups_by_node_names:
                    groups_by_node_names[arrow_start][0].append(item)

        done = set([])
        layer_id = len(layers)
        while layer_id > 0:
            layer_id -= 1
            for node in layers[layer_id]:
                if node not in done and node._name in groups_by_node_names:
                    done.add(node)
                    tup = groups_by_node_names[node._name]
                    # hide unwanted layers
                    if (depth is not None) and (layer_id > depth - 1):
                        if len(tup[0]) != 0:
                            tup[0].set("opacity", "0")
                            tup[3].text = tup[3].text + '+'
                    for parent in node._parents:
                        if parent._name in groups_by_node_names:
                            groups_by_node_names[parent._name][0].append(tup[0])
                            groups_by_node_names[parent._name][0].append(tup[2])
                            groups_by_node_names[parent._name][0].append(tup[3])
                            if len(tup) > 4:
                                groups_by_node_names[parent._name][0].append(tup[4])

        group = ET.Element('g')
        group.append(groups_by_node_names[self._name][0])
        group.append(groups_by_node_names[self._name][2])
        group.append(groups_by_node_names[self._name][3])
        if len(groups_by_node_names[self._name]) > 4:
            group.append(groups_by_node_names[self._name][4])
        return group

    def create_svg_tree(self, dot_exec, png = "out.svg", depth = None, faculties = []):
        ##11 first rows from dot output are important
        dot = self.create_dot_file(faculties)

        #draw the graph
        p = subprocess.Popen([dot_exec, "-Tsvg"], stdin = subprocess.PIPE, stdout = subprocess.PIPE)

        #get all svg objects
        output, errors = p.communicate(input = dot)
        importnat = (output.splitlines()[0:11])
        importnat = "\n".join(importnat)
        root = ET.fromstring(output)
        gs = get_all_g_tagged_children(root)
        root_elem = get_root_elem(gs)
        root_elem = self.rebuild_tree(root_elem, gs, depth = depth, faculties=faculties)

        res = ET.tostring(root_elem, encoding='utf-8')
        res = importnat + res + "</g>\n"+"<script>\n//<![CDATA[\n"
        with open("visibillityChanger.js", 'r') as script:
            res += script.read()
        res += "\n//]]>\n</script></svg>"
        return res

    def _make_fail_svg(self):
        fail_svg="""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        <parent xmlns="http://example.org"
        xmlns:svg="http://www.w3.org/2000/svg">
        <svg:svg height="30" width="200">
  <svg:text x="0" y="15" fill="red">Wrong course number</svg:text>
</svg:svg></parent>"""
        return  fail_svg

    def write_nexts_to_stream(self, dot_exec, depth = 0, faculties = []):
        try:
            temp = self.create_svg_tree(dot_exec, depth = depth, faculties=faculties)
            print(temp)
        except:
            traceback.print_exc()
            print self._make_fail_svg()

    def write_nexts_to_svg(self, dot_exec, svg = "out.svg"):
        with open(svg, 'w') as out:
            out.write(self.create_svg_tree(dot_exec))


    def write_nexts_to_png(self, dot_exec, png = "out.png"):
        dot = self.create_dot_file()
        #draw the graph
        p = subprocess.Popen([dot_exec, "-Tpng", "-o", png], stdin = subprocess.PIPE)
        output, errors = p.communicate(input = dot)

    def write_nexts_to_png_stream(self, dot_exec):
        dot = self.create_dot_file()
        #draw the graph
        p = subprocess.Popen([dot_exec, "-Tpng"], stdin = subprocess.PIPE)
        output, errors = p.communicate(input = dot)
        print output
