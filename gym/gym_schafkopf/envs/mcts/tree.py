import graphviz
import random
from gym_schafkopf.envs.helper  import idx2Name 

# TODO ML this tree is only used for visualization at the moment
# you can get rid of all other methods!
class Tree:
    def __init__(self, root_node, schafObj=None):
        self.root_node = root_node
        self.nodes     = {root_node}
        self.schafObj  = schafObj # this is the schafObj and can be used to print metaData!!!

    def add_node(self, node, parent_node):
        self.nodes.add(node)
        parent_node.add_child(node)

    # def backup_rewards(self, leaf_node, rewards):
    #     current_node = leaf_node
    #     while current_node != self.root_node:
    #         current_node.update_rewards(rewards)
    #         current_node.update_visits()
    #         current_node = current_node.parent
    #     self.root_node.update_visits()

    def get_depth(self, node):
        current_node = node
        depth = 0
        while current_node != self.root_node:
            depth += 1
            current_node = current_node.parent
        return depth

    def get_leaves(self):
        leaves = set()
        for node in self.nodes:
            if node.is_leaf():
                leaves.add(node)
        return leaves

    def max_depth(self):
        max_depth = 0
        for node in self.get_leaves():
            depth = self.get_depth(node)
            if depth > max_depth:
                max_depth = depth
        return max_depth

    def average_depth(self):
        all_depths = [self.get_depth(leave) for leave in self.get_leaves()]
        return sum(all_depths) / len(all_depths)

    def visualize_tree(self, format="png", ucb=None, filename=None):
        """Create a visualization of the tree and save it as .png as well as .gv"""
        folder_location = "tests/unit/trees/"
        if filename is None:
            filename = "Tree_{}nodes{}.gv".format(len(self.nodes) - 1, ucb)
        filename=folder_location+filename
        graph = graphviz.Digraph(filename=filename,
                                 format=format,
                                 node_attr={"shape": "ellipse", "fixedsize": "True"})
        self.add_tree(graph=graph,
                      my_root_node=self.root_node, ucb_const=ucb)

        graph.render()

    def add_tree(self, graph, my_root_node, graph_root_name=None, ucb_const=50):
        # recursively add nodes and draw all edges
        if graph_root_name is None:
            graph.node(name="ROOT", label="", **{'width':str(0), 'height':str(0)})
            graph_root_name = "ROOT"
        for child in my_root_node.children:
            new_name = str(random.choice(range(10**10)))
            idx = child.previous_action                    # TODO is the active Player wrong?! for each node?!
            my_label = "<<TABLE BORDER=\"0\"><TR><TD>"+str(child.parent.gActive_Player)+"<FONT COLOR=\""+self.getColor(idx)+"\" POINT-SIZE=\"20.0\"><B>"+idx2Name(idx)+"</B></FONT></TD></TR>  <TR><TD>"+str(child.visits)+" "+str(round(child.ucbVal,1))+"</TD> </TR> </TABLE>>"

            # This highlights the best child according to the ucbVal
            # However I choose currently the best action according to the number of visits!
            best_child = child.parent.best_child(ucb_const)
            if best_child is not None and idx == best_child.previous_action:
                graph.node(name=new_name, label=my_label, fillcolor="grey", style="filled", **{'width':str(0.9), 'height':str(0.9)})

            graph.node(name=new_name, label=my_label, **{'width':str(0.9), 'height':str(0.9)})
            graph.edge(graph_root_name, new_name)
            self.add_tree(graph=graph, my_root_node=child, graph_root_name=new_name)

    def getColor(self, idx):
        if idx<8:
            return "gold2" #-> eichel
        elif idx<16:
            return "green" #-> blatt
        elif idx<24:
            return "red"   #-> herz 
        else:
            return "brown" #-> schell