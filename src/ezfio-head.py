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

import os, sys
import time
import cStringIO as StringIO
from gzip import GzipFile
import tempfile
import threading

def version(x):
  b = [int(i) for i in x.split('.')]
  return b[2] + b[1]*100 + b[0]*10000

def size(x):
  return len(x)

def flatten(l):
  res = []
  for i in l:
    if hasattr(i, "__iter__") and not isinstance(i, basestring):
      res.extend(flatten(i))
    else:
      res.append(i)
  return res
    
def maxval(l):
  return reduce(max, l, l[0])

def minval(l):
  return reduce(min, l, l[0])


def reshape(l,shape):
 l = flatten(l)
 for d in shape[:-1]:
   buffer = []
   buffer2 = []
   i=0
   while i<len(l):
    buffer2.append(l[i])
    if len(buffer2) == d:
      buffer.append(buffer2)
      buffer2 = []
    i+=1
   l = list(buffer)
 return l

def at(array,index):
  return array[index-1]

def n_count_ch(array,isize,val):
  result = 0
  for i in array:
    if i == val:
      result +=1
  return result
    
n_count_in = n_count_ch
n_count_do = n_count_ch
n_count_lo = n_count_ch


def get_conv(type):
  if type in ["do","re"]:
    conv = float
  elif type in ["in","i8"]:
    conv = int
  elif type == "lo":
    def conv(a):
      if a == True:
        return 'T'
      elif a == False:
        return 'F'
      elif a.lower() == 't':
        return True
      elif a.lower() == 'f':
        return False
      else:
        raise TypeError
  elif type == "ch":
    conv = lambda x: x.strip()
  else:
    raise TypeError
  return conv

class ezfio_obj(object):

  def __init__(self,read_only=False):
    self._filename = "EZFIO_File"
    self.buffer_rank = -1
    self.read_only = read_only
    self.locks = {}
  
  def acquire_lock(self,var):
    locks = self.locks
    try:
      locks[var].acquire()
    except:
      locks[var] = threading.Lock()
      locks[var].acquire()

  def release_lock(self,var):
    self.locks[var].release()

  def set_read_only(self,v):
    self.read_only = v

  def get_read_only(self):
    return self.read_only

  def exists(self,path):
    if os.access(path+'/.version',os.F_OK) == 1:
      file = open(path+'/.version',"r")
      v = file.readline().strip()
      file.close()
    else:
      return False

  def mkdir(self,path):
    if self.read_only:
      self.error('Read-only file.')
    if self.exists(path):
      self.error('mkdir','Group '+path+' exists')
    try:
      os.mkdir(path.strip())
    except OSError:
      pass
    file = open(path.strip()+'/.version','w')
    print >>file,self.version
    file.close()

  def error(self,where,txt):
    print '------------------------------------------------------------'
    print 'EZFIO File     : '+self.filename
    print 'EZFIO Error in : '+where.strip()
    print '------------------------------------------------------------'
    print ''
    print txt.strip()
    print ''
    print '------------------------------------------------------------'
    raise IOError

  def get_filename(self):
    if not self.exists(self._filename):
      self.mkdir(self._filename)
    return self._filename

  def set_filename(self,filename):
    self._filename = filename

  filename = property(fset=set_filename,fget=get_filename)

  def set_file(self,filename):
    self.filename = filename
    if not self.exists(filename):
      self.mkdir(filename)
      self.mkdir(filename+"/ezfio")
      os.system("""
LANG= date > %s/ezfio/creation
echo $USER > %s/ezfio/user
echo %s > %s/ezfio/library"""%(filename,filename,self.LIBRARY,filename))

  def open_write_buffer(self,dir,fil,rank):
    if self.read_only:
      self.error('Read-only file.')
    l_filename=dir.strip()+'/'+fil+'.gz'
    if self.buffer_rank != -1:
      self.error('open_write_buffer','Another buffered file is already open.')

    self.buffer_rank = rank
    assert (self.buffer_rank > 0)

    try:
      self.file = GzipFile(filename=l_filename,mode='wb7')
    except IOError:
      self.error('open_write_buffer','Unable to open buffered file.')

    self.file.write("%2d\n"%(rank,))


  def open_read_buffer(self,dir,fil,rank):
    l_filename=dir.strip()+'/'+fil+'.gz'

    if self.buffer_rank != -1:
      self.error('open_read_buffer','Another buffered file is already open.')

    try:
      self.file = GzipFile(filename=l_filename,mode='rb')
    except IOError:
      self.error('open_read_buffer','Unable to open buffered file.')

    try:
      rank = eval(self.file.readline())
    except IOError:
      self.error('open_read_buffer','Unable to read buffered file.')

    self.buffer_rank = rank
    assert (self.buffer_rank > 0)
    return rank

  def close_buffer(self):
    assert (self.buffer_rank > 0)
    self.buffer_rank = -1
    self.file.close()

  def read_buffer(self,isize):

    if self.buffer_rank == -1:
      self.error('read_buffer','No buffered file is open.')

    indices = []
    values = []
    for i in xrange(isize):
      try:
        line = self.file.readline().split()
      except:
        return indices, values
      if len(line) == 0:
        return indices, values
      indices.append ( [ int(i) for i in line[:-1] ] )
      values.append (eval(line[-1]))
    return indices, values

  def write_buffer(self,indices,values,isize):
    if self.read_only:
      self.error('Read-only file.')
    if self.buffer_rank == -1:
      self.error('write_buffer','No buffered file is open.')

    for i in xrange(isize):
     for j in indices[i]:
       self.file.write("%4d "%(j,))
     self.file.write("%24.15e\n"%(values[i],))

