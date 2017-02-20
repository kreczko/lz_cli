source /cvmfs/lz.opensciencegrid.org/ROOT/v5.34.32/slc6_gcc44_x86_64/root/bin/thisroot.sh
source /cvmfs/lz.opensciencegrid.org/geant4/etc/geant4env.sh geant4.9.5.p02

./BACCARATExecutable LZ/LZMacros/LZQuickCheckNoVis.mac
./tools/BaccRootConverter EnergyDeposition_1477452940.bin
./tools/BaccMCTruth EnergyDeposition_1477452940.root
