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

format= {
 'integer*8'       : ["'(I20)'", "%20d"],
 'integer'         : ["'(I20)'", "%20d"],
 'real'            : ["'(E24.15)'","%24.15E"],
 'double precision': ["'(E24.15)'","%24.15E"],
 'logical'         : ["'(L1)'","%c"],
 'character*(*)'   : ["'(A)'","%s"]
 }

def t_short(x):
  x = x.lower()
  if x == 'integer*8':
    return 'i8'
  elif x == 'integer':
    return 'in'
  elif x == 'real':
    return 're'
  elif x.startswith('double'):
    return 'do'
  elif x == 'logical':
    return 'lo'
  elif x.startswith('character'):
    return 'ch'

f2c = {
'in' : 'int',
're' : 'float',
'i8' : 'long int',
'do' : 'double',
'ch' : 'char',
'lo' : 'int'
}

f2ocaml = {
'in' : 'int',
're' : 'float',
'i8' : 'int64',
'do' : 'float',
'ch' : 'string',
'lo' : 'bool'
}
