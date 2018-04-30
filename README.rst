EZFIO
=====

EZFIO is the Easy Fortran I/O library generator. It generates
automatically an I/O library from a simple configuration file. The
produced library contains Fortran subroutines to read/write the data
from/to disk, and to check if the data exists.
A Python and an Ocaml API are also provided.

With EZFIO, the data is organized in a file system inside a main
directory. This main directory contains subdirectories, which contain
files. Each file corresponds to a data. For atomic data the file is a
plain text file, and for array data the file is a gzipped text file. 

Download
========

The following packages are needed:

* `IRPF90 <http://irpf90.ups-tlse.fr>`_
* `Python <http://www.python.org>`_
* `GNU make <http://www.python.org>`_ or `Ninja <http://github.com/martine/ninja>`_


Tutorial
========

In this example, we will write a Fortran program which computes
properties of a molecule. The molecule is described as point charges in
the 3D space.

Preparation of the library
--------------------------

Create an empty directory for your project and unpack the ``EZFIO.tar.gz`` file in this directory. This directory now contains:

.. code-block:: bash

  $ ls
  EZFIO/

Get into the ``EZFIO`` directory and configure the library to produce the
desired suboutines. Get into the ``config`` directory and create a new file
``test.config``
containing::

  molecule
    num_atoms   integer
    mass        real      (molecule_num_atoms)
    coord       real      (3,molecule_num_atoms)
  
  properties
    mass              real  = sum(molecule_mass)
    center_of_mass    real  (3)


In this example, ``molecule`` and ``properties`` are containers of data.
Those are defined in the config file by their name at the beginning of a
new line.
Each data contained inside a container is characterized by a triplet
(name,type,dimension), preceded by at least one white space at the
beginning of the line.

If the dimension of an array is a data, the name of the data can be used
as ``<container>_<data>`` in the definition of the dimension. For
example, the dimension (``molecule_num_atoms``) uses the data
``num_atoms`` of container ``molecule``.

Data can also be the result of a simple operation. In that case, the
simple operation is written after an = symbol (as for ``mass`` in the
``properties`` container). In that case, the data is read-only.

Once your configuration file is ready, run ``make`` and your library
will be built.


Building the library
--------------------

Now, go back to the EZFIO root directory. To build with GNU make, run:

.. code-block:: bash

  $ make

Or you can use Ninja to build the library:

.. code-block:: bash

  $ ninja


The ``lib`` directory now contains the static library ``libezfio.a``, and a static
library for use under the IRPF90 environment (``libezfio_irp.a``).
The ``Python``, ``Ocaml`` and ``Bash`` directories contain the binding for these languages.


Using the produced library
--------------------------

In the following, we will call 'EZFIO file' the main directory
containing the EZFIO data.

All the produced libraries contain the following subroutines:

subroutine ezfio_set_read_only(ro)
  If ``ro`` is .True., the read-only attribute is set. It will be
  impossible to write to the EZFIO file.

subroutine ezfio_is_read_only(ro)
  Returns the value of the read_only attribute to ``ro``.

subroutine ezfio_set_file(filename)   
  Only one EZFIO can be manipulated at a time. This subroutine selects
  which file will be manipulated.

subroutine ezfio_get_filename(fname)
  Returns the name of the EZFIO file which is currently manipulated.

For each data, 3 subroutines are created.
<dir> is the name of the container which contains the data and
<data> is the name of the data.

subroutine ezfio_has_<dir>_<data> (has_it)
  ``has_it`` is .True. if the data exists in the EZFIO file, .False. otherwise.

subroutine ezfio_set_<dir>_<data> (source)
  writes the source data to the EZFIO file.

subroutine ezfio_get_<dir>_<data> (destination)
  reads the data from the EZFIO file to the destination.

With our example, the library contains the following subroutines:

.. code-block:: fortran

  subroutine ezfio_set_read_only(ro)
  subroutine ezfio_is_read_only(ro)
  subroutine ezfio_set_file(filename)                           
  subroutine ezfio_get_filename(filename)
  
  subroutine ezfio_set_molecule_num_atoms(num_atoms)
  subroutine ezfio_get_molecule_num_atoms(num_atoms)
  subroutine ezfio_has_molecule_num_atoms(has_it)
  
  subroutine ezfio_set_molecule_mass(mass)
  subroutine ezfio_get_molecule_mass(mass)
  subroutine ezfio_has_molecule_mass(has_it)
  
  subroutine ezfio_set_molecule_coord(coord)
  subroutine ezfio_get_molecule_coord(coord)
  subroutine ezfio_has_molecule_coord(has_it)
  
  subroutine ezfio_get_properties_mass(mass)
  
  subroutine ezfio_set_properties_center_of_mass(center_of_mass)
  subroutine ezfio_get_properties_center_of_mass(center_of_mass)
  subroutine ezfio_has_properties_center_of_mass(has_it)
  
  subroutine ezfio_set_properties_center_of_charge(center_of_charge)
  subroutine ezfio_get_properties_center_of_charge(center_of_charge)
  subroutine ezfio_has_properties_center_of_charge(has_it)

Note that ``ezfio_get_properties_mass`` has only the ``get`` subroutine
since it is computed data.

In Python
---------

All the subroutines are also produced for Python in the ezfio.py file in
the Python directory. To use them, in your Python script, use:

.. code-block:: python

  import sys
  EZFIO = "./EZFIO"  # Put here the absolute path to the EZFIO directory
  sys.path = [ EZFIO+"/Python" ]+sys.path
  from ezfio import ezfio

and all the subroutines will be accessible by replacing the first
underscore character of the name of the subroutine by a dot (``ezfio_``
becomes ``ezfio.``). 

Let us create the input of our Fortran program with a Python script.
Create a file named ``create_input.py`` with:

