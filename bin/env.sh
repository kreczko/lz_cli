#!/bin/bash
if [ -n "${PROJECT_ROOT}" ] ; then
   old_projectbase=${PROJECT_ROOT}
fi


if [ "x${BASH_ARGV[0]}" = "x" ]; then
    if [ ! -f bin/env.sh ]; then
        echo ERROR: must "cd where/project/is" before calling ". bin/env.sh" for this version of bash!
        PROJECT_ROOT=; export PROJECT_ROOT
        return 1
    fi
    PROJECT_ROOT="$PWD"; export PROJECT_ROOT
else
    # get param to "."
    envscript=$(dirname ${BASH_ARGV[0]})
    PROJECT_ROOT=$(cd ${envscript}/..;pwd); export PROJECT_ROOT
fi

if [ -n "${old_projectbase}" ] ; then
  PATH=`python ${PROJECT_ROOT}/bin/remove_from_env.py "$PATH" "${old_projectbase}"`
  PYTHONPATH=`python ${PROJECT_ROOT}/bin/remove_from_env.py "$PYTHONPATH" "${old_projectbase}"`
fi

if [ -z "${PATH}" ]; then
   PATH=$PROJECT_ROOT/bin; export PATH
else
   PATH=$PROJECT_ROOT/bin:$PATH; export PATH
fi

if [ -z "${PYTHONPATH}" ]; then
   PYTHONPATH=$PROJECT_ROOT; export PYTHONPATH
else
   PYTHONPATH=$PROJECT_ROOT:$PYTHONPATH; export PYTHONPATH
fi

unset old_projectbase
unset envscript

# for grid tools
source ${PROJECT_ROOT}/scripts/grid_tools.sh
# now the LZ software
source ${PROJECT_ROOT}/scripts/lz_software.sh
# miniconda setup for modern python and additional python packages
source ${PROJECT_ROOT}/scripts/conda_env.sh
source ${PROJECT_ROOT}/scripts/git_projects.sh

lz setup
