BUILD_SYSTEM= make

.EXPORT_ALL_VARIABLES:
include ../make.config

# Dark magic below modify with caution!
# "You are Not Expected to Understand This"
#                     .
#           /^\     .
#      /\   "V",
#     /__\   I      O  o
#    //..\\  I     .
#    \].`[/  I
#    /l\/j\  (]    .  O
#   /. ~~ ,\/I          .
#   \\L__j^\/I       o
#    \/--v}  I     o   .
#    |    |  I   _________
#    |    |  I c(`       ')o
#    |    l  I   \.     ,/
#  _/j  L l\_!  _//^---^\\_


ifeq ($(BUILD_SYSTEM),ninja)
	BUILD_FILE=IRPF90_temp/build.ninja
	IRPF90FLAGS += -j
else ifeq ($(BUILD_SYSTEM),make)
	BUILD_FILE=IRPF90_temp/build.make
	BUILD_SYSTEM += -j
else
DUMMY:
	$(error 'Wrong BUILD_SYSTEM: $(BUILD_SYSTEM)')
endif

define run_and_touch
        $(BUILD_SYSTEM) -C $(dir $(1) ) -f $(notdir $(1) ) $(addprefix $(CURDIR)/, $(2)) && touch $(2)
endef

export PYTHONPATH:=$(CURDIR):$(PYTHONPATH)


.PHONY: static all

all: static ../Python/ezfio.py ../Ocaml/ezfio.ml
static: ../lib/libezfio.a ../lib/libezfio_irp.a

../lib/libezfio.a: IRPF90_temp/irpf90.a
	rm -f ../lib/libezfio.a
	cp  IRPF90_temp/irpf90.a ../lib/libezfio.a
	$(RANLIB) ../lib/libezfio.a

#No more irp_stack
../lib/libezfio_irp.a: ../lib/libezfio.a
	cp ../lib/libezfio.a ../lib/libezfio_irp.a

../Python/ezfio.py:
	python create_python.py

../Ocaml/ezfio.ml:
	python create_ocaml.py

IRPF90_temp/irpf90.a: $(BUILD_FILE)
	$(call run_and_touch, $<, $@)

$(BUILD_FILE): $(shell find .  -maxdepth 2 -path ./IRPF90_temp -prune -o -name '*.irp.f' -print) ../config/*
	$(IRPF90) $(IRPF90FLAGS)

clean:
	rm -f -- $(BUILD_FILE) $(shell find IRPF90_temp -type f \( -name "*.o" -o -name "*.mod" -name "*.a" \)  -delete;)
	rm -f ../lib/libezfio.a ../lib/libezfio_irp.a

veryclean: clean
	rm -rf IRPF90_temp/ IRPF90_man/ irpf90_entities dist tags
