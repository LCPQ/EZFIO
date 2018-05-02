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

 BEGIN_PROVIDER [ integer, PID ]
&BEGIN_PROVIDER [ character*(256), PID_str ]
  implicit none
  BEGIN_DOC
  ! Current process ID
  END_DOC
  integer                        :: getpid
  character*(240)                :: hostname
  PID = getpid()
  write(PID_str,'(I8.8)') PID
  call HOSTNM(hostname)
  write(PID_str,'(A,''.'',I8.8,X)') trim(hostname), PID
  PID_str = trim(PID_str)
END_PROVIDER

logical function ezfio_exists(path)
  implicit none
  BEGIN_DOC
! Checks if a file path exists
  END_DOC
  character*(*)                  :: path
  inquire(file=trim(path)//'/.version',exist=ezfio_exists)
  if (ezfio_exists) then
    open(unit=libezfio_iunit,file=trim(path)//'/.version')
    character*(32)                 :: V
    read(libezfio_iunit,*) V
    close(libezfio_iunit)
  endif
end function

subroutine ezfio_mkdir(path)
  implicit none
  BEGIN_DOC
! Creates a directory
  END_DOC
  character*(*)                  :: path
  logical                        :: ezfio_exists
  if (libezfio_read_only) then
    call ezfio_error(irp_here,'Read-only file.')
  endif
  if (.not.ezfio_exists(path)) then
    call system('mkdir '//trim(path))
    open(unit=libezfio_iunit,file=trim(path)//'/.version')
    write(libezfio_iunit,'(A)') libezfio_version
    close(libezfio_iunit)
  endif
end subroutine 


subroutine libezfio_openz(filename,mode,err)
 implicit none
  BEGIN_DOC
! Opens a compressed file
  END_DOC
 character*(*)                  :: filename, mode
 character*(1024)               :: fifo
 integer                        :: err
 fifo = trim(filename)//'.'//trim(PID_str)
 err=1
 
 if (mode(1:1) == 'r') then
   call system('zcat '//trim(filename)//' > '//trim(fifo))
   open(unit=libezfio_iunit,file=trim(fifo),form='FORMATTED',action='READ')
   err=0
 else if (mode(1:1) == 'w') then
   open(unit=libezfio_iunit,file=trim(fifo),form='FORMATTED',action='WRITE')
   err=0
 else
   call ezfio_error(irp_here,'Mode '//trim(mode)//' is not implemented.')
 endif
end

subroutine libezfio_closez(filename,mode)
 implicit none
  BEGIN_DOC
! Closes a compressed file
  END_DOC
 character*(*)                  :: filename, mode
 character*(1024)               :: fifo
 fifo = trim(filename)//'.'//trim(PID_str)
 if (mode(1:1) == 'w') then
   close(unit=libezfio_iunit)
   call system('gzip -c < '//trim(fifo)//' > '//trim(filename))
   open(unit=libezfio_iunit,file=trim(fifo),form='FORMATTED',action='WRITE')
 endif
 close(unit=libezfio_iunit,status='DELETE')
end


BEGIN_SHELL [ /usr/bin/env python2 ]
from f_types import format, t_short


template = """
subroutine ezfio_read_%(type_short)s(dir,fil,dat)
  implicit none
  BEGIN_DOC
! Reads a %(type_short)s
  END_DOC
  character*(*), intent(in)      :: dir, fil
  %(type)s, intent(out)          :: dat
  character*(1024)               :: l_filename
  l_filename=trim(dir)//'/'//fil
  open(unit=libezfio_iunit,file=l_filename,form='FORMATTED',         &
      action='READ',err=9)
  read(libezfio_iunit,%(fmt)s,end=9,err=9) dat
  close(libezfio_iunit)
  return
9 continue
  call ezfio_error(irp_here,'Attribute '//trim(dir)//'/'//trim(fil)//' is not set')
end

subroutine ezfio_write_%(type_short)s(dir,fil,dat)
  implicit none
  BEGIN_DOC
! Writes a %(type_short)s
  END_DOC
  character*(*), intent(in)      :: dir, fil
  %(type)s, intent(in)           :: dat
  character*(1024)               :: l_filename(2)
  if (libezfio_read_only) then
    call ezfio_error(irp_here,'Read-only file.')
  endif
  l_filename(1)=trim(dir)//'/.'//fil//'.'//trim(PID_str)
  l_filename(2)=trim(dir)//'/'//fil
  open(unit=libezfio_iunit,file=l_filename(1),form='FORMATTED',action='WRITE')
  write(libezfio_iunit,%(fmt)s) dat
  close(libezfio_iunit)
  call system( 'mv -f '//trim(l_filename(1))//' '//trim(l_filename(2)) )
end

subroutine ezfio_read_array_%(type_short)s(dir,fil,rank,dims,dim_max,dat)
  implicit none
  BEGIN_DOC
! Reads a %(type_short)s array
  END_DOC
  character*(*), intent(in)      :: dir, fil
  integer                        :: rank
  integer                        :: dims(rank)
  integer                        :: dim_max
  %(type)s                       :: dat(dim_max)
  integer                        :: err
  character*(1024)               :: l_filename
  l_filename=trim(dir)//'/'//fil//'.gz'
  
  err = 0
  call libezfio_openz(trim(l_filename),'rb',err)
  if (err == 0) then
    integer                        :: rank_read
    integer                        :: dims_read(rank), i
    
    read(libezfio_iunit,'(I3)') rank_read
    if (rank_read /= rank) then
      call ezfio_error(irp_here,'Rank of data '//trim(l_filename)//  &
          ' different from array.')
    endif
    
    if (err /= 0) then
      call ezfio_error(irp_here,'Error reading data in '//trim(l_filename)//&
          '.')
    endif
    read(libezfio_iunit,'(30(I20,X))') dims_read(1:rank)
    do i=1,rank
      if (dims_read(i) /= dims(i)) then
        call ezfio_error(irp_here,'Dimensions of data '//trim(l_filename)//&
            ' different from array.')
      endif
    enddo
    
    do i=1,dim_max
      if (err /= 0) then
        call ezfio_error(irp_here,'Error reading data in '//trim(l_filename)//&
            '.')
      endif
      read(libezfio_iunit,%(fmt)s) dat(i)
    enddo
    call libezfio_closez(trim(l_filename),'r')
    return
  else
    call ezfio_error(irp_here,'Attribute '//trim(l_filename)//' is not set')
  endif
end

subroutine ezfio_write_array_%(type_short)s(dir,fil,rank,dims,dim_max,dat)
  implicit none
  BEGIN_DOC
! Writes a %(type_short)s array
  END_DOC
  character*(*), intent(in)      :: dir, fil
  integer, intent(in)            :: rank
  integer, intent(in)            :: dims(rank)
  integer, intent(in)            :: dim_max
  %(type)s, intent(in)           :: dat(dim_max)
  integer                        :: err
  character*(1024)               :: l_filename(2)
  if (libezfio_read_only) then
    call ezfio_error(irp_here,'Read-only file.')
  endif
  l_filename(1)=trim(dir)//'/.'//fil//trim(PID_str)//'.gz'
  l_filename(2)=trim(dir)//'/'//fil//'.gz'
  
  err = 0
  call libezfio_openz(trim(l_filename(1)),'wb',err)
  if (err == 0) then
    write(libezfio_iunit,'(I3)') rank
    write(libezfio_iunit,'(30(I20,X))') dims(1:rank)
    
    integer                        :: i
    do i=1,dim_max
      write(libezfio_iunit,%(fmt)s) dat(i)
    enddo
    call libezfio_closez(trim(l_filename(1)),'w')
  endif
  call system( 'mv -f '//trim(l_filename(1))//' '//trim(l_filename(2)) )
end
"""

template_no_logical = """
integer function n_count_%(type_short)s(array,isize,val)
  implicit none
  BEGIN_DOC
! Count number of elements of array of type %(type)s
  END_DOC
  %(type)s, intent(in)           :: array(*)
  integer, intent(in)            :: isize
  %(type)s, intent(in)           :: val
  
  integer                        :: i
  n_count_%(type_short)s = 0
  do i=1,isize
    if (array(i) == val) then
      n_count_%(type_short)s = n_count_%(type_short)s +1
    endif
  enddo
end function

! Build Python functions
"""
for t in format.keys():
  print template%{ 'type_short' : t_short(t), 'type' : t, 'fmt':format[t][0] }
  if t != "logical":
    print template_no_logical%{ 'type_short' : t_short(t), 'type' : t, 'fmt':format[t][0] }

template_py = """
  def read_%(type_short)s(self,dir,fil):
    conv = get_conv("%(type_short)s")
    l_filename=dir.strip()+'/'+fil
    try:
      file = open(l_filename,"r")
    except IOError:
      self.error('read_%(type_short)s',\
         'Attribute '+dir.strip()+'/'+fil+' is not set')
    dat = file.readline().strip()
    try:
      dat = conv(dat)
    except SyntaxError:
      pass
    file.close()
    return dat

  def write_%(type_short)s(self,dir,fil,dat):
    if self.read_only:
      self.error('Read-only file.')
    conv = get_conv("%(type_short)s")
    l_filename= [ dir.strip()+'/.'+fil ]
    l_filename += [ dir.strip()+'/'+fil ]
    dat = conv(dat)
    file = open(l_filename[0],'w')
    print >>file,'%(fmt)s'%%(dat,)
    file.close()
    os.rename(l_filename[0],l_filename[1])

  def read_array_%(type_short)s(self,dir,fil,rank,dims,dim_max):
    l_filename=dir.strip()+'/'+fil+'.gz'
    conv = get_conv("%(type_short)s")
    try:
      file = GzipFile(filename=l_filename,mode='rb')
      lines = file.read().splitlines()
      rank_read = int(lines[0])
      assert (rank_read == rank)
     
      dims_read = map(int,lines[1].split())
     
      for i,j in zip(dims_read,dims):
        assert i == j
      
      lines.pop(0)
      lines.pop(0)
      dat = map(conv,lines)

      file.close()
      return reshape(dat,dims)
        
    except IOError:
      self.error('read_array_%(type_short)s', 'Attribute '+l_filename+' is not set')

  def write_array_%(type_short)s(self,dir,fil,rank,dims,dim_max,dat):
    if self.read_only:
      self.error('Read-only file.')
    l_filename = [ tempfile.mktemp(dir=dir.strip()), dir.strip()+'/'+fil+'.gz' ]
    try:
      file = StringIO.StringIO()
      file.write("%%3d\\n"%%(rank,))
      for d in dims:
        file.write("%%20d "%%(d,))
      file.write("\\n")

      dat = flatten(dat)
      for i in xrange(dim_max):
        file.write("%(fmt)s\\n"%%(dat[i],))
      file.flush()
      buffer = file.getvalue()
      file.close()
      file = GzipFile(filename=l_filename[0],mode='wb')
      file.write(buffer)
      file.close()
      os.rename(l_filename[0],l_filename[1])
    except:
      self.error("write_array_%(type_short)s",
        "Unable to write "+l_filename[1])
"""

file_py = open("libezfio_util-gen.py","w")
for t in format.keys():
  print >>file_py, template_py%{ 'type_short' : t_short(t), 'type' : t, 'fmt':format[t][1] }

import os
command = "'echo %s > '//libezfio_filename//'/ezfio/last_library'"
cwd = os.getcwd()
cwd = cwd.split('src')[:-1]
cwd = '/'.join(cwd)
print >>file_py, """
  LIBRARY = "%s"
"""%cwd

file_py.close()

END_SHELL

BEGIN_PROVIDER [ integer, libezfio_buffer_rank ]
 BEGIN_DOC
 ! Rank of the buffer ready for reading
 END_DOC
 libezfio_buffer_rank = -1
END_PROVIDER

subroutine ezfio_open_write_buffer(dir,fil,rank)
  implicit none
  BEGIN_DOC
! Opens a buffer for writing 
  END_DOC
  character*(*),intent(in)       :: dir
  character*(*),intent(in)       :: fil
  integer,intent(in)             :: rank
  character*(1024)               :: l_filename
  if (libezfio_read_only) then
    call ezfio_error(irp_here,'Read-only file.')
  endif
  l_filename=trim(dir)//'/'//fil//'.gz'
  
  if (libezfio_buffer_rank /= -1) then
    call ezfio_error(irp_here,'Another buffered file is already open.')
  endif
  
  libezfio_buffer_rank = rank
  if (libezfio_buffer_rank <= 0) then
    call ezfio_error(irp_here,'In file '//trim(l_filename)//': rank <= 0.')
  endif
  TOUCH libezfio_buffer_rank
  
  integer                        :: err
  call libezfio_openz(trim(l_filename),'wb',err)
  if (err /= 0) then
    call ezfio_error(irp_here,'Unable to open buffered file '//trim(l_filename)//'.')
  endif
  
  write(libezfio_iunit,'(I2)') rank
end

subroutine ezfio_open_read_buffer(dir,fil,rank)
  implicit none
  BEGIN_DOC
! Opens a buffer for reading
  END_DOC
  character*(*),intent(in)       :: dir
  character*(*),intent(in)       :: fil
  integer,intent(in)             :: rank
  character*(1024)               :: l_filename
  l_filename=trim(dir)//'/'//fil//'.gz'
  
  if (libezfio_buffer_rank /= -1) then
    call ezfio_error(irp_here,'Another buffered file is already open.')
  endif
  
  integer                        :: err
  call libezfio_openz(trim(l_filename),'rb',err)
  if (err /= 0) then
    print *,  err, l_filename
    call ezfio_error(irp_here,'Unable to open buffered file '//trim(l_filename)//'.')
  endif
  
  if (err /= 0) then
    print *,  err, l_filename
    call ezfio_error(irp_here,'Unable to read buffered file '//trim(l_filename)//'.')
  endif
  
  read(libezfio_iunit,'(I2)') libezfio_buffer_rank
  if (libezfio_buffer_rank /= rank) then
    call ezfio_error(irp_here,'In file '//trim(l_filename)//': Rank is not correct')
  endif
  TOUCH libezfio_buffer_rank
  
end

subroutine ezfio_close_read_buffer(dir,fil,rank)
  implicit none
  BEGIN_DOC
! Closes a buffer
  END_DOC
  character*(*),intent(in)       :: dir
  character*(*),intent(in)       :: fil
  integer,intent(in)             :: rank
  character*(1024)               :: l_filename
  l_filename=trim(dir)//'/'//fil//'.gz'
  ASSERT (libezfio_buffer_rank > 0)
  call libezfio_closez(l_filename,'r')
  FREE libezfio_buffer_rank
end

subroutine ezfio_close_write_buffer(dir,fil,rank)
  implicit none
  BEGIN_DOC
! Closes a buffer
  END_DOC
  character*(*),intent(in)       :: dir
  character*(*),intent(in)       :: fil
  integer,intent(in)             :: rank
  character*(1024)               :: l_filename
  l_filename=trim(dir)//'/'//fil//'.gz'
  ASSERT (libezfio_buffer_rank > 0)
  call libezfio_closez(l_filename,'w')
  FREE libezfio_buffer_rank
end

subroutine ezfio_read_buffer(indices,values,isize)
  implicit none
  BEGIN_DOC
! Reads a buffer
  END_DOC
  
  integer, intent(inout)         :: isize
  integer, intent(out)           :: indices(*)
  double precision, intent(out)  :: values(isize)
  
  integer                        :: i, j
  
  if (libezfio_buffer_rank == -1) then
    call ezfio_error(irp_here,'No buffered file is open.')
  endif
  
  do i=1,isize
    read(libezfio_iunit,err=10) (indices((i-1)*libezfio_buffer_rank+j), j=1,libezfio_buffer_rank), values(i)
  enddo
  return
  10 continue
  isize=i-1
end

subroutine ezfio_write_buffer(indices,values,isize)
  implicit none
  BEGIN_DOC
! Writes a buffer
  END_DOC
  
  integer, intent(in)            :: isize
  integer, intent(in)            :: indices(*)
  double precision, intent(in)   :: values(isize)
  
  character*(80)                 :: cformat
  integer                        :: i, j, k, num, imax, l1, l2
  
  if (libezfio_read_only) then
    call ezfio_error(irp_here,'Read-only file.')
  endif
  if (libezfio_buffer_rank == -1) then
    call ezfio_error(irp_here,'No buffered file is open.')
  endif
  
  write(cformat,*) '(',num,'(',libezfio_buffer_rank,'(I4,X),E24.15,A1))'
  write(libezfio_iunit,cformat) ((indices((i-1)*libezfio_buffer_rank+j), j=1,libezfio_buffer_rank),&
      values(i), i=1,isize)
  
end

