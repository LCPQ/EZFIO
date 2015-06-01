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

DEFAULT_TARGET: all

include ../make.config
export

include irpf90.make

irpf90.make: $(wildcard *.irp.f) ../config/* 
	$(IRPF90)

include ../version

.PHONY: static all

all: static 

static: ../lib/libezfio.a ../lib/libezfio_irp.a

../lib/libezfio.a: IRPF90_temp/irpf90.a
	rm -f ../lib/libezfio.a
	$(AR) cru ../lib/libezfio.a $(OBJ1)
	$(RANLIB) ../lib/libezfio.a

../lib/libezfio_irp.a: ../lib/libezfio.a
	rm -f ../lib/libezfio_irp.a
	cp ../lib/libezfio.a ../lib/libezfio_irp.a
	$(AR) dv ../lib/libezfio_irp.a irp_stack.irp.o
	$(RANLIB) ../lib/libezfio_irp.a

test: static
	$(FC) -o $@ IRPF90_temp/run.irp.F90 -L../lib/ -lezfio

