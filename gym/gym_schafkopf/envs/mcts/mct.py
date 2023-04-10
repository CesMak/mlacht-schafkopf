import random
from gym_schafkopf.envs.mcts.node    import Node
from copy import deepcopy

class MonteCarloTree:
  '''
  Inspired by https://github.com/Taschee/schafkopf/blob/master/schafkopf/players/uct_player.py
  '''
  def __init__(self, game_state, schafobj, ucb_const=1):
    # schafobj is used there as reference to Schafkopf()
    # cause import Schafkopf is not possible here (cause of circular imports error!)
    gS = deepcopy(game_state)
    gS["options"]["type"] = ["RANDOM", "RANDOM", "RANDOM", "RANDOM"] # used for simulation
    gS["options"]["print_"] = 0
    self.root = Node(gS, parent=None, previous_action=None)
    self.ucb_const = ucb_const
    self.rewards = []
    self.gameOver = False
    self.treeList = []
    self.treeFilled = False
    self.schafobj   = schafobj
    self.money      = None

  def uct_search(self, num_playouts=5, print_=False):
    for i in range(num_playouts):
      selected_node = self.selection()
      rewards = self.simulation(selected_node)
      self.backup_rewards(leaf_node=selected_node, rewards=rewards)

    if print_:
      print(self.getTree(node=self.root), "\n-->Depth: ", self.getMaxDepth(), " Elements: ", len(self.treeList))
      self.printTree()
    
    results = {}
    self.root.best_child(ucb_const=self.ucb_const)
    for child in self.root.children:
        results[child.previous_action] = child.visits# alternatively: child.visits, child.get_average_reward(player=child.parent.gActive_Player)
    return results  

  def selection(self):
    current_node = self.root
    while not self.gameOver or current_node.is_terminal():
      if not current_node.fully_expanded():
        return self.expand(current_node)
      else:
        current_node = current_node.best_child(ucb_const=self.ucb_const)
    return current_node

  def expand(self, node):
    not_visited_actions = deepcopy(node.gActions) # possible actions for current player
    for child in node.children:
      not_visited_actions.remove(child.previous_action)

    chosen_action = random.choice(tuple(not_visited_actions))

    s = deepcopy(self.schafobj) # cannot use Schafkopf(node.gOptions) here due to circular import error!
    s.resetGame(node.gOptions)

    s.replayGame(moves=node.gMoves, handCards=node.gInitialHandsIdx)
    self.gameOver, _ , self.money = s.step(customIdx=chosen_action)
    
    new_node = Node(s.getGameState(), parent=node, previous_action=chosen_action)
    new_node.gInitialHandsIdx = node.gInitialHandsIdx

    # use for debugging path to Root:     new_node.get_path()

    node.add_child(child_node=new_node)
    return new_node

  def simulation(self, selected_node):
    if self.gameOver: # special case if is already game over do not expand anymore / create new node!
      return self.money

    s = deepcopy(self.schafobj)  # cannot use Schafkopf(node.gOptions) here due to circular import error!
    s.resetGame(selected_node.gOptions)
    s.replayGame(moves=deepcopy(selected_node.gMoves), handCards=deepcopy(selected_node.gInitialHandsIdx)) # TODO do I need deepcopy here?!
    gO    = s.gameOver

    while not gO:
      gO, _, self.money = s.step()
    return self.money

  def backup_rewards(self, leaf_node, rewards):
    current_node = leaf_node
    while current_node != self.root:
      current_node.update_rewards(rewards)
      current_node.update_visits()
      current_node = current_node.parent
    self.root.update_visits()

  def get_action_count_rewards(self):
    result = {}
    for child in self.root.children:
      if isinstance(child.previous_action, list):
        result[tuple(child.previous_action)] = (child.visits, child.cumulative_rewards)
      else:
        result[child.previous_action] = (child.visits, child.cumulative_rewards)
    return result


  ## below only printing Tree functions:
  def getSimpleDepth(self, node, d=0):
    '''get simple depth at first children always'''
    if len(node.children)>0:
      return self.getDepth(node.children[0], d=d+1)
    else:
      return d

  def getMaxChildren(self):
    '''use getTree for that 
       the child number is the second one
    '''
    if not self.treeFilled:
      self.getTree(self.root)
    max = 0
    for i in self.treeList:
      [_, c, _, _] = i
      if c>max: max=c
    return max+1 # cause it starts counting from

  def getMaxDepth(self):
    '''use getTree for that 
       this is quite easy cause treeList is a list that is already sorted by depth
    '''
    if not self.treeFilled:
      self.getTree(self.root)
    return self.treeList[len(self.treeList)-1][0]+1 # cause it starts counting from 0

  def subfinder(self, mylist, pattern):
      return list(filter(lambda x: x in pattern, mylist))

  def getTree(self, node, d=0):
    '''getTree(self.root) returns e.g. 
    self.treeList = [[0, 0, 37, -1], [0, 1, 34, -1], [0, 2, 39, -1], [0, 3, 36, -1], [0, 4, 32, -1], [0, 5, 41, -1], [1, 0, 40, 36], [1, 0, 40, 39], [1, 1, 32, 36], [1, 1, 32, 39], [1, 2, 38, 36], [1, 2, 38, 39], [1, 3, 33, 36], [1, 3, 33, 39], [1, 4, 39, 39], [1, 5, 34, 39], [2, 0, 37, 32], [2, 0, 41, 40], [2, 1, 35, 32], [2, 1, 36, 40]]
    with:
      [0,       0,           37,      -1],
       depth,   childnumber  action   parent that action belongs to (-1 means root)
    '''
    self.treeFilled = False
    if len(node.children)>0:
      for i,child in enumerate(node.children):
        if child.parent.previous_action is None:
            p = -1
        else:
            p = child.parent.previous_action
        a = [d, i, child.previous_action, p ]
        if len(self.subfinder(self.treeList, [a])) == 0:
          self.treeList.append(a)
          return self.getTree(child, d=d+1)
      if d>0:
        return self.getTree(node.parent, d=d-1)
      else:
        self.treeList.sort()
        self.treeFilled = True
        return self.treeList
    else:
      return self.getTree(node.parent, d=d-1)

  def printTree(self):
    '''[0, 0, 37, -1]
        d  c  a    p     depth child action parent
        Drawing such big trees is hard!!!
        This tree is only correct for the layer 0 and layer 1 !

        This method does not work cause if there are in one depth duplicates 
        e.g. multiple play try to play the same option 40....40 
        then the index finder does not work correctly!

        one Example is this wrong tree:
          
        [[0, 0, 20, -1], [0, 1, 3, -1], [1, 0, 17, 3], [1, 0, 17, 20], [1, 1, 21, 3], [1, 1, 21, 20], [2, 0, 24, 17], [2, 0, 24, 21], [2, 1, 29, 17], [2, 1, 29, 21], [3, 0, 6, 24], [3, 0, 6, 29]] 
        -->Depth:  4  Elements:  12
        0--........................20......................3......................--0

        1--................17.21...................17.21...........................--1

        2--........24.29.29........................................................--2

        3--6..6..................................................................--3
    '''
    res = []
    md = self.getMaxDepth()    -1
    mc = self.getMaxChildren() -1
    depth = 0
    for i in range(md+1):
                            # layers zwischenPlatz   #namen
      one_line = list("---"+len(self.treeList)*4*".."+"---")      
      one_line[0]=str(i)
      one_line[len(one_line)-1]=str(i)
      one_line.append("\n")
      res.append(''.join(one_line))

    for i in self.treeList:
      [d, c, a, p]=i
      if d>depth:
        depth +=1

      ol = list(res[d])
      if d>0:
        e = "".join(res[d-1]).index(str(p))+c*3-8
        ol[e:e+2]=str(a).zfill(2)
      else:
        aa=int(len(one_line)/(mc+2))
        e = 3+aa+aa*c
        ol[e:e+2]=str(a).zfill(2)
      res[d]=''.join(ol)
    for line in res: print(line)