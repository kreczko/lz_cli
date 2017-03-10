# LZ Command Line Interface
## Prerequisites
 1. Make sure you have access to the LZ repositories (lz-git.ua.edu)
 2. Configure SSH access for your gitlab account



## Setup on Scientific Linux 6/7
```
git clone https://github.com/kreczko/lz_cli.git
cd lz_cli
source bin/env.sh
```

## interactive mode
The lz_cli comes with an interactive mode that allows for auto-completion of commands.
To use it simply execute `lz <enter>`.


## Setup on OS X/Ubuntu/Windows
### Prerequisites:
 - installed virtualbox: https://www.virtualbox.org/
 - installed vagrant: https://www.vagrantup.com
```
git clone https://github.com/kreczko/lz_cli.git
cd lz_cli
vagrant up
# wait
vagrant ssh
cd /vagrant
source bin/env.sh
```

## Run LuxSim example
```
lz run luxsim examples/luxsim.mac
# or
DEBUG=1 lz run luxsim examples/luxsim.mac
# if you need additional output
```

# Benchmark suite
 1. Setup lz_cli (either [Setup on Scientific Linux 6/7](#setup-on-scientific-linux-67) or [Setup on OS X/Ubuntu/Windows](#setup-on-os-xubuntuwindows))
 2. run `make benchmark`
 3. Get some coffee/tea/cake
