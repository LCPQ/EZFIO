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



#--------
# Fortran
#--------

path = """
BEGIN_PROVIDER [ character*(128), path_%(group)s ]
  BEGIN_DOC
! Path to the %(group)s group
  END_DOC

  logical :: ezfio_exists

  path_%(group)s = trim(libezfio_filename)//'/%(group)s'
  if (.not.ezfio_exists(path_%(group)s)) then
    if (.not.libezfio_read_only) then
      call ezfio_mkdir(path_%(group)s)
    endif
  endif

END_PROVIDER
"""

attributes = """
BEGIN_PROVIDER [ %(type)s, %(group)s_%(var)s ]
  implicit none
  BEGIN_DOC
! %(var)s attribute of group %(group)s
  END_DOC

  call ezfio_read_%(type_short)s(path_%(group)s,'%(var)s',%(group)s_%(var)s)

END_PROVIDER

subroutine ezfio_set_%(group)s_%(var)s(%(var)s)
  implicit none
  BEGIN_DOC
! Sets the %(group)s/%(var)s attribute
  END_DOC
  %(type_set)s :: %(var)s
  call ezfio_write_%(type_short)s(path_%(group)s,'%(var)s',%(var)s)
  FREE %(group)s_%(var)s
end subroutine

subroutine ezfio_get_%(group)s_%(var)s(%(var)s)
  implicit none
  BEGIN_DOC
! Gets the %(group)s/%(var)s attribute
  END_DOC
  %(type)s :: %(var)s
  %(var)s = %(group)s_%(var)s
end subroutine

subroutine ezfio_has_%(group)s_%(var)s(result)
  implicit none
  BEGIN_DOC
! True if the %(group)s/%(var)s attribute exists in the EZFIO directory
  END_DOC
  logical :: result
  inquire(file=trim(path_%(group)s)//'/%(var)s',exist=result)
end subroutine

subroutine ezfio_free_%(group)s_%(var)s()
  implicit none
  BEGIN_DOC
! Frees the memory for %(group)s/%(var)s
  END_DOC
  FREE %(group)s_%(var)s
end
"""

attributes_arr = """
BEGIN_PROVIDER [ %(type)s, %(group)s_%(var)s, %(dims)s ]
  BEGIN_DOC
! %(var)s attribute of group %(group)s
  END_DOC

  integer :: rank, dim_max, i
  integer :: dims(10)
  rank = %(rank)s
  %(dims_loop)s
  dim_max = %(dim_max)s
  call ezfio_read_array_%(type_short)s(path_%(group)s,'%(var)s', &
   rank,dims,dim_max,%(group)s_%(var)s)

END_PROVIDER

subroutine ezfio_set_%(group)s_%(var)s(%(var)s)
  implicit none
  BEGIN_DOC
! Sets the %(group)s/%(var)s attribute
  END_DOC
  %(type_set)s :: %(var)s (*)
  integer :: rank, dim_max, i
  integer :: dims(10)
  rank = %(rank)s
  character*(1024) :: message
%(dims_loop)s
  call ezfio_write_array_%(type_short)s(path_%(group)s,'%(var)s', &
   rank,dims,%(dim_max)s,%(var)s)
  FREE %(group)s_%(var)s
end subroutine

subroutine ezfio_get_%(group)s_%(var)s(%(var)s)
  implicit none
  BEGIN_DOC
! Gets the %(group)s/%(var)s attribute
  END_DOC
  %(type)s, intent(out) :: %(var)s (*)
  character*(1024) :: message
  %(var)s(1: %(dim_max)s ) = reshape ( %(group)s_%(var)s, (/ %(dim_max)s /) )
end subroutine

subroutine ezfio_has_%(group)s_%(var)s(result)
  implicit none
  BEGIN_DOC
! True if the %(group)s/%(var)s attribute exists in the EZFIO directory
  END_DOC
  logical :: result
  inquire(file=trim(path_%(group)s)//'/%(var)s.gz',exist=result)
end subroutine

subroutine ezfio_free_%(group)s_%(var)s()
  implicit none
  BEGIN_DOC
! Frees the memory for %(group)s/%(var)s
  END_DOC
  FREE %(group)s_%(var)s
end
"""

calculated="""
BEGIN_PROVIDER [ %(type)s, %(group)s_%(var)s ]
 BEGIN_DOC  
! Calculated as %(expr)s
 END_DOC
 %(group)s_%(var)s = %(expr)s
END_PROVIDER

subroutine ezfio_get_%(group)s_%(var)s(%(var)s)
  implicit none
  BEGIN_DOC
! Gets the %(group)s/%(var)s attribute
  END_DOC
  %(type)s, intent(out) :: %(var)s
  %(var)s = %(group)s_%(var)s
end

subroutine ezfio_free_%(group)s_%(var)s()
  implicit none
  BEGIN_DOC
! Frees the memory for %(group)s/%(var)s
  END_DOC
  FREE %(group)s_%(var)s
end
"""

buffered="""
subroutine ezfio_open_read_%(group)s_%(var)s()
 implicit none
 BEGIN_DOC
! Opens the read buffer for %(group)s/%(var)s
 END_DOC
 call ezfio_open_read_buffer(path_%(group)s,'%(var)s',%(dims)s)
end

subroutine ezfio_open_write_%(group)s_%(var)s()
 implicit none
 BEGIN_DOC
! Opens the write buffer for %(group)s/%(var)s
 END_DOC
 call ezfio_open_write_buffer(path_%(group)s,'%(var)s',%(dims)s)
end

subroutine ezfio_close_read_%(group)s_%(var)s()
 implicit none
 BEGIN_DOC
! Closes the read buffer for %(group)s/%(var)s
 END_DOC
 call ezfio_close_read_buffer(path_%(group)s,'%(var)s')
end

subroutine ezfio_close_write_%(group)s_%(var)s()
 implicit none
 BEGIN_DOC
! Closes the write buffer for %(group)s/%(var)s
 END_DOC
 call ezfio_close_write_buffer(path_%(group)s,'%(var)s')
end

subroutine ezfio_has_%(group)s_%(var)s(result)
  implicit none
  BEGIN_DOC
!  If the %(group)s_%(var)s, returns True
  END_DOC
  logical :: result
  inquire(file=trim(path_%(group)s)//'/%(var)s.gz',exist=result)
end subroutine

subroutine ezfio_free_%(group)s_%(var)s()
  implicit none
  BEGIN_DOC
! Frees the memory for %(group)s/%(var)s
  END_DOC
 FREE %(group)s_%(var)s
end
"""



