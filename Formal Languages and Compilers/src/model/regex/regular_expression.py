from dataclasses import dataclass
from collections import defaultdict
from .syntax_tree import SyntaxTree

@dataclass
class RegularExpression:
    
    def __init__(self, er):
        self.er = er
        self.syntax_tree = SyntaxTree().construct_from_regex(postfix_er=er)
    
    def get_leaves(self):
        """Coleta todas as folhas da árvore sintática"""
        leaves_dict = {}
        
        def collect_leaves(node):
            if node is None:
                return
            if node.node_type == 'leaf':
                leaves_dict[node.position] = node.symbol
            collect_leaves(node.left)
            collect_leaves(node.right)
        
        collect_leaves(self.syntax_tree)
        return leaves_dict
    
    def compute_parameters(self):

        def recursion(subtree):
            if subtree.node_type == 'leaf':
                subtree.nullable = (subtree.symbol == '&')
                subtree.firstpos = {subtree.position} if subtree.position else set()
                subtree.lastpos = {subtree.position} if subtree.position else set()

            elif subtree.node_type == '|':
                recursion(subtree.left)
                recursion(subtree.right)
                subtree.nullable = subtree.left.nullable or subtree.right.nullable
                subtree.firstpos = subtree.left.firstpos | subtree.right.firstpos
                subtree.lastpos = subtree.left.lastpos | subtree.right.lastpos

            elif subtree.node_type == '.':
                recursion(subtree.left)
                recursion(subtree.right)
                subtree.nullable = subtree.left.nullable and subtree.right.nullable

                if subtree.left.nullable:
                    subtree.firstpos = subtree.left.firstpos | subtree.right.firstpos
                else:
                    subtree.firstpos = subtree.left.firstpos

                if subtree.right.nullable:
                    subtree.lastpos = subtree.left.lastpos | subtree.right.lastpos
                else:
                    subtree.lastpos = subtree.right.lastpos
            
            elif subtree.node_type == '*' or subtree.node_type == '?':
                recursion(subtree.left)
                subtree.nullable = True
                subtree.firstpos = subtree.left.firstpos
                subtree.lastpos = subtree.left.lastpos
               
            elif subtree.node_type == '+':
                recursion(subtree.left)
                subtree.nullable = subtree.left.nullable
                subtree.firstpos = subtree.left.firstpos
                subtree.lastpos = subtree.left.lastpos
                
        recursion(self.syntax_tree)

    def get_firstpos(self):
        return self.syntax_tree.firstpos
    
    def get_lastpos(self):
        return self.syntax_tree.lastpos

    def get_followpos(self):
        followpos = defaultdict(set)

        def recursion(subtree):
            if subtree is None:
                return
            recursion(subtree.left)
            recursion(subtree.right)

            # Caso de concatenação
            if subtree.node_type == '.':
                for i in subtree.left.lastpos:
                    followpos[i] |= subtree.right.firstpos

            # Caso de estrela
            elif subtree.node_type == '*':
                for i in subtree.lastpos:
                    followpos[i] |= subtree.firstpos

            # Caso de plus (pelo menos um elemento)
            elif subtree.node_type == '+':
                for i in subtree.lastpos:
                    followpos[i] |= subtree.firstpos

        recursion(self.syntax_tree)
        return followpos