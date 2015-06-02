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

ezfio = ezfio_obj()

def main():
  import pprint
  import sys
  import os

  try:
    EZFIO_FILE = os.environ["EZFIO_FILE"]
  except KeyError:
    print "EZFIO_FILE not defined"
    return 1

  ezfio.set_file(EZFIO_FILE)

  command = '_'.join(sys.argv[1:]).lower()

  try:
    f = getattr(ezfio,command)
  except AttributeError:
    print "{0} not found".format(command)
    return 1

  if command.startswith('has'):
      if f(): return 0
      else  : return 1

  elif command.startswith('get'):
      result = f()
      pprint.pprint( result, width=60, depth=3, indent=4 )
      return 0

  elif command.startswith('set'):
      try:
          data = eval(sys.stdin.read())
      except:
          print "Syntax Error"
          return 1
      f(data)
      return 0

  else:
      return 1


if __name__ == '__main__':
  rc = main()
  sys.exit(rc)



