!   EZFIO is an automatic generator of I/O libraries
!   Copyright (C) 2009 Anthony SCEMAMA, CNRS
!
!   This program is free software; you can redistribute it and/or modify
!   it under the terms of the GNU General Public License as published by
!   the Free Software Foundation; either version 2 of the License, or
!   (at your option) any later version.
!
!   This program is distributed in the hope that it will be useful,
!   but WITHOUT ANY WARRANTY; without even the implied warranty of
!   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!   GNU General Public License for more details.
!
!   You should have received a copy of the GNU General Public License along
!   with this program; if not, write to the Free Software Foundation, Inc.,
!   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
!
!   Anthony Scemama
!   LCPQ - IRSAMC - CNRS
!   Universite Paul Sabatier
!   118, route de Narbonne      
!   31062 Toulouse Cedex 4      
!   scemama@irsamc.ups-tlse.fr

subroutine ezfio_error(where,txt)
  implicit none
  BEGIN_DOC
! Prints an error message
  END_DOC
  character*(*) :: where
  character*(*) :: txt
  character*(128) :: fname

  fname = libezfio_filename
  print *,  '------------------------------------------------------------'
  print *,  'EZFIO File     : '//trim(fname)
  print *,  'EZFIO Error in : '//trim(where)
  print *,  '------------------------------------------------------------'
  print *,  ''
  print *,  trim(txt)
  print *,  ''
  print *,  '------------------------------------------------------------'
  stop 
end subroutine

