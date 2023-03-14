# Code https://github.com/Taschee/schafkopf/blob/master/schafkopf/players/mc_node.py
import numpy as np
class Node:
    def __init__(self, game_state, parent=None, previous_action=None):
        self.children = []
        self.parent = parent
        self.previous_action = previous_action
        self.visits = 0
        self.cumulative_rewards = [0 for i in range(4)]

        # the GameState:
        self.gOptions   = game_state["options"]  # Schafkopf Options
        self.gMoves   = game_state["moves"] 
        self.gInitialHandsIdx = game_state["initialHandsIdx"]
        self.gActive_Player = game_state["activePlayer"]
        self.gGameOver       = game_state["gameOver"]
        self.gActions        = game_state["actions"] # possible actions for current Player

    def add_child(self, child_node):
        self.children.append(child_node)

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def is_terminal(self):
        if self.gGameOver:
            return True
        else:
            return False

    def fully_expanded(self):
        if len(self.children) == len(self.gActions):
            return True
        else:
            return False

    def best_child(self, ucb_const):
        if not self.is_leaf():
            return max(self.children, key=lambda child: child.ucb_value(ucb_const))

    def ucb_value(self, ucb_const):
        if self.visits != 0:
            average_reward = self.get_average_reward(player=self.parent.current_player)
            return average_reward + ucb_const * np.sqrt(2 * np.log(self.parent.visits) / self.visits)
        else:
            return np.infty

    def ucb_values(self, ucb_const):
        return [child.ucb_value(ucb_const) for child in self.children]

    def update_visits(self):
        self.visits += 1

    def update_rewards(self, rewards):
        for i in range(len(self.cumulative_rewards)):
            self.cumulative_rewards[i] += rewards[i]

    def get_average_reward(self, player):
        if self.visits > 0:
            return self.cumulative_rewards[player] / self.visits
        else:
            return 0