.. code-block:: python

  #!/usr/bin/python2
  
  import sys
  EZFIO = "./EZFIO"  # Put here the absolute path to the EZFIO directory
  sys.path = [ EZFIO+"/Python" ]+sys.path
  from ezfio import ezfio
  
  # Water molecule:
  # mass, x, y, z
  input = """16.    0.000000    0.222396    0.000000
             1.     1.436494   -0.889660    0.000000
             1.    -1.436494   -0.889660    0.000000  """
  
  Molecule = []
  for line in input.splitlines():
    new_list = map(eval,line.split())
    Molecule.append(new_list)
  
  # Create the mass array
  mass = map( lambda x: x[0], Molecule )
  # print mass
  # [16.0, 1.0, 1.0]
  
  # Create the coord array
  coord = map( lambda x: (x[1], x[2], x[3]), Molecule )
  # print coord
  # [(0.0, 0.222396, 0.0), (1.436494, -0.88966, 0.0), (-1.436494, -0.88966, 0.0)]
  
  # Select the EZFIO file
  ezfio.set_file("Water")
  
  # Add the arrays to the file
  ezfio.molecule_num_atoms = len(Molecule)
  ezfio.molecule_mass = mass
  ezfio.molecule_coord = coord
  
  # Check that the total mass is correct:
  print ezfio.properties_mass   # Should give 18.

Execute the script:

.. code-block:: bash

  $ python2 create_input.py
  18.0

The printed mass is correct, and a new directory (``Water``) was created with our data:

.. code-block:: bash

  $ ls Water/*
  Water/ezfio:
  creation  library  user

  Water/molecule:
  coord.gz  mass.gz  num_atoms

In Fortran
----------

We will create here a Fortran program which reads the atomic coordinates
and the atomic masses from an EZFIO file, computes the coordinates of
the center of mass, and writes the coordinates of the center of mass to
the EZFIO file.

.. code-block:: fortran

  program test
   implicit none
   integer :: num_atoms
   real, allocatable :: mass(:)
   real, allocatable :: coord(:,:)
   real :: center_of_mass(3)
   real :: total_mass
   integer :: i,j
  
  ! Set which file is read/written
   call ezfio_set_file("Water")
  
  ! Read the number of atoms
   call ezfio_get_molecule_num_atoms(num_atoms)
  
  ! Allocate the mass and coord arrays
   allocate(mass(num_atoms), coord(3,num_atoms))
  
  ! Read the arrays from the file
   call ezfio_get_molecule_mass(mass)
   call ezfio_get_molecule_coord(coord)
  
  ! Check that the read data is correct
   print *, 'Data in the EZFIO file:'
   do i=1,num_atoms
    print *, mass(i), (coord(j,i),j=1,3)
   end do
  ! prints:
  ! Data in the EZFIO file:
  !   16.00000       0.000000      0.2223960       0.000000    
  !   1.000000       1.436494     -0.8896600       0.000000    
  !   1.000000      -1.436494     -0.8896600       0.000000    
  
  ! Perform the calculation of the center of mass
   do j=1,3
    center_of_mass(j) = 0.
   end do
  
   do i=1,num_atoms
    do j=1,3
     center_of_mass(j) = center_of_mass(j) + mass(i)*coord(j,i)
    end do
   end do
  
   call ezfio_get_properties_mass(total_mass)
   do j=1,3
    center_of_mass(j) = center_of_mass(j)/total_mass
   end do
  
   deallocate(mass, coord)
  
  ! Write the center of mass to the EZFIO file
   call ezfio_set_properties_center_of_mass(center_of_mass)
  
  end

Compile the fortran program and link it the ``libezfio.a`` library, and run the
executable.

.. code-block:: bash

  $ gfortran test.f90 EZFIO/lib/libezfio.a -o test.x
  $ ./test.x
  Data in the EZFIO file:
     16.0000000       0.00000000      0.222396001       0.00000000    
     1.00000000       1.43649399     -0.889660001       0.00000000    
     1.00000000      -1.43649399     -0.889660001       0.00000000    



A new directory (``properties``) was created with the center_of_mass
file:

.. code-block:: bash

  $ ls Water/*
  Water/ezfio:
  creation

  Water/molecule:
  coord.gz  mass.gz  num_atoms

  Water/properties:
  center_of_mass.gz


Using Bash
----------

To use EZFIO in Bash, you need to source the ``ezfio.sh`` file:

.. code-block:: bash

  $ source EZFIO/Bash/ezfio.sh

The usage of the ``ezfio`` bash command is::

  ezfio set_file    EZFIO_DIRECTORY
  ezfio unset_file 

  ezfio has         DIRECTORY   ITEM
  ezfio get         DIRECTORY   ITEM
  ezfio set         DIRECTORY   ITEM  VALUE  : Scalar values
  ezfio set         DIRECTORY   ITEM         : Array values read from stdin

  ezfio set_verbose
  ezfio unset_verbose


Here is the same script as the Python script, but using Bash (``create_input.sh``):

.. code-block:: bash

  #!/bin/bash
  
  source EZFIO/Bash/ezfio.sh
  
  # Select the EZFIO file
  ezfio set_file Water
  
  # Set the number of atoms
  ezfio set molecule num_atoms 3
  
  # Create the mass array
  mass="[16.0, 1.0, 1.0]"
  echo $mass | ezfio set molecule mass
  
  # Create the coordinates
  cat << EOF | ezfio set molecule coord
  [
  [ 0.000000,  0.222396, 0.0],
  [ 1.436494, -0.889660, 0.0],
  [-1.436494, -0.889660, 0.0]
  ]
  EOF
  
  # Check that the total mass is correct:
  ezfio get properties mass      # Should print 18.



