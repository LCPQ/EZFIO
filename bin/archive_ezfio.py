#!/usr/bin/env python2

import sys
import os
sys.path = [ os.path.dirname(__file__)+"/../Python" ]+sys.path
import cPickle as pickle
import zlib
from ezfio import ezfio_obj, ezfio

# Hide errors
def f(where,txt):
  raise IOError
ezfio.error = f


def main():
  do_verbose = False
  if "-v" in sys.argv:
    do_verbose = True
    sys.argv.remove("-v")

  if len(sys.argv) == 1:
    print "syntax: %s <EZFIO_Filename>"%(sys.argv[0])
    sys.exit(1)
  ezfio_filename = sys.argv[1]
  while ezfio_filename[-1] == "/":
    ezfio_filename = ezfio_filename[:-1]

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
      if do_verbose:
        print "%-40s [%5s]"%(f_name, "Empty")
    else:
      if do_verbose:
        print "%-40s [%5s]"%(f_name, " OK  ")

  dump = zlib.compress(pickle.dumps(d))
  file = open(ezfio_filename+".ezar","w")
  file.write(dump)
  file.close()


if __name__ == "__main__":
  main()
