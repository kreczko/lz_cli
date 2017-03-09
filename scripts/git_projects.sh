#!/bin/bash
DEV_PATH="${PROJECT_ROOT}/DEV";export DEV_PATH

if [ ! -d "${DEV_PATH}" ] ; then
  mkdir ${DEV_PATH}
fi

# need to use SSH agent in order to type the password for the ssh key
if [ "x${SSH_AGENT_PID}" == "x" ] ; then
  killall ssh-agent
  echo "Starting SSH agent"
  eval $(ssh-agent)
  ssh-add -l | grep -q '/home/vagrant/.ssh/id_rsa' || ssh-add
fi


python ${PROJECT_ROOT}/scripts/git_projects.py

# now the paths
BAC_TOOLS=${DEV_PATH}/BACCARAT/tools; export BAC_TOOLS
DER_PATH=${DEV_PATH}/DER/bin; export DER_PATH

# clean
echo ${BAC_TOOLS}
echo ${DER_PATH}
PATH=`python ${PROJECT_ROOT}/bin/remove_from_env.py "$PATH" "${BAC_TOOLS}"`
LD_LIBRARY_PATH=`python ${PROJECT_ROOT}/bin/remove_from_env.py "$LD_LIBRARY_PATH" "${BAC_TOOLS}"`
PATH=`python ${PROJECT_ROOT}/bin/remove_from_env.py "$PATH" "${DER_PATH}"`
#
# # add projects to PATH and PYTHONPATH
PATH=${BAC_TOOLS}:${DER_PATH}:$PATH; export PATH
LD_LIBRARY_PATH=${BAC_TOOLS}:$LD_LIBRARY_PATH; export LD_LIBRARY_PATH
