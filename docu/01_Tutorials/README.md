## Sheepshead Rules
only RAMSCH supported for now (this is on duty!)


## Monte Carlo Tree Search Player
Player type: "MCTS_OFF_10_50"
* OFF: 
    - OFF means no subsampling: it is assumed that the MCTS Player knows all other cards
    - if you put a number here e.g. MCTS_20_10_50 --> the other player cards are subsampled 20 times and for each subsample the best card is evaluated
* 10: 
    - number of playouts (the higher the better)
    - if this number is higher the tree is more deep
* 50: ucb constant
    - if you choose 1   : expolration
    - if you choose 1000: exploitation

### Monte Carlo Tree Search
A Monte Carlo Tree Search algorithm consists of the following 4 steps
![mcts_algorithm](01_MCTS/mcts_algo.png)

An example for Schafkopf would be:
![mcts_nodes_explained](01_MCTS/mcts_nodes_explained.png)

if you want to save the mcts trees use option "save_tree": 1

### Exploration vs Exploitation
Let's take this example:

![ddd](01_MCTS/seed_451.png)

* Player 1 has ucb_const = 1: MCTS_20_50_**1**:
![ddd](01_MCTS/Tree_move_4ucb_const1.png)
![ddd](01_MCTS/move_ucb_1.png)

* If Player has ucb_const = 1000: MCTS_20_50_**1000**: 
![ddd](01_MCTS/Tree_move_4ucb_const1000.png)
![ddd](01_MCTS/move_ucb_1000.png)

* You can see that the tree for ucb=1 is more deep and the apprently best option GA is exploited more!
* The GA has 23 visits and many other options as e.g. HA, H9, EU is only visited once
* For ucb=1000 you can see that the tree is not so deep but more spread out.
* The GA has 7 visits which is only one more compared to all other nodes