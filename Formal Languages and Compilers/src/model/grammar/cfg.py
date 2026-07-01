# Context Free Grammar (CFG) class
from dataclasses import dataclass, field
from typing import Set, Dict, List, Tuple
import re

@dataclass
class CFG:
    N: Set[str] = field(default_factory=set)      # Non-terminal symbols
    T: Set[str] = field(default_factory=set)      # Terminal symbols
    S: str = None            # Initial symbol
    P: Dict[str, Set[str]] = field(default_factory=dict)   # Production: A ::= δ, such A ∈ N and δ ∈ (N ∪ T)*

    @classmethod
    def from_text(cls, text: str) -> 'CFG':
        """Parse grammar text in format '<S> ::= <A> | b'.
           Non-terminal symbols must be enclosed in < >.
        """
        N, T, P, S = set(), set(), [], None
        
        # Helper to check if a string looks like a potential non-terminal
        def is_potential_nt(s):
            return s.startswith('<') and s.endswith('>')

        for line in [l.strip() for l in text.strip().split('\n') if l.strip()]:
            if '::=' not in line: 
                continue

            head, body_str = map(str.strip, line.split('::=', 1))
            
            if not is_potential_nt(head):
                raise ValueError(f"Head must be a non-terminal enclosed in < >: {head}")
            
            N.add(head)

            if S is None: 
                S = head
            
            for prod_str in [p.strip() for p in body_str.split('|')]:
                if not prod_str:
                    P.append((head, ['&']))
                    continue
                
                # Tokenization using regex: matches <...> or non-whitespace sequences
                tokens = re.findall(r'<[^>]+>|\S+', prod_str)
                
                body = []
                
                for token in tokens:
                    if token == '&': 
                        body.append('&')

                    elif is_potential_nt(token):
                
                        content = token[1:-1]

                        # If the content is alphanumeric, add it to the non-terminal set
                        if any(c.isalnum() or c == '_' for c in content):
                            N.add(token)
                            body.append(token)

                        else:
                            T.add(token)
                            body.append(token)
                    else: 
                        T.add(token); body.append(token)
                
                if not body:
                     P.append((head, ['&']))
                else:
                    P.append((head, body))

        if S is None: raise ValueError("No valid productions found")
        return cls(N, T, S, P)

    def to_text(self) -> str:
        """Convert CFG object back to text format '<S> ::= <E>'."""

        lines = []
        for head, bodies in sorted(self.P.items()):
            body_strs = []
            for body in bodies:
                if body == ['&'] or body == '&': 
                    body_strs.append('&')
                else: 
                    body_strs.append(' '.join(str(s) for s in body))
            lines.append(f"{head} ::= {' | '.join(body_strs)}")
        return '\n'.join(lines)

    # Check if grammar variables are cohesive
    def __post_init__(self):
        # Convert P from list of tuples to dict if needed
        if isinstance(self.P, list):
            P_dict = {}
            for head, body in self.P:
                if head not in P_dict:
                    P_dict[head] = []
                P_dict[head].append(body)
            self.P = P_dict
        
        if self.S not in self.N:
            raise ValueError(f"Initial Symbol (S) must be a non-terminal variable (N). Got: {self.S}")
        
        # Validate productions
        for head in self.P:
            if head not in self.N:
                raise ValueError(f"Left side of production must be a non-terminal variable (N). Got: {head}")
    
    def first(self) -> Dict[str, Set[str]]:
        """Compute FIRST sets for all non-terminals in the grammar."""
        # Initialize FIRST sets for all non-terminals
        first_dict: Dict[str, Set[str]] = {A: set() for A in self.N}

        changed = True
        while changed:
            changed = False
            # Iterate over each production A -> body
            for A, bodies in self.P.items():
                for body in bodies:
                    # Case 1: production derives epsilon
                    if not body or body == ['&']:
                        if '&' not in first_dict[A]:
                            first_dict[A].add('&')
                            changed = True
                        continue

                    # Case 2: production A -> Y1 Y2 ... Yk
                    for i, Y in enumerate(body):
                        if Y in self.T or Y not in self.N:
                            # (a) If Y is terminal, add it directly to FIRST(A)
                            if Y not in first_dict[A]:
                                first_dict[A].add(Y)
                                changed = True
                            break  # stop propagation, terminals block further checks
                        else:
                            # (c) If Y is non-terminal, add FIRST(Y) - {&} to FIRST(A)
                            before = len(first_dict[A])
                            first_dict[A] |= (first_dict.get(Y, set()) - {'&'})
                            if len(first_dict[A]) != before:
                                changed = True

                            # Stop propagation if Y does not derive &
                            if '&' not in first_dict.get(Y, set()):
                                break

                            # (iii) If all symbols derive &, add & to FIRST(A)
                            if i == len(body) - 1:
                                if '&' not in first_dict[A]:
                                    first_dict[A].add('&')
                                    changed = True

        return first_dict
    
    def follow(self) -> Dict[str, Set[str]]:
        """Compute FOLLOW sets for all non-terminals in the grammar."""
        
        # Initialize FOLLOW sets for all non-terminals
        follow_dict: Dict[str, Set[str]] = {A: set() for A in self.N}

        # The start symbol always contains the end-of-input marker
        follow_dict[self.S].add('$')

        # Precompute FIRST sets (used inside FOLLOW rules)
        first_dict = self.first()

        changed = True
        while changed:
            changed = False
            # For each production A -> alpha B beta
            for A, bodies in self.P.items():
                for body in bodies:
                    for i, B in enumerate(body):
                        if B in self.N:
                            # Look ahead for the sequence beta = body[i+1:]
                            beta = body[i + 1:]

                            if beta:
                                # Add FIRST(beta) - {&} to FOLLOW(B)
                                first_beta = set()
                                for symbol in beta:
                                    if symbol in self.T or symbol not in self.N:
                                        first_beta.add(symbol)
                                        break
                                    else:
                                        first_beta |= (first_dict[symbol] - {'&'})
                                        if '&' not in first_dict[symbol]:
                                            break
                                before = len(follow_dict[B])
                                follow_dict[B] |= (first_beta - {'&'})
                                if len(follow_dict[B]) != before:
                                    changed = True

                                # If beta ->* &, add FOLLOW(A) to FOLLOW(B)
                                if all('&' in first_dict.get(sym, set()) for sym in beta):
                                    before = len(follow_dict[B])
                                    follow_dict[B] |= follow_dict[A]
                                    if len(follow_dict[B]) != before:
                                        changed = True
                            else:
                                # If B is at the end (no beta), add FOLLOW(A) to FOLLOW(B)
                                before = len(follow_dict[B])
                                follow_dict[B] |= follow_dict[A]
                                if len(follow_dict[B]) != before:
                                    changed = True

        return follow_dict


    def simplify_grammar(self) -> None:
        """Simplifies the grammar by removing, in order:
        - Unproductive symbols
        - Unreachable symbols
        - &-productions
        """

        self.remove_unproductive_symbols()
        self.remove_unreachable_symbols()
        self.remove_e_productions()
        
    def remove_unproductive_symbols(self) -> None:
        """Removes unproductive symbols from CFG"""
        # SP := T ∪ {&}
        SP = self.T.copy()
        SP.add('&')

        changed = True
        while changed:
            changed = False
            for X in self.N:
                if X not in SP:
                    for production in self.P[X]:
                        if all(symbol in SP for symbol in production):
                            SP.add(X)
                            changed = True

        # Only productive non-terminals
        self.N = self.N.intersection(SP)

        # If S is a productive symbol
        if self.S in SP:
            new_P = {}
            for X in self.N:
                valid_productions = [
                    prod for prod in self.P[X] if all(sym in SP for sym in prod)
                ]
                if valid_productions:
                    new_P[X] = valid_productions
            self.P = new_P
        else:
            self.P = None
    
    def remove_unreachable_symbols(self) -> None:
        """Removes unreachable symbols from the context-free grammar (CFG)."""
        
        # Initialize the set of reachable symbols with the start symbol
        SA = {self.S}
        changed = True

        # Iteratively find all reachable symbols
        while changed:
            changed = False
            for A, productions in self.P.items():
                # If the left-hand side is reachable,
                # all symbols in its productions become reachable too
                if A in SA:
                    for production in productions:
                        for symbol in production:
                            if symbol not in SA:
                                SA.add(symbol)
                                changed = True

        # Keep only nonterminals and terminals that are reachable
        self.N = self.N.intersection(SA)
        self.T = self.T.intersection(SA)

        # Keep only productions whose left-hand side and all right-hand symbols are reachable
        new_P = {}
        for A in self.N:
            valid_prods = [
                p for p in self.P.get(A, [])
                if all(sym in SA for sym in p)
            ]
            if valid_prods:
                new_P[A] = valid_prods

        # Update the grammar with the filtered set of productions
        self.P = new_P
    

    def remove_e_productions(self) -> None:
        """Removes &-productions from the CFG."""

        # Identify the set E of &-nonterminals
        E = self._identify_e_productions()

        # Initialize P' with all non-& productions
        new_P = {
            A: [p for p in prods if p != ['&'] and p != '&']
            for A, prods in self.P.items()
        }

        # Closure — repeatedly add new productions A ::= alphabeta
        # where a production A ::= alphaBbeta exists and B ∈ E
        changed = True
        while changed:
            changed = False
            for A, productions in list(new_P.items()):
                to_add = []
                for prod in productions:
                    # Generate new productions by removing occurrences of &-nonterminals
                    for i, symbol in enumerate(prod):
                        if symbol in E:
                            new_prod = prod[:i] + prod[i+1:]
                            if new_prod and new_prod not in productions and new_prod not in to_add:
                                to_add.append(new_prod)
                if to_add:
                    new_P[A].extend(to_add)
                    changed = True

        # Handle the start symbol if it can produce &
        if self.S in E:
            # Use helper to generate new name <S'>
            S_prime = self._make_nt(self.S, "'")
            new_P[S_prime] = [[self.S], ['&']]
            self.N.add(S_prime)
            self.S = S_prime

        # Update grammar
        self.P = new_P

    def _identify_e_productions(self) -> set[str]:
        """Identifies the set of &-nonterminals (E)."""

        # E initially contains & itself
        E = {'&'}
        
        changed = True
        while changed:
            changed = False
            Q = set()

            # For each nonterminal, check if it can derive &
            for X in self.N:
                if X not in E:
                    for production in self.P.get(X, []):
                        # A nonterminal is &-productive if all symbols
                        # in at least one of its productions are in E
                        if all(symbol in E for symbol in production):
                            Q.add(X)
                            break

            # If new &-nonterminals were found, update E
            if Q:
                E.update(Q)
                changed = True

        return E
    
    def remove_unitary_productions(self) -> None:

        NA = {A: {A} for A in self.N}

        changed = True
        while changed:
            changed = False
            for A in self.N:
                for production in self.P.get(A, []):
                    # If it's a unit production A ::= B (production is a single non-terminal)
                    if len(production) == 1 and production[0] in self.N:
                        B = production[0]
                        old_size = len(NA[A])
                        NA[A].add(B)
                        # Add all B's reachable non-terminals (transitive closure)
                        NA[A].update(NA[B])
                        if len(NA[A]) > old_size:
                            changed = True

        # Build the new set of productions P'
        new_P = {A: [] for A in self.N}

        for A in self.N:
            for B in NA[A]:
                for rhs in self.P.get(B, []):
                    # Skip unitary productions (B ::= C)
                    if not (len(rhs) == 1 and rhs[0] in self.N):
                        new_P[A].append(rhs)

        self.P = new_P
    
    def factorize_grammar(self) -> None:
        """Factorizes the CFG to remove common prefixes (left-factoring)
        and reduce direct and indirect non-determinism.
        """
        
        # Helper function: find the longest common prefix of a list of productions
        def longest_common_prefix(productions: list[list[str]]) -> list[str]:
            if not productions:
                return []
            # Start with the first production as reference
            prefix = productions[0].copy()
            for prod in productions[1:]:
                # Compare prefix with each production
                i = 0
                while i < len(prefix) and i < len(prod) and prefix[i] == prod[i]:
                    i += 1
                prefix = prefix[:i]  # shrink prefix
                if not prefix:
                    break
            return prefix

        # Make a copy of the current productions
        new_P = {A: [p.copy() for p in prods] for A, prods in self.P.items()}

        changed = True
        next_nonterminal_index = 1  # for generating new auxiliary symbols
        
        while changed:
            changed = False
            updated_P = {}

            for A, productions in new_P.items():
                if len(productions) <= 1:
                    # No need to factor
                    updated_P[A] = productions
                    continue

                # Group productions by their first symbol
                groups = {}
                for prod in productions:
                    if not prod:
                        key = ''
                    else:
                        key = prod[0]
                    groups.setdefault(key, []).append(prod)

                factorized = False
                for key, group in groups.items():
                    if len(group) > 1:
                        # More than one production shares the same prefix: factor it
                        prefix = longest_common_prefix(group)
                        if prefix:
                            # Create a new auxiliary non-terminal
                            while True:
                                # Generate name like <S'1>
                                A_prime = self._make_nt(A, f"'{next_nonterminal_index}")
                                next_nonterminal_index += 1
                                if A_prime not in self.N:
                                    break
                            self.N.add(A_prime)

                            # Remove prefix from original productions
                            new_group = [prod[len(prefix):] if len(prod) > len(prefix) else ['&'] for prod in group]

                            # Update productions for A
                            updated_P.setdefault(A, [])
                            updated_P[A].append(prefix + [A_prime])

                            # Add new productions for A_prime
                            updated_P[A_prime] = new_group

                            factorized = True
                            changed = True
                            break  # restart loop after factoring

                if not factorized:
                    # No factorization done for this non-terminal
                    updated_P.setdefault(A, []).extend(productions)

            new_P = updated_P

        self.P = new_P
    
    def remove_left_side_recursion(self) -> None:
        """Removes direct and indirect left recursion from the CFG"""

        # List of non-terminals in some order
        non_terminals = list(self.N)
        
        # Eliminate indirect recursion
        # For each non-terminal Ai
        for i, Ai in enumerate(non_terminals):
            for j in range(i):
                Aj = non_terminals[j]
                new_productions = []
                for prod in self.P.get(Ai, []):
                    # If production starts with Aj, replace Aj with its productions
                    if prod and len(prod) > 0 and prod[0] == Aj:
                        # Remove Ai ::= Aj γ
                        for beta in self.P.get(Aj, []):
                            new_prod = beta + prod[1:]  # replace Aj by beta
                            new_productions.append(new_prod)
                    else:
                        new_productions.append(prod)
                self.P[Ai] = new_productions

        # Remove direct left recursion for each Ai
        for Ai in non_terminals:
            alpha_list = []  # productions of the form Ai ::= Ai alpha
            beta_list = []   # productions of the form Ai ::= beta (not starting with Ai)
            
            for prod in self.P.get(Ai, []):
                if prod and len(prod) > 0 and prod[0] == Ai:
                    # Direct recursion detected
                    alpha_list.append(prod[1:])  # remove the leading Ai
                else:
                    beta_list.append(prod)
            
            if alpha_list:
                # Direct left recursion exists, need a new non-terminal
                # Generate name like <S'>
                Ai_prime = self._make_nt(Ai, "'")
                while Ai_prime in self.N:
                     Ai_prime = self._make_nt(Ai_prime, "'")

                self.N.add(Ai_prime)
                
                # Update Ai productions: Ai ::= beta Ai'
                self.P[Ai] = [beta + [Ai_prime] for beta in beta_list]

                # Update Ai' productions: Ai' ::= alpha Ai' | &
                self.P[Ai_prime] = [alpha + [Ai_prime] for alpha in alpha_list]
                self.P[Ai_prime].append(['&'])

    def _make_nt(self, base: str, suffix: str) -> str:
        """Helper to create new non-terminal name maintaining < > format."""
        
        if base.startswith('<') and base.endswith('>'):
            content = base[1:-1]
            return f"<{content}{suffix}>"
        return f"<{base}{suffix}>"
