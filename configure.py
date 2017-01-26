#!/usr/bin/env python

import os,sys

def write_if_different(filename,s):
  try:
    with open(filename, "r") as f:
        ref = f.read()
  except:
    ref = ""

  if ref == s:
      return
  else:
      with open(filename, "w") as f:
        f.write(s)
    
  
with open("version",'r') as f:
    version = f.read().strip().rsplit('=')[1]

d_default = {
  "VERSION" : version,
  "IRPF90" : 'irpf90',
  "FC" : 'gfortran -g -ffree-line-length-none -fPIC',
  "FCFLAGS" : '-O2',
  "RANLIB" : 'ranlib',
  "AR" : 'ar',
  "BUILD_SYSTEM" : 'make'
}

CONFIG_FILES=' '.join([ os.path.join("config",x) for x in os.listdir('config') if x != '.empty'])

def create_make_config():

    try:
        d = read_make_config()
    except:
        d = {}

    fmt = { "make.config" :'{0}={1}\n' , 
            ".make.config.sh": 'export {0}="{1}"\n' }
    
    for var,default in d_default.iteritems():
        if var not in d:
            try:
                cur = os.environ[var] 
            except KeyError:
                cur = default
            d[var]=cur
        
    for filename in fmt:
        out = ""
        for var,default in d_default.iteritems():
            cur = d[var]
            out += fmt[filename].format(var,cur)
        write_if_different(filename,out)
    
    return d



def read_make_config():
    result = {}
    with open("make.config",'r') as f:
        for line in f.readlines():
          try:
            key, value = line.strip().split('=',1)
          except:
            print "Error in make.config:"
            print line
            sys.exit(1)
          result[key] = value
    return result


def create_build_ninja():
    
    d=create_make_config()

    d["irpf90_files"] = [ "src/{0}".format(x) for x in
        """
        IRPF90_temp/build.ninja irpf90.make irpf90_entities
        tags libezfio_groups-gen.py libezfio_util-gen.py
        """.split() ] 

    d["irpf90_sources"] = [ "src/{0}".format(x) for x in
        """
        libezfio_error.irp.f create_ocaml.py groups_templates.py
        libezfio_file.irp.f create_python.py 
        libezfio_groups.irp.f ezfio-head.py  
        libezfio_util.irp.f ezfio-tail.py read_config.py 
        f_types.py test.py groups.py 
        """.split() ] + [ "make.config" ]

    d["irpf90_files"] = ' '.join(d["irpf90_files"])
    d["irpf90_sources"] = ' '.join(d["irpf90_sources"])
        

    template = """

rule compile_irpf90
   command = bash -c 'source .make.config.sh ; cd src ; {IRPF90} --ninja'
   description = Compiling IRPF90

rule build_irpf90_a
   command = {NINJA} -C src/IRPF90_temp && touch $out
   description = Compiling Fortran files

rule build_libezfio_a
   command = cp src/IRPF90_temp/irpf90.a lib/libezfio.a ; {RANLIB} lib/libezfio.a
   description = Building libezfio.a

rule build_libezfio_irp_a
   command = cp lib/libezfio.a lib/libezfio_irp.a ; {RANLIB} lib/libezfio_irp.a
   description = Building libezfio_irp.a

rule build_python
   command = cd src ; python create_python.py
   description = Building Python module

rule build_ocaml
   command = cd src ; python create_ocaml.py
   description = Building Ocaml module

build {irpf90_files}: compile_irpf90 | {irpf90_sources} {CONFIG_FILES}

build src/IRPF90_temp/irpf90.a: build_irpf90_a | {irpf90_files}

build lib/libezfio.a: build_libezfio_a | src/IRPF90_temp/irpf90.a

build lib/libezfio_irp.a: build_libezfio_irp_a | lib/libezfio.a

build Python/ezfio.py: build_python | lib/libezfio.a

build Ocaml/ezfio.ml: build_ocaml | lib/libezfio.a

"""
    d["CONFIG_FILES"] = CONFIG_FILES
    write_if_different('generated.ninja',template.format(**d))


if __name__ == '__main__':
	create_build_ninja()
