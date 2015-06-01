#!/usr/bin/env python
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

import re
from read_config import groups
from groups_templates import *
from f_types import t_short, f2ocaml
import os

import sys

def run():

  head = []
  tail = []
  
  file = open("../version","r")
  v = file.readline()
  file.close()
  v = v.split('=')[1].strip()
  l = os.getcwd().replace('/src','')
  head += ["""let version = "%s";;"""%(v),
           """let library = "%s";;"""%(l)]
  
  for group in groups.keys():
     for var,type,dims,command in groups[group]:
       if command is not "":
         continue
       dims_py = str(dims)
       for g in groups.keys():
         dims_py = dims_py.replace(g,'self.'+g)
       var = var.lower()
       group = group.lower()
       strdims = tuple(map(lambda x: '('+str(x)+')',dims))
       strdims = str(strdims).replace("'","")
       if len(dims) == 1:
         strdims = strdims[:-2]+")"
       dim_max = strdims[1:-1].replace(',','*')
       type_set = type
       if type.lower().startswith('character'):
         type_set = 'character*(*)'
       d = { 'type_short': f2ocaml[t_short(type)],
             'type': type,
             'type_set': type_set,
             'var': var,
             'group': group,
             'dims': strdims}
       if dims == ():
         tail += ['let get_%(group)s_%(var)s () = read_%(type_short)s "%(group)s" "%(var)s";;' %(d),
         'let set_%(group)s_%(var)s = write_%(type_short)s "%(group)s" "%(var)s" ;;' %(d) ,
         'let has_%(group)s_%(var)s () = has "%(group)s" "%(var)s" ;;' %(d) ]
       else:
         tail += ['let get_%(group)s_%(var)s () = read_%(type_short)s_array "%(group)s" "%(var)s";;' %(d),
         'let set_%(group)s_%(var)s = write_%(type_short)s_array "%(group)s" "%(var)s";;' %(d) ,
         'let has_%(group)s_%(var)s () = has_array "%(group)s" "%(var)s" ;;' %(d) ]
  
  
  file = open('ezfio.ml','r')
  template = file.read()
  file.close()
  template = template.replace("(*$HEAD*)",'\n'.join(head))
  template = template.replace("(*$TAIL*)",'\n'.join(tail))

  file = open('../Ocaml/ezfio.ml','w')
  file.write(template)
  file.close()

