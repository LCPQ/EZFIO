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

DEFAULT_TARGET: python

../make.config:
	make -C .. make.config
include ../make.config

include irpf90.make

irpf90.make: $(wildcard *.irp.f) ../config/*
	$(IRPF90)

include ../version

.PHONY: python static

static: ../lib/libezfio_irp.a ../lib/libezfio.a

../lib/libezfio.a: $(OBJ1)
	- bash -c "[[ -e ../libezfio.a ]] && rm ../lib/libezfio.a"
	$(AR) cru ../lib/libezfio.a $(OBJ1)
	$(RANLIB) ../lib/libezfio.a

../lib/libezfio_irp.a: ../lib/libezfio.a
	cp ../lib/libezfio.a ../lib/libezfio_irp.a
	$(AR) dv ../lib/libezfio_irp.a irp_stack.irp.o
	$(RANLIB) ../lib/libezfio_irp.a

test: static
	ifort -o $@ IRPF90_temp/run.irp.F90 -L../lib/ -lezfio

python: static
	cat ezfio-head.py libezfio_groups-gen.py libezfio_util-gen.py ezfio-tail.py > ../Python/ezfio.py

ezfio.py: python

