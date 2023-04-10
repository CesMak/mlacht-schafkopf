# Tutorials
I created some tutorials to explain in detail the code etc.
See **[here](docu/01_Tutorials/README.md)**
# Install
## Install Gym Environment
```bash
git clone https://github.com/CesMak/mlacht-schafkopf.git
cd mlacht-schafkopf
python3 -m venv .env
source .env/bin/activate
cd gym
pip3 install -e .
```
## Install Test Environment
```bash
source .env/bin/activate
## required for testing environment:
pip3 install coverage
pip3 install gymnasium
## required for visualizing MCTS
sudo apt-get install graphviz
pip3 install graphviz
```

# Bash commands
```bash
alias cd_schafkopf='source /home/markus/Documents/06_Software_Projects/mlacht-schafkopf/.env/bin/activate && cd /home/markus/Documents/06_Software_Projects/mlacht-schafkopf'
alias run_all_tests='cd /home/markus/Documents/06_Software_Projects/mlacht-schafkopf/tests/unit && python3 -m coverage run -m unittest && python -m coverage report && cd /home/markus/Documents/06_Software_Projects/mlacht-schafkopf'
```

# Run Unit Tests
```bash
cd /mlacht-schafkopf/tests/unit

# run all testclasses
python -m unittest discover -v
# run a single testmodule (go inside unit folder)
python -m unittest test_player.TestPlayer.test_Options -v

# Code coverage
python -m coverage run -m unittest
python -m coverage report
python -m coverage html
```

Now you can do the **[TUTORIALS](docu/01_Tutorials/README.md)**

<!---
# Use Environmment
```python
import gym_examples
# TODO ML
env = gymnasium.make('gym_examples/GridWorld-v0')
```

# Folder structure
```
├── docu
│   ├── 01_Tutorials
│   └── 02_Data
│       ├── class_diag.drawio
│       ├── class_diag.png
│       └── details.odp
├── gym
│   ├── gym_schafkopf
│   │   ├── envs
│   │   │   ├── card.py
│   │   │   ├── deck.py
│   │   │   ├── player.py
│   │   │   ├── schafkopf_env.py
│   │   │   └── schafkopf.py
│   │   │   ├── helper.py
│   │   │   ├── mcts
│   │   │   │   ├── mct.py
│   │   │   │   ├── node.py
│   │   │   │   └── tree.py
│   ├── gym_schafkopf.egg-info
│   │   ├── dependency_links.txt
│   │   ├── PKG-INFO
│   │   ├── requires.txt
│   │   ├── SOURCES.txt
│   │   └── top_level.txt
│   └── setup.py
├── LICENSE
├── README.md
└── tests
    ├── integration
    └── unit
        ├── test_card.py
        ├── test_deck.py
        ├── test_player.py
        ├── test_schafkopf.py
```


### Environments
This repository hosts the examples that are shown [on the environment creation documentation](https://gymnasium.farama.org/tutorials/environment_creation/).
- `GridWorldEnv`: Simplistic implementation of gridworld environment

### Wrappers
This repository hosts the examples that are shown [on wrapper documentation](https://gymnasium.farama.org/api/wrappers/).
- `ClipReward`: A `RewardWrapper` that clips immediate rewards to a valid range
- `DiscreteActions`: An `ActionWrapper` that restricts the action space to a finite subset
- `RelativePosition`: An `ObservationWrapper` that computes the relative position between an agent and a target
- `ReacherRewardWrapper`: Allow us to weight the reward terms for the reacher environment

### Contributing
If you would like to contribute, follow these steps:
- Fork this repository
- Clone your fork
- Set up pre-commit via `pre-commit install`

--->