#!/bin/bash
if [ ! -d "${PROJECT_ROOT}/external" ] ; then
	mkdir ${PROJECT_ROOT}/external
fi

PLATFORM=`python -mplatform`

LZ_CONDA_PATH=${PROJECT_ROOT}/external/miniconda/LZ; export LZ_CONDA_PATH
# clean paths
PATH=`python ${PROJECT_ROOT}/bin/remove_from_env.py "$PATH" "${LZ_CONDA_PATH}"`

if [ ! -d "${LZ_CONDA_PATH}" ] ; then
  CONDA_URL=https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
  # create all parent folders except miniconda
  echo "Could not find conda install in ${LZ_CONDA_PATH}. Installing conda ..."
  mkdir -p ${LZ_CONDA_PATH}; rmdir ${LZ_CONDA_PATH}
  wget -nv ${CONDA_URL} -O miniconda.sh
  bash miniconda.sh -b -p ${LZ_CONDA_PATH}
  PATH=${LZ_CONDA_PATH}/bin:$PATH; export PATH
  rm -f miniconda.sh
  echo "Finished conda installation, updating packages"
  conda config --add channels conda-forge
  conda config --add channels nlesc
  conda config --set show_channel_urls yes
  conda update conda -y
  conda update pip -y
  conda install psutil -y
  echo "Finished updating packages, creating new conda environment"
  # create new conda environment with Python 2.7 and ROOT 6
  conda create -n lz python=2.7 -y
  echo "Created conda environment, installing basic dependencies"
  source activate lz
  conda install --file ${PROJECT_ROOT}/conda_packages.txt -y
  # install python packages
  pip install -U -r ${PROJECT_ROOT}/requirements.txt
  # clean the cache (downloaded tarballs)
  conda clean -t -y
  # give the group write access
  chmod g+r -R ${LZ_CONDA_PATH}
else
  echo "Found conda install in ${LZ_CONDA_PATH}, activating..."
  PATH=${LZ_CONDA_PATH}/bin:$PATH; export PATH
  source activate lz
fi
