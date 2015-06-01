#!/usr/bin/env python

import os

if __name__ == '__main__':
   
  d_default = {
    "IRPF90" : 'irpf90',
    "FC" : 'gfortran -g -ffree-line-length-none -fPIC',
    "FCFLAGS" : '-O2',
    "RANLIB" : 'ranlib',
    "AR" : 'ar',
    "NINJA" : 'ninja'
    }

  with open("make.config",'w') as out:
      for var,default in d_default.iteritems():
          try:
              cur = os.environ[var] 
          except KeyError:
              cur = default
          out.write("{0} = {1}\n".format(var,cur))
