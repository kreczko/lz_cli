MACRO = """
#Radioactivity in the LS in the screener
/run/verbose 0
/control/verbose 0
/tracking/verbose 0
/event/verbose 0
/grdm/verbose 0

/run/initialize
/Bacc/io/outputDir {output_dir}
/Bacc/io/updateFrequency 10000

# Detector settings
/Bacc/detector/select LZXenonCyl
/Bacc/detector/update

/Bacc/physicsList/useOpticalProcesses true

/Bacc/detector/recordLevel PTFE 2
/Bacc/detector/recordLevel LXe 2
/Bacc/detector/recordLevel photoCathode 2

/Bacc/detector/recordLevelOptPhot LXe  4
/Bacc/detector/recordLevelOptPhot PTFE  4
/Bacc/detector/recordLevelOptPhot photoCathode 3

/Bacc/source/set LXe {process}

/Bacc/io/outputName xenon_photon_{suffix}_
/Bacc/beamOn {nevents}


exit
"""

PROCESSES = {
    'SingleParticle_e': 'LXe SingleParticle_e- 1 mBq/kg 10 keV',
    'SingleParticle_opticalphoton': 'SingleParticle_opticalphoton 1 Bq/kg 6.888 eV',
}
