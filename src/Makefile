IRPF90= python ~/Work/Project/p16.03/irpf90/src/irpf90.py
IRPF90FLAGS=  -I ./
BUILD_SYSTEM= make

export LD_LIBARY_PATH = 
export CXX = g++
export CXXFLAGS = -O2
export CC = gcc
export FC = gfortran
export CFLAGS = -O2
export FCFLAGS = -O2
export AR = AR
export RANLIB = ranlib

ifeq ($(BUILD_SYSTEM),ninja)
	CMD_PHONY=-t  # Chose a specific target
	BUILD_FILE=IRPF90_temp/build.ninja
	IRPF90FLAGS += -j # Create ninja
else
	CMD_PHONY= -j # All job abalaible
	BUILD_FILE=IRPF90_temp/build.make
endif

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))

.PHONY: static all

export PYTHONPATH:=$(current_dir):$(PYTHONPATH)

all: static ../Python/ezfio.py ../Ocaml/ezfio.ml

static: ../lib/libezfio.a ../lib/libezfio_irp.a

../lib/libezfio.a: IRPF90_temp/irpf90.a
	rm -f ../lib/libezfio.a
	cp  IRPF90_temp/irpf90.a ../lib/libezfio.a
	$(RANLIB) ../lib/libezfio.a


../lib/libezfio_irp.a: ../lib/libezfio.a
	cp ../lib/libezfio.a ../lib/libezfio_irp.a

../Python/ezfio.py:
	python create_python.py

../Ocaml/ezfio.ml:
	python create_ocaml.py

IRPF90_temp/irpf90.a: $(BUILD_FILE)
	$(BUILD_SYSTEM) -C $(dir $^) -f $(notdir $^) $(CMD_PHONY) $(current_dir)$@ && touch $@

$(BUILD_FILE): $(shell find . -path ./IRPF90_temp -prune -o -name '*.irp.f' -maxdepth 2  -print)
	$(IRPF90) $(IRPF90FLAGS)

clean: $(BUILD_FILE)
	$(BUILD_SYSTEM) -f $^ $(CMD_PHONY) clean
	rm -f $(BUILD_FILE)
	rm -f ../lib/libezfio.a ../lib/libezfio_irp.a	

veryclean: clean
	rm -rf IRPF90_temp/ IRPF90_man/ irpf90_entities dist tags $(EXE)
