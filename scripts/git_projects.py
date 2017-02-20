from __future__ import print_function
import os
from git import GitConfigParser, Repo
import six
import re

# github group
# GROUP = "sim"
# mapping of github user names to aliases (for remotes)
DEVELOPERS = {
    "kreczko": 'luke',
    "benkrikler": 'ben',
}
# LZ has no public repositories at the moment, hence the two are the same
GITHUB_BASE = 'git@lz-git.ua.edu:'
GITHUB_SSH = 'git@lz-git.ua.edu:'
PROJECTS = {
    'BACCARAT': GITHUB_BASE + "sim/BACCARAT.git",
    'DER': GITHUB_BASE + "sim/ElectronicsSimulation.git",
    'TDRAnalysis': GITHUB_BASE + "sim/TDRAnalysis.git",
    'PhotonDetection': GITHUB_BASE + "physics/PhotonDetection.git",
    #'TDRScience': GITHUB_BASE + "TDRScience.git", # this one is 700 MB large
}

globalconfig = GitConfigParser(
    [os.path.normpath(os.path.expanduser("~/.gitconfig"))], read_only=True)
USER = globalconfig.get('user', 'name')


DEV_PATH = os.environ.get('DEV_PATH')

for alias, git_url in six.iteritems(PROJECTS):
    repo_dir = os.path.join(DEV_PATH, alias)
    if os.path.exists(repo_dir):
        print(">> Repo {0} already exists".format(repo_dir))
        continue
    print('>> Cloning {0}'.format(git_url))
    Repo.clone_from(git_url, repo_dir)
    repo = Repo(repo_dir)
    # rename origin
    repo.remotes.origin.rename('upstream')
    group = re.findall(':(.*?)/', git_url, re.DOTALL)[0]
    print('group', group)
    for github_name, dev_alias in six.iteritems(DEVELOPERS):
        remote_url = git_url.replace(group, github_name)
        remote_alias = dev_alias
        if github_name == USER:
            # use git+ssh for the user's fork
            remote_url = remote_url.replace(GITHUB_BASE, GITHUB_SSH)
            remote_alias = 'origin'
        print('>>>> Adding remote {0}'.format(remote_url))
        repo.create_remote(remote_alias, remote_url)
    print('>>>> Fetching all remotes for {0}'.format(alias))
    for remote in repo.remotes:
        try:
            remote.fetch()
        except:
            print('>>>> Could not fetch {0}'.format(remote.url))
