#!/bin/bash
LZ_GEANT_PATH=/cvmfs/lz.opensciencegrid.org/geant4; export LZ_GEANT_PATH
LZ_CLHEP_PATH=/cvmfs/lz.opensciencegrid.org/CLHEP/2.1.0.1; export LZ_CLHEP_PATH
LZ_ROOT_PATH=/cvmfs/lz.opensciencegrid.org/ROOT/v5.34.32/slc6_gcc44_x86_64/root; export LZ_ROOT_PATH
LZ_LUXSIM_PATH=/cvmfs/lz.opensciencegrid.org/LUXSim/release-4.4.6;export LZ_LUXSIM_PATH

# setup all the projects
DOMAIN=`dnsdomainname`
if [ "$DOMAIN" == "nersc.gov" ]; then
  module load Geant4/4.9.5
  module load ROOT/5.34.20
  module load CLHEP/2.2.0.8
else
  source ${LZ_GEANT_PATH}/etc/geant4env.sh geant4.9.5.p02
  source ${LZ_ROOT_PATH}/bin/thisroot.sh
fi

export LD_LIBRARY_PATH=${LZ_CLHEP_PATH}/lib:${LD_LIBRARY_PATH}
export CPATH=/cvmfs/lz.opensciencegrid.org/external/gsl/1.14/include
