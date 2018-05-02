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

BEGIN_PROVIDER [ logical, libezfio_read_only ]
 implicit none
  BEGIN_DOC  
! If true, the EZFIO file is read-only
  END_DOC

  libezfio_read_only = .False.
END_PROVIDER

subroutine ezfio_set_read_only(v)
 implicit none
 BEGIN_DOC
! If true, sets the EZFIO file in a read-only state
 END_DOC
 logical :: v
 libezfio_read_only = v
 TOUCH libezfio_read_only
end subroutine ezfio_set_read_only

subroutine ezfio_is_read_only(v)
 implicit none
 BEGIN_DOC
! True if the EZFIO file is in a read-only state
 END_DOC
  logical :: v
  v = libezfio_read_only
end subroutine ezfio_is_read_only

integer function char_to_version(v)
 implicit none
 BEGIN_DOC
! Computes the version number from a string
 END_DOC
 character*(32), intent(in) :: v
 character*(32) :: vnew
 integer :: i, j, k
 vnew=v
 do i=1,32
  if (vnew(i:i) == '.') then
   vnew(i:i) = ' '
  endif
 enddo
 read(vnew,*) i,j,k
 char_to_version =  j*1000 + i*1000000
end

BEGIN_PROVIDER [ character*(32), libezfio_version ]
 implicit none
 BEGIN_DOC  
! Version of the library
 END_DOC
 BEGIN_SHELL [/bin/sh]
  echo libezfio_version = \"`cat ../version | cut -d '=' -f 2` \"
 END_SHELL
END_PROVIDER

BEGIN_PROVIDER [ character*(128), libezfio_filename ]
  implicit none
  BEGIN_DOC
! Name of the EZFIO filesystem 
  END_DOC

  libezfio_filename = 'EZFIO_File'

END_PROVIDER

subroutine ezfio_get_filename(fname)
  implicit none
 BEGIN_DOC
! Returns the name of the EZFIO file
 END_DOC
  character*(*) :: fname
  fname = libezfio_filename
end subroutine

BEGIN_PROVIDER [ integer, libezfio_iunit ]
  implicit none
  BEGIN_DOC
! Unit number for I/O access
  END_DOC

  logical            :: is_open
  is_open = .True.
  libezfio_iunit = 99
  do while (is_open)
    inquire(unit=libezfio_iunit,opened=is_open)
    if (is_open) then
      libezfio_iunit = libezfio_iunit-1
    endif
    if (libezfio_iunit == 9) then
      call ezfio_error(irp_here,'No more free file units!')
    endif
  enddo
  if ( (libezfio_iunit < 10).or.(libezfio_iunit > 99) ) then
    call ezfio_error(irp_here,'No more free units for files.')
  endif
END_PROVIDER

logical function exists(path)
  implicit none
 BEGIN_DOC
! Returns True if the path exists
 END_DOC
  character*(*) :: path
  character*(32) :: V
  inquire(file=trim(path)//'/.version',exist=exists)
  if (exists) then
    open(libezfio_iunit,file=trim(path)//'/.version')
    read(libezfio_iunit,*) V
    close(libezfio_iunit)
!   integer :: char_to_version
!   if (char_to_version(V) > char_to_version(libezfio_version)) then
!     call ezfio_error(irp_here, 'This file was generated with version '//trim(V)//&
!     '  but the current installed version is '//trim(libezfio_version)//'')
!   endif
  endif
end function

subroutine ezfio_set_file(filename_in)
  implicit none
 BEGIN_DOC
! Sets the file for I/O
 END_DOC

  character*(*) :: filename_in

  if (filename_in == '') then
    call ezfio_error(irp_here,'EZFIO file name is empty.')
  endif
  libezfio_filename = filename_in

  logical  :: exists
  if (.not.exists(libezfio_filename)) then
    call ezfio_mkdir(libezfio_filename)
    call ezfio_mkdir(trim(libezfio_filename)//'/ezfio')
    call system('LANG= date > '//trim(libezfio_filename)//'/ezfio/creation')
    call system('echo $USER > '//trim(libezfio_filename)//'/ezfio/user')
    BEGIN_SHELL [ /usr/bin/env python2 ]
import os
command = "'echo %s > '//trim(libezfio_filename)//'/ezfio/library'"
cwd = os.getcwd()
cwd = cwd.split('src')[:-1]
cwd = '/'.join(cwd)
print "call system("+command%cwd+")"
    END_SHELL
  endif

  TOUCH libezfio_filename
end subroutine

subroutine ezfio_finish()
 implicit none
 BEGIN_DOC
! Close all open buffers
 END_DOC
 close(libezfio_iunit)
 BEGIN_SHELL [ /usr/bin/env python2 ]
import os
from zlib import crc32
print '  call irp_finalize_%s'%(str(abs(crc32(os.getcwd()))))
 END_SHELL
end
