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


from ezfio import ezfio

EZFIO=ezfio

EZFIO.set_file('icule')
EZFIO.set_system_num_alpha(4)
EZFIO.set_geometry_num_atom(5)
x = [ "label"+str(i) for i in range(5) ]
indices = [ [ 1, 2, 3, 4 ], [ 5, 6, 7, 8] ]
values = [ 10., 20.]
isize = len(indices)
EZFIO.open_write_ao_two_int()
EZFIO.write_buffer(indices,values,isize)
EZFIO.write_buffer(indices,values,isize)
EZFIO.close_write_ao_two_int()
indices = []
values = []
isize = 5
EZFIO.open_read_ao_two_int()
indices,values = EZFIO.read_buffer(isize)
print indices
print values
EZFIO.close_read_ao_two_int()

