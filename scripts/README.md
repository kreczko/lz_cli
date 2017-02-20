# Recipes for various subtasks

## cms_extras.sh
Loads CMSSW commands and CRAB

## conda_env.sh
Loads the conda environment for the project or creates it if it does not exist

## git_projects.py and git_projects.sh
Sets up any git projects and their remotes for the current set of developers.
Developers and projects are specified in git_projects.py, eg.

```python
DEVELOPERS = {
    "kreczko": 'luke',
    # "benkrikler": 'ben',
}

PROJECTS = {
    'BACCARAT': GITHUB_BASE + "BACCARAT.git",
    'DER': GITHUB_BASE + "ElectronicsSimulation.git",
}
```

The script will also read `~/.gitconfig` and will set the remotes with respect to the person setting up the current environment.
E.g. if the github user in `~/.gitconfig` is configured to be `kreczko` the remote for that developer will point to `origin` and will use the `git@github` (SSH) URL.

## grid_tools.sh
Setting up the grid tools (`xrd`, `voms-proxy-&`, `gfal-*`, etc).
