#!/usr/bin/env python2
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
from f_types import t_short, f2c

file_py = open("libezfio_groups-gen.py","w")
file = open("../version","r")
v = file.readline()
file.close()
v = v.split('=')[1].strip()
print >>file_py, """
  def get_version(self):
    return '%s'
  version = property(fset=None,fget=get_version)
"""%(v)

import sys

for group in groups.keys():
  print path%{ 'group' : group }
  print >>file_py, path_py%{ 'group' : group }
  for var,type,dims,command in groups[group]:
    command_py = command
    dims_py = str(dims)
    for g in groups.keys():
      command_py = command_py.replace(g,'self.'+g)
      dims_py = dims_py.replace(g,'self.'+g)
    var = var.lower()
    group = group.lower()
    strdims = tuple(map(lambda x: '('+str(x)+')',dims))
    strdims = str(strdims).replace("'","")
    if len(dims) == 1:
      strdims = strdims[:-2]+")"
    dim_max = strdims[1:-1].replace(',','*')
    type_set = type
    cstring = ""
    cstring2 = ""
    if type.lower().startswith('character'):
      type_set = 'character*(*)'
      cstring = ',long size_'+var+'_string'
      cstring2 = ',strlen(size_'+var+'_string)'
    if dims == ():
      if command == "":
        d = { 'type_short': t_short(type),
              'type': type,
              'ctype': f2c[t_short(type)],
              'cstring': cstring,
              'cstring2': cstring2,
              'type_set': type_set,
              'var': var,
              'group': group,
              'dims': strdims}
        print attributes%d
        print >>file_py, attributes_py%d
      else:
        d = { 'type': type,
              'var': var,
              'ctype': f2c[t_short(type)]+"*",
              'cstring': cstring,
              'group': group,
              'expr': command,
              'expr_py': command_py}
        buffer = calculated%d
        buffer = re.sub(r"at\((.*),(.*)\)",r'\1(\2)',buffer)
        print buffer
        print >>file_py, calculated_py%d
    elif type == "buffered":
      d = { 'group': group,
            'var': var,
            'dims_py': dims_py,
            'dims': dims }
      print buffered%d
      print >>file_py, buffered_py%d
    else:
      dims_loop = ''
      copy_loop = ''
      dims_loop_py = ''
      declar_loop = '  integer :: '
      for k,d in enumerate(dims):
        declar_loop += "i"+str(k+1)+","
      declar_loop = declar_loop[:-1]
      for k,d in enumerate(dims):
        dims_loop += "  dims("+str(k+1)+") = "+str(d)+"\n"
        dims_loop_py += "    dims["+str(k)+"] = "+str(d)+"\n"
      for k,d in enumerate(dims):
        copy_loop += k*" "+"  do i"+str(k+1)+"=1,"+str(d)+'\n'
      copy_loop += (k+1)*" "+"  %(var)s ("
      for k,d in enumerate(dims):
        copy_loop += "i"+str(k+1)+","
      copy_loop = copy_loop[:-1] + ") = %(group)s_%(var)s ("
      for k,d in enumerate(dims):
        copy_loop += "i"+str(k+1)+","
      copy_loop = copy_loop[:-1]%{'var': var,'group': group} + ")\n"
      for k,d in enumerate(dims):
        copy_loop += (len(dims)-k-1)*" "+"  enddo\n"
      for g in groups.keys():
        dims_loop_py = dims_loop_py.replace(" "+g,' self.'+g)
        dims_loop_py = dims_loop_py.replace("*"+g,'*self.'+g)
        dims_loop_py = dims_loop_py.replace("/"+g,'/self.'+g)
        dims_loop_py = dims_loop_py.replace("+"+g,'+self.'+g)
        dims_loop_py = dims_loop_py.replace("-"+g,'-self.'+g)
        dims_loop_py = dims_loop_py.replace("("+g,'(self.'+g)
      d = { 'type_short': t_short(type),
            'type': type,
            'type_set': type_set,
            'var': var,
            'ctype': f2c[t_short(type)]+"*",
            'cstring': cstring,
            'group': group,
            'rank' : str(len(dims)),
            'dims': strdims,
            'dim_max': str(dim_max),
            'dims_loop': dims_loop,
            'dims_loop_py': dims_loop_py,
            'copy_loop': copy_loop,
            'declar_loop' : declar_loop}
      print attributes_arr%d
      print >>file_py, attributes_arr_py%d

file_py.close()
