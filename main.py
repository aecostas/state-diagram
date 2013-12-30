#
# Node style
#   solid
#   dashed
#   dotted
#   bold
#   rounded
#   diagonals
#   filled
#   striped
#   wedged
#

import re
import os
import sys
import gv
import os, os.path
import getopt
import argparse

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

STYLE_SEPARATOR = ':'

def main(argv):
    outputfile = "state.png"

    f = open('data', 'r')
    gr = digraph()
    for line in f:
        command = line.rstrip()
        if command.startswith('#'):
            continue;

        if command is "":
            continue

        fields = command.split(STYLE_SEPARATOR)
        if fields[0].startswith('node'):
            # define a new node
            # ex.: ['node A', 'dashed']
            newnode = fields[0].split(' ')
            gr.add_node(newnode[1])
        else:
            #arrow
            edge = fields[0].split(',')
            try:
                comment_tmp = fields[1].split(',')
            except IndexError:
                comment_tmp = ''
                
            arrow = edge[0]
            try:
                arrow_color = edge[1]
            except IndexError:
                arrow_color = ''

            try:
                comment = comment_tmp[0]
            except IndexError:
                comment = ''

            try:
                comment_color = comment_tmp[1]
            except IndexError:
                comment_color = arrow_color

            if '-->' in arrow:
                attrs = []
                attrs.append(('style','dashed'))
                attrs.append(('fontcolor', comment_color))
                start = arrow.index('-->')
                node_from = arrow[0:start]
                node_to = arrow[start+3:]
                attrs.append(('label', comment))
                attrs.append(('color', arrow_color))

                gr.add_edge((node_from, node_to), attrs=attrs)

            elif '->' in arrow and '-->' not in arrow:
                attrs = []
                attrs.append(('style',''))
                attrs.append(('fontcolor', comment_color))
                start = arrow.index('->')
                node_from = arrow[0:start]
                node_to = arrow[start+2:]
                attrs.append(('label', comment))
                attrs.append(('color', arrow_color))

                gr.add_edge((node_from, node_to), attrs=attrs)

            elif '..>' in arrow:
                attrs = []
                attrs.append(('style','dotted'))
                attrs.append(('fontcolor', comment_color))
                start = arrow.index('..>')
                node_from = arrow[0:start]
                node_to = arrow[start+3:]
                attrs.append(('label', comment))
                attrs.append(('color', arrow_color))

                gr.add_edge((node_from, node_to), attrs=attrs)

    # Draw as PNG
    dot = write(gr)
    gvv = gv.readstring(dot)
    gv.layout(gvv,'dot')
    gv.render(gvv,'png', outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
