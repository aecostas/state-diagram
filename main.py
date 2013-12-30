# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Andres Estevez Costas <aecostas@gmail.com>
# Date: 12/30/2013

import re
import sys
import gv
import getopt
import argparse

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

gr = digraph()
STYLE_SEPARATOR = ':'

def create_arrow(node_from, node_to, attrs, nodes):
    if node_from not in nodes:
        gr.add_node(node_from)
        nodes.append(node_from)

    if node_to not in nodes:
        gr.add_node(node_to)
        nodes.append(node_to)

    gr.add_edge((node_from, node_to), attrs=attrs)



def main(argv):
    outputfile = argv[0]+".png"
    f = open(argv[0], 'r')
    nodes = []

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
            nodename = newnode[1]
            if nodename not in nodes:
                nodes.append(nodename)
            gr.add_node(newnode[1])
        else:
            #arrow
            edge = fields[0].split(',')
            arrow = edge[0]

            try:
                comment_tmp = fields[1].split(',')
            except IndexError:
                comment_tmp = ''

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

            attrs = []
            attrs.append(('fontcolor', comment_color))
            attrs.append(('label', comment))
            attrs.append(('color', arrow_color))

            if '-->' in arrow:
                attrs.append(('style','dashed'))
                start = arrow.index('-->')
                node_from = arrow[0:start]
                node_to = arrow[start+3:]
                create_arrow(node_from, node_to, attrs, nodes)

            elif '->' in arrow and '-->' not in arrow:
                attrs.append(('style',''))
                start = arrow.index('->')
                node_from = arrow[0:start]
                node_to = arrow[start+2:]
                create_arrow(node_from, node_to, attrs, nodes)

            elif '..>' in arrow:
                attrs.append(('style','dotted'))
                start = arrow.index('..>')
                node_from = arrow[0:start]
                node_to = arrow[start+3:]
                create_arrow(node_from, node_to, attrs, nodes)


    # Draw as PNG
    dot = write(gr)
    gvv = gv.readstring(dot)
    gv.layout(gvv,'dot')
    gv.render(gvv,'png', outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
