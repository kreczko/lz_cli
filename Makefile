# simple makefile to simplify repetitive build env management tasks under posix

PYTHON := $(shell which python)
all: clean

clean:
	@cd DEV/BACCARAT && make clean

benchmark:
	@bash ./bin/compare_geant4.9vs4.10 10000
