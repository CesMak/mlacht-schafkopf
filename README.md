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
```

# Use Environmment
```python
import gym_examples
env = gymnasium.make('gym_examples/GridWorld-v0')
```

# Run Unit Tests
```bash
cd /schafkopf/schafkopf_docu/gym_tests

# run all testclasses
python -m unittest discover -v
# run a single testmodule (go inside unit folder)
python -m unittest test_player.TestPlayer.test_Options -v

# Code coverage
python -m coverage run -m unittest
python -m coverage report
python -m coverage html
```


# Folder structure
├── mlacht-schafkopf
│   ├── gym_schafkopf
│   │   ├── envs
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── wrappers
│   ├── gym_schafkopf.egg-info
│   │   ├── dependency_links.txt
│   │   ├── PKG-INFO
│   │   ├── requires.txt
│   │   ├── SOURCES.txt
│   │   └── top_level.txt
│   ├── README.md
│   └── setup.py
└── schafkopf_docu
    ├── 01_Tutorials
    ├── 02_Data
    │   ├── class_diag.drawio
    │   ├── class_diag.png
    │   └── details.odp
    ├── gym_tests
    │   ├── integration
    │   └── unit
    ├── LICENSE
    └── README.md

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

## Test Example
```
Max's hand: [EO, GO, EU, GU, HU, EA, E9, SA] type: RANDOM
Lea's hand: [HO, H9, EK, GA, GX, GK, SX, S8] type: RANDOM
Jo's hand: [SU, HA, H8, H7, EX, G9, G7, S7] type: RANDOM
Tim's hand: [SO, HX, HK, E8, E7, G8, SK, S9] type: RANDOM
0-0: Max RANDOM declares weg
0-1: Lea RANDOM declares weg
0-2: Jo RANDOM declares weg
0-3: Tim RANDOM declares weg

1-4: Max RANDOM plays E9
1-5: Lea RANDOM plays H9
1-6: Jo RANDOM plays EX
1-7: Tim RANDOM plays S9
        Winner: Lea with H9 --> 10

2-8: Lea RANDOM plays GX
2-9: Jo RANDOM plays HA
2-10: Tim RANDOM plays G8
2-11: Max RANDOM plays GU
        Winner: Max with GU --> 23

3-12: Max RANDOM plays HU
3-13: Lea RANDOM plays S8
3-14: Jo RANDOM plays H8
3-15: Tim RANDOM plays SK
        Winner: Max with HU --> 6

4-16: Max RANDOM plays EA
4-17: Lea RANDOM plays SX
4-18: Jo RANDOM plays G7
4-19: Tim RANDOM plays E8
        Winner: Max with EA --> 21

5-20: Max RANDOM plays GO
5-21: Lea RANDOM plays EK
5-22: Jo RANDOM plays SU
5-23: Tim RANDOM plays SO
        Winner: Max with GO --> 12

6-24: Max RANDOM plays SA
6-25: Lea RANDOM plays HO
6-26: Jo RANDOM plays S7
6-27: Tim RANDOM plays E7
        Winner: Lea with HO --> 14

7-28: Lea RANDOM plays GK
7-29: Jo RANDOM plays G9
7-30: Tim RANDOM plays HX
7-31: Max RANDOM plays EO
        Winner: Max with EO --> 17

8-32: Max RANDOM plays EU
8-33: Lea RANDOM plays GA
8-34: Jo RANDOM plays H7
8-35: Tim RANDOM plays HK
        Winner: Max with EU --> 17

Max's hand: [] offhand: [[GU, GX, HA, G8], [HU, S8, H8, SK], [EA, SX, G7, E8], [GO, EK, SU, SO], [EO, GK, G9, HX], [EU, GA, H7, HK]] points: 96 --> 45$
Lea's hand: [] offhand: [[E9, H9, EX, S9], [SA, HO, S7, E7]] points: 24 --> -15$
Jo's hand: [] offhand: [] points: 0 --> -15$
Tim's hand: [] offhand: [] points: 0 --> -15$
```