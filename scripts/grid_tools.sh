#!/bin/bash
# for grid tools
vomsInfo=`which voms-proxy-info &> /dev/null`
if [ "$vomsInfo" == "" ]; then
  if [ -f /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh ]; then
	source /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh
	# the UI uses an old java version, we do not want that
	unset JAVA_HOME
  else
    echo "Cannot find voms-proxy-info nor setup-cvmfs-ui.sh"
  fi
fi
