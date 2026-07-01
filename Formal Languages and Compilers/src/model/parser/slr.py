# Simple LR (SLR) parser for context-free grammars

from dataclasses import dataclass
from typing import Set, List
from graphviz import Digraph
from ..grammar.cfg import CFG

@dataclass(frozen=True)
class SLR:
    grammar: CFG

    @property
    def augmented_grammar(self) -> CFG:
        """Property to get the augmented grammar."""
        return self.get_augmented_grammar()
    
    def get_augmented_grammar(self) -> CFG:
        """Generate the augmented grammar by adding a new start production: E' -> E"""
        if self.grammar.S.startswith('<') and self.grammar.S.endswith('>'):
             augmented_start_symbol = f"<{self.grammar.S[1:-1]}'>"
        else:
             augmented_start_symbol = self.grammar.S + "'"
        
        P_dict = {augmented_start_symbol: [[self.grammar.S]]}
        for head, bodies in self.grammar.P.items():
            P_dict[head] = bodies
        
        N = self.grammar.N.copy()
        N.add(augmented_start_symbol)
        return CFG(N=N,
                   T=self.grammar.T,
                   S=augmented_start_symbol,
                   P=P_dict)
    
    def closure(self, I: Set[tuple]) -> Set[tuple]:
        J = set(I)
        added = True
        while added:
            added = False
            new_items = set()
            for (A, before_dot, after_dot) in J:
                if after_dot and after_dot[0] in self.grammar.N:
                    B = after_dot[0]
                    if B in self.grammar.P:
                        for prod_body in self.grammar.P[B]:
                            prod_body_tuple = tuple(prod_body) if isinstance(prod_body, list) else tuple(prod_body)
                            item = (B, tuple(), prod_body_tuple)
                            if item not in J:
                                new_items.add(item)
            if new_items:
                J |= new_items
                added = True
        return J


    def goto(self, I: Set[tuple], X: str) -> Set[tuple]:
        moved = set()
        for (A, before_dot, after_dot) in I:
            if after_dot and after_dot[0] == X:
                moved.add((A, before_dot + (X,), after_dot[1:]))
        return self.closure(moved)


    def LR0_items(self) -> list[set[tuple]]:
        """Construct Canonic LR(0) Items"""
        C = []
        start_item = (self.augmented_grammar.S, tuple(), (self.grammar.S,))
        I0 = self.closure({start_item})
        C.append(I0)

        added = True
        while added:
            added = False
            for I in list(C):
                for X in self.grammar.N | self.grammar.T:
                    goto_I_X = self.goto(I, X)
                    if goto_I_X and goto_I_X not in C:
                        C.append(goto_I_X)
                        added = True
        return C


    def build_parsing_table(self):
        """Builds the ACTION and GOTO tables for the SLR parser."""
        C = self.LR0_items()
        follow = self.grammar.follow()

        ACTION = {}
        GOTO = {}

        for i, I in enumerate(C):
            ACTION[i] = {}
            GOTO[i] = {}

            for (A, before_dot, after_dot) in I:
                # Case 1: [A → α • a β], where a ∈ T
                if after_dot and after_dot[0] in self.grammar.T:
                    a = after_dot[0]
                    J = self.goto(I, a)
                    if J in C:
                        j = C.index(J)
                        ACTION[i][a] = ('shift', j)

                # Case 2: [A → α •], reduction or accept
                elif not after_dot:
                    if A == self.augmented_grammar.S:
                        ACTION[i]['$'] = ('accept',)
                    else:
                        # Reduce A → α for all a in FOLLOW(A)
                        for a in follow[A]:
                            ACTION[i][a] = ('reduce', (A, before_dot))

            # Case 3: for nonterminals, define GOTO
            for A in self.grammar.N:
                J = self.goto(I, A)
                if J in C:
                    j = C.index(J)
                    GOTO[i][A] = j

        return ACTION, GOTO

    def parse(self, input_tokens: List[str], return_history: bool = False):
        """Perform LR parsing for a given list of input tokens."""
        ACTION, GOTO = self.build_parsing_table()
        tokens, stack, history = input_tokens + ['$'], [0], []

        while True:
            state, token = stack[-1], tokens[0]
            action = ACTION.get(state, {}).get(token)

            step = {'stack': stack.copy(), 'input': tokens.copy(), 'action': self.format_action(action), 'raw_action': action}
            history.append(step)

            if not action:
                step.update({'action': 'ERROR', 'accepted': False})
                return history if return_history else False

            type, val = action[0], action[1] if len(action) > 1 else None
            if type == 'shift':
                stack.extend([token, val])
                tokens.pop(0)
            elif type == 'reduce':
                A, beta = val
                if beta != ['&'] and beta != tuple(['&']): del stack[-2 * len(beta):]
                stack.extend([A, GOTO[stack[-1]][A]])
            elif type == 'accept':
                step['accepted'] = True
                return history if return_history else True
    
    def format_action(self, action) -> str:
        """Format action tuple for display."""
        if not action: 
            return '-'

        type, val = action[0], action[1] if len(action) > 1 else None

        if type == 'shift': 
            return f's{val}'
        if type == 'reduce': 
            return f'r{self._get_production_number(val[0], val[1])}'
        if type == 'accept': 
            return 'acc'
        return '-'
    
    def _get_production_number(self, head: str, body) -> int:
        """Get production number for reduction display."""
        body = list(body) if isinstance(body, tuple) else body
        
        # Iterate through productions to find index
        idx = 0
        for h, bodies in self.grammar.P.items():
            for b in bodies:
                b_list = list(b) if isinstance(b, tuple) else b
                if h == head and b_list == body:
                    return idx
                idx += 1
        return 0

    def get_lr0_states_count(self) -> int:
        """Get number of LR(0) states."""
        return len(self.LR0_items())
    
    def get_productions_count(self) -> int:
        """Get number of productions in grammar."""
        return sum(len(bodies) for bodies in self.grammar.P.values())

    def generate_canonical_collection_image(self) -> bytes:
        """Generate a PNG image of the Canonical LR(0) collection using graphviz."""
        dot = Digraph(comment="Canonical LR0 Items", format='png')
        dot.attr(rankdir='LR', fontsize='12', dpi='300')
        
        C = self.LR0_items()
        
        # Create nodes for each state
        for i, I in enumerate(C):
            label_lines = [f"I{i}"]
            sorted_items = sorted(list(I), key=lambda x: (x[0], x[1], x[2]))
            
            for (A, before_dot, after_dot) in sorted_items:

                before_str = ' '.join(before_dot) if before_dot else ''
                after_str = ' '.join(after_dot) if after_dot else ''
                
                # Add padding
                if before_str: before_str += ' '
                if after_str: after_str = ' ' + after_str
                
                line = f"{A} -> {before_str}•{after_str}"
                label_lines.append(line)
                
            label = '\n'.join(label_lines)
            dot.node(str(i), label=label, shape='box', fontsize='10', fontname="Courier")

        # Create edges
        for i, I in enumerate(C):
            # Check for ACCEPT state transition (special case)
            for (A, before_dot, after_dot) in I:
                if not after_dot and A == self.augmented_grammar.S:
                    # If we have S' -> S ., this is an accept state
                    dot.node("accept", label="ACCEPT", shape="doublecircle", style="filled", fillcolor="lightgreen")
                    dot.edge(str(i), "accept", label="$")
            
            # Iterate over all possible symbols to find transitions
            symbols = self.grammar.N | self.grammar.T
            for X in symbols:
                goto_I_X = self.goto(I, X)
                if goto_I_X:
                    # Find the index of the target state
                    if goto_I_X in C:
                        j = C.index(goto_I_X)
                        dot.edge(str(i), str(j), label=X)
        
        return dot.pipe()