#---------
# C
#---------

attributes_c = """
void ezfio_set_%(group)s_%(var)s(%(ctype)s %(var)s)
{
  ezfio_set_%(group)s_%(var)s_(&%(var)s);
}

void ezfio_get_%(group)s_%(var)s(%(ctype)s *%(var)s)
{
  ezfio_get_%(group)s_%(var)s_(%(var)s);
}

int ezfio_has_%(group)s_%(var)s()
{
  ezfio_has_%(group)s_%(var)s_();
}
"""

attributes_arr_c = """
void ezfio_set_%(group)s_%(var)s(%(ctype)s %(var)s)
{
  ezfio_set_%(group)s_%(var)s_(&%(var)s);
}

void ezfio_get_%(group)s_%(var)s(%(ctype)s *%(var)s)
{
  ezfio_get_%(group)s_%(var)s_(%(var)s);
}

int ezfio_has_%(group)s_%(var)s()
{
  ezfio_has_%(group)s_%(var)s_();
}
"""

calculated_c = attributes_c

c_header = """#ifndef EZFIO_H\n#define EZFIO_H

#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct
{
  int* indices;
  double* values;
} sparse;

void ezfio_set_file(char* filename)
{
  long len;
  len = strlen(filename);
  ezfio_set_file_(filename,len);
}

sparse ezfio_read_buffer(int isize)
{
  sparse result;
  ezfio_read_buffer_(result.indices,result.values,&isize);
  return result;
}

void ezfio_write_buffer(sparse data, int isize)
{
  ezfio_write_buffer_(data.indices,data.values,&isize);
}

"""

c_footer = """
#ifdef  __cplusplus
}
#endif
#endif
"""




#--------
# Python
#--------

path_py = """
  def get_path_%(group)s(self):
    result = self.filename.strip()+'/%(group)s'
    self.acquire_lock('%(group)s')
    try:
     if not self.exists(result):
       self.mkdir(result)
    finally:
     self.release_lock('%(group)s')
    return result

  path_%(group)s = property(fget=get_path_%(group)s)
"""

attributes_py = """
  def get_%(group)s_%(var)s(self):
    self.acquire_lock('%(group)s_%(var)s')
    try:
     result = self.read_%(type_short)s(self.path_%(group)s,'%(var)s')
    finally:
     self.release_lock('%(group)s_%(var)s')
    return result

  def set_%(group)s_%(var)s(self,%(var)s):
    self.acquire_lock('%(group)s_%(var)s')
    try:
     self.write_%(type_short)s(self.path_%(group)s,'%(var)s',%(var)s)
    finally:
     self.release_lock('%(group)s_%(var)s')

  %(group)s_%(var)s = property(fset=set_%(group)s_%(var)s, \
     fget=get_%(group)s_%(var)s)

  def has_%(group)s_%(var)s(self):
    return (os.access(self.path_%(group)s+'/%(var)s',os.F_OK) == 1)
"""

attributes_arr_py = """
  def get_%(group)s_%(var)s(self):
    rank = %(rank)s
    dims = range(rank)
%(dims_loop_py)s
    dim_max = 1
    for d in dims:
      dim_max *= d
    self.acquire_lock('%(group)s_%(var)s')
    try:
     result = self.read_array_%(type_short)s(self.path_%(group)s,'%(var)s', rank,dims,dim_max)
    finally:
     self.release_lock('%(group)s_%(var)s')
    return result

  def set_%(group)s_%(var)s(self,%(var)s):
    rank = %(rank)s
    dims = range(rank)
%(dims_loop_py)s
    dim_max = 1
    for d in dims:
      dim_max *= d
    self.acquire_lock('%(group)s_%(var)s')
    try:
     self.write_array_%(type_short)s(self.path_%(group)s,'%(var)s', rank,dims,dim_max,%(var)s)
    finally:
     self.release_lock('%(group)s_%(var)s')

  %(group)s_%(var)s = property(fset=set_%(group)s_%(var)s,fget=get_%(group)s_%(var)s)

  def has_%(group)s_%(var)s(self):
    return (os.access(self.path_%(group)s+'/%(var)s.gz',os.F_OK) == 1)
"""

calculated_py="""
  def get_%(group)s_%(var)s(self):
    return %(expr_py)s

  %(group)s_%(var)s = property(fget=get_%(group)s_%(var)s)
"""

buffered_py="""
  def open_read_%(group)s_%(var)s(self):
    self.open_read_buffer(self.path_%(group)s,'%(var)s',%(dims_py)s)

  def open_write_%(group)s_%(var)s(self):
    self.open_write_buffer(self.path_%(group)s,'%(var)s',%(dims_py)s)

  def close_read_%(group)s_%(var)s(self):
    self.close_buffer()

  def close_write_%(group)s_%(var)s(self):
    self.close_buffer()

  def has_%(group)s_%(var)s(self):
    return (os.access(self.path_%(group)s+'/%(var)s.gz',os.F_OK) == 1)
"""



