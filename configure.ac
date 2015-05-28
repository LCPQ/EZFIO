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
#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

VERSION=[`. version ; echo $VERSION`]
AC_SUBST([VERSION])

AC_REVISION([$Revision: $VERSION $])

AC_PREREQ([2.50])

AC_INIT([EZFIO Library Generator], [], [scemama@irsamc.ups-tlse.fr],[ezfio],[http://ezfio.sourceforge.net])

AC_SYS_LONG_FILE_NAMES
ROOT=`pwd`
AC_SUBST([ROOT])

AC_CONFIG_SRCDIR([src/run.irp.f])
AC_CONFIG_FILES([make.config])
AC_PREFIX_DEFAULT([./])

STATIC_LIB=$ROOT/lib/libezfio.a

AC_PROG_RANLIB

# Test Fortran
# ------------

AC_LANG([Fortran])
AC_PROG_FC([ifort gfortran],[Fortran 90])
AC_PROG_FC_C_O
AC_FC_SRCEXT([F90])
AC_FC_FREEFORM

# Test Python
# ------------

AC_CHECK_PROG([PYTHON],[python],[yes],[no])
if [[ "$PYTHON" = no ]] ; then
  AC_MSG_ERROR([Please install Python.])
fi

# Test Ninja
# -----------

if [[ -z "$NINJA" ]] ; then
  AC_CHECK_PROG([NINJA],[ninja],[yes],[no])
  if [[ "$NINJA" = no ]] ; then
    NINJA=
  fi
fi
AC_SUBST[[NINJA]]

# Test AR
# -------

if [[ -z "$AR" ]] ; then
  AC_CHECK_PROG([AR],[ar],[yes],[no])
  if [[ "$AR" = no ]] ; then
    AC_MSG_ERROR([ar not found.])
  fi
  AR=ar
fi
AC_SUBST([AR])

# Test Gzip and zcat
# ------------------

if [[ -z "$HAS_GZIP" ]] ; then
  AC_CHECK_PROG([GZIP],[gzip],[yes],[no])
  if [[ "$GZIP" = no ]] ; then
    HAS_GZIP="-DNO_GZIP"
  fi
  
  AC_CHECK_PROG([ZCAT],[zcat],[yes],[no])
  if [[ "$ZCAT" = no ]] ; then
    HAS_GZIP="-DNO_GZIP"
  fi
  
  AC_CHECK_PROG([MKFIFO],[mkfifo],[yes],[no])
  if [[ "$MKFIFO" = no ]] ; then
    HAS_GZIP="-DNO_GZIP"
  fi
fi
AC_SUBST([HAS_GZIP])

# Test IRPF90
# ------------

if [[ -z "$IRPF90" ]] ; then
  AC_CHECK_PROG([IRPF90],[irpf90],[yes],[no])
  if [[ "$IRPF90" = no ]] ; then
    AC_MSG_ERROR([Please install IRPF90:\nhttp://irpf90.ups-tlse.fr])
  fi
  IRPF90=`which irpf90`
fi
AC_SUBST([IRPF90])

if [[ -z "$FCFLAGS" ]] ; then
  case $FC in
      ifort*)
         FCFLAGS="-O2 -g -ip"
         STATIC_FC="-static-intel -static-libgcc -static"
         ;;
      gfortran*)
         FCFLAGS="-O2 -g -ffree-line-length-none"
         STATIC_FC="-static-libgcc -static"
         ;;
  esac
fi

# Write make.config

LIB="$STATIC_LIB"
FCFLAGS="$FCFLAGS $STATIC_FC"
AC_SUBST([LIB])

# Done
#-----

AC_OUTPUT


