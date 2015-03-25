#!/usr/bin/env python

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
  if len(sys.argv) == 1:
    print "syntax: %s <EZFIO_Archive.ezar>"%(sys.argv[0])
    sys.exit(1)
  ezfio_filename = sys.argv[1].split(".ezar")[0]

  file = open(ezfio_filename+".ezar","r")
  dump = file.read()
  file.close()

  ezfio.set_filename(ezfio_filename)

  d = pickle.loads(zlib.decompress(dump))

  set_functions = d.keys()

  nerrors_old = len(d)+1
  nerrors = nerrors_old+1
  while nerrors != nerrors_old:
    nerrors_old = nerrors
    nerrors = 0
    failed = []
    for f_name in set_functions:
      try:
        exec """ezfio.%s = d['%s']"""%(f_name,f_name)
      except:
        nerrors += 1
        failed.append(f_name)

  if nerrors != 0:
    print "Unarchive failed:"
    for i in failed:
      print i
    sys.exit(1)

if __name__ == "__main__":
  main()
