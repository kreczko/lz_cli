#!/bin/bash
drop_from_path()
{
   # Assert that we got enough arguments
   if test $# -ne 2 ; then
      echo "drop_from_path: needs 2 arguments"
      return 1
   fi

   p=$1
   drop=$2

   newpath=`echo $p | sed -e "s;:${drop}:;:;g" \
                          -e "s;:${drop};;g"   \
                          -e "s;${drop}:;;g"   \
                          -e "s;${drop};;g"`
}

if [ -n "${HEP_PROJECT_ROOT}" ] ; then
   old_projectbase=${HEP_PROJECT_ROOT}
fi


if [ "x${BASH_ARGV[0]}" = "x" ]; then
    if [ ! -f bin/env.sh ]; then
        echo ERROR: must "cd where/project/is" before calling ". bin/env.sh" for this version of bash!
        HEP_PROJECT_ROOT=; export HEP_PROJECT_ROOT
        return 1
    fi
    HEP_PROJECT_ROOT="$PWD"; export HEP_PROJECT_ROOT
else
    # get param to "."
    envscript=$(dirname ${BASH_ARGV[0]})
    HEP_PROJECT_ROOT=$(cd ${envscript}/..;pwd); export HEP_PROJECT_ROOT
fi

if [ -n "${old_projectbase}" ] ; then
   if [ -n "${PATH}" ]; then
      drop_from_path "$PATH" ${old_projectbase}/bin
      drop_from_path "$PATH" ${old_projectbase}/external/miniconda/bin
      PATH=$newpath
   fi
   if [ -n "${PYTHONPATH}" ]; then
      drop_from_path $PYTHONPATH ${old_projectbase}
      PYTHONPATH=$newpath
   fi
fi

if [ -z "${PATH}" ]; then
   PATH=$HEP_PROJECT_ROOT/bin; export PATH
else
   PATH=$HEP_PROJECT_ROOT/bin:$PATH; export PATH
fi

if [ -z "${PYTHONPATH}" ]; then
   PYTHONPATH=$HEP_PROJECT_ROOT; export PYTHONPATH
else
   PYTHONPATH=$HEP_PROJECT_ROOT:$PYTHONPATH; export PYTHONPATH
fi

unset old_projectbase
unset envscript

# for grid tools
vomsInfo=`which voms-proxy-info` &> /dev/null
if [ "$vomsInfo" = "" ]; then
  if [ -f /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh ]; then
	source /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh
  else
    echo "Cannot find voms-proxy-info nor setup-cvmfs-ui.sh"
  fi
fi

# miniconda setup for modern python and additional python packages
if [ ! -d "${HEP_PROJECT_ROOT}/external" ] ; then
	mkdir ${HEP_PROJECT_ROOT}/external
fi

PLATFORM=`python -mplatform`

if [ ! -d "${HEP_PROJECT_ROOT}/external/miniconda" ] ; then
	wget -nv http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
	bash miniconda.sh -b -p ${HEP_PROJECT_ROOT}/external/miniconda
	PATH=${HEP_PROJECT_ROOT}/external/miniconda/bin:$PATH; export PATH
	rm -f miniconda.sh
	conda update conda -y
	conda update pip -y
	conda create --name lz python=2.7 -y
	source activate lz
	# python modules
	pip install -U python-cjson nose psutil
	if [[ $PLATFORM == *"redhat"* ]]; then
		PYCURL_SSL_LIBRARY=nss pip install --compile pycurl --global-option='--with-nss'
	fi
	if [[ $PLATFORM == *"debian"* ]]; then
		PYCURL_SSL_LIBRARY=openssl pip install --compile pycurl --global-option='--with-openssl'
	fi
	pip install -r ${HEP_PROJECT_ROOT}/requirements.txt

	conda clean -t -y
else
	PATH=${HEP_PROJECT_ROOT}/external/miniconda/bin:$PATH; export PATH
	source activate lz
fi

# now the LZ software
LZ_GEANT_PATH=/cvmfs/lz.opensciencegrid.org/geant4/geant4.9.5.p02; export LZ_GEANT_PATH
LZ_CLHEP_PATH=/cvmfs/lz.opensciencegrid.org/CLHEP/2.1.0.1; export LZ_CLHEP_PATH
LZ_ROOT_PATH=/cvmfs/lz.opensciencegrid.org/ROOT/v5.34.32/slc6_gcc44_x86_64/root; export LZ_ROOT_PATH
LZ_LUXSIM_PATH=/cvmfs/lz.opensciencegrid.org/LUXSim/release-4.4.6;export LZ_LUXSIM_PATH

# setup all the projects
source ${LZ_GEANT_PATH}/bin/geant4.sh
source ${LZ_ROOT_PATH}/bin/thisroot.sh
export LD_LIBRARY_PATH=${LZ_CLHEP_PATH}/lib:${LD_LIBRARY_PATH}
