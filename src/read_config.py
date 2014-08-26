#!/usr/bin/python
#   EZFIO is an automatic generator of I/O libraries
#   Copyright (C) 2009 Anthony SCEMAMA, CNRS
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#   Anthony Scemama
#   LCPQ - IRSAMC - CNRS
#   Universite Paul Sabatier
#   118, route de Narbonne      
#   31062 Toulouse Cedex 4      
#   scemama@irsamc.ups-tlse.fr


# Read ezfio config file
#----------------------

import os, sys
lines = []
for filename in [ '../config/'+i for i in os.listdir('../config')]:
  file = open(filename,'r')
  lines += map(lambda x: (x,filename), file.readlines())
  try:
    if lines[-1] != '':
      lines.append( ('', filename) )
  except:
     pass
  file.close()

import re

groups = {}
group = None
my_list = []
for line, filename in lines:
  try:

    if len(line.strip()) == 0:
      groups[group] = my_list
    elif line[0] != ' ':  # New group
      group = line.strip()
      if group in groups.keys():
        my_list = groups[group] 
      else:
        my_list = []
    else:
      line = line.replace("double precision","double_precision")
      line = line.split('=')
      if len(line) == 1:
        command = ""
      else:
        command = line[1].strip()
      line = line[0]
      buffer = line.split()
      if len(buffer) == 2:
        buffer += ["()"]
      else:
        buffer[2] = re.sub(r"\)",r',)',buffer[2])
      if buffer[1] == "double_precision":
        buffer[1] = "double precision"
      buffer[2] = re.sub(r"([a-zA-Z0-9_\-\+*/]+)",r'"\1"',buffer[2])
      buffer[2] = eval(buffer[2])
      buffer.append(command)
      my_list.append(tuple(buffer))
  except:
    import sys, time
    print >>sys.stderr, ''
    print >>sys.stderr, '*'*80
    print >>sys.stderr, 'Error in EZFIO config file '+filename+' :'
    print >>sys.stderr, line
    print >>sys.stderr, '*'*80
    print >>sys.stderr, ''
    time.sleep(3)
    sys.exit(1)

