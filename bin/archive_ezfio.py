#!/usr/bin/env python

import sys
import os
sys.path = [ os.path.dirname(__file__)+"/../Python" ]+sys.path
import cPickle as pickle
from ezfio import ezfio_obj, ezfio

# Hide errors
def f(where,txt):
  raise IOError
ezfio.error = f


def main():
  if len(sys.argv) == 1:
    print "syntax: %s <EZFIO_Filename>"%(sys.argv[0])
    sys.exit(1)
  ezfio_filename = sys.argv[1]

  ezfio.set_filename(ezfio_filename)

  get_functions = filter(
    lambda x: x.startswith("has_"),
    ezfio_obj.__dict__.keys() )

  d = {}
  for f in get_functions:
    f_name = f[4:]
    try:
      exec """d['%s'] = ezfio.%s"""%(f_name,f_name)
    except:
      print "%-40s [%5s]"%(f_name, "Empty")
    else:
      print "%-40s [%5s]"%(f_name, " OK  ")

  dump = pickle.dumps(d)
  file = open(ezfio_filename+".ezar","w")
  file.write(dump)
  file.close()


if __name__ == "__main__":
  main()
