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

include version
include make.config

.PHONY: default clean distclean archive configure 

default: make.config
	- bash -c "[[ -e lib/libezfio.a ]] && rm $$PWD/lib/*"
	@echo Compiling library && make -C $$PWD/src static
	@echo Building Python module && make -C $$PWD/src python

clean:
	- bash -c "[[ -e lib/libezfio.a ]] && rm $$PWD/lib/*"
	- bash -c "[[ -e Python/ezfio.py ]] && rm $$PWD/Python/*"
	- make -C $$PWD/src veryclean

distclean: clean
	- rm -rf autom4te.cache config.status config.log make.config 

archive: distclean
	git archive --format=tar HEAD > EZFIO.$(VERSION).tar
	mkdir EZFIO ; cd EZFIO ; tar -xvf ../EZFIO.$(VERSION).tar
	rm EZFIO.$(VERSION).tar
	tar -zcvf EZFIO.$(VERSION).tar.gz EZFIO
	rm -rf EZFIO

configure: make.config.in configure.ac
	autoconf 

make.config: 
	./configure --host=dummy

