from typing import Set, Dict, Tuple, List
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict
from graphviz import Digraph

@dataclass
class Automaton:

    states: Set[str] = field(default_factory=set)
    alphabet: Set[str] = field(default_factory=set)
    transitions: Dict[Tuple[str, str], str] = field(default_factory=dict) #delta(q, a)  -> p
    initial_state: str = None
    accept_states: set = field(default_factory=set)
    deterministic: bool = True

    # Validating automaton instance
    def __post_init__(self):
        if (
            not self.states
            and not self.alphabet
            and not self.transitions
            and not self.accept_states
            and not self.initial_state
        ):
            return

        if self.initial_state not in self.states:
            raise ValueError("Start state must be in states")
        if not self.accept_states.issubset(self.states):
            raise ValueError("Accept states must be a subset of states")
        for (state, symbol), next_state in self.transitions.items():
            if state not in self.states:
                raise ValueError(f"State {state} in transitions must be in states")
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol {symbol} in transitions must be in alphabet")
            if next_state not in self.states:
                raise ValueError(
                    f"Next state {next_state} in transitions must be in states"
                )

    # Automaton Operations

    def minimize(self) -> None:
        """Minimize the automata by removing unreachable, dead and equivalent states"""
        self.remove_unreachable_states()
        self.remove_dead_states()
        self.merge_equivalent_states()
    
    @staticmethod
    def union(automata: List["Automaton"]) -> "Automaton":
        """Union of Automata by &-transitions, returns an NDFA"""

        if len(automata) < 1:
            raise ValueError("You need at least one automaton for union.")
        
        if len(automata) == 1:
            return automata[0]
        
        new_automaton = Automaton()

        # Create new initial state
        new_initial_state = "q0_union"
        new_automaton.states.add(new_initial_state)
        new_automaton.initial_state = new_initial_state

        state_counter = 1

        # Combine states, alphabet, and accept states from ALL automata
        for i, automaton in enumerate(automata):
 
            state_mapping = {}
            for old_state in automaton.states:
                new_state = f"q{state_counter}_{i}"
                state_mapping[old_state] = new_state
                new_automaton.states.add(new_state)
                state_counter += 1
                
                if old_state in automaton.accept_states:
                    new_automaton.accept_states.add(new_state)
            
            for (old_from, symbol), old_to in automaton.transitions.items():
                new_from = state_mapping[old_from]
                
                if isinstance(old_to, set):
                    new_to = {state_mapping[s] for s in old_to}
                else:
                    new_to = state_mapping[old_to]
                    
                new_automaton.transitions[(new_from, symbol)] = new_to
            
            new_automaton.alphabet.update(automaton.alphabet)
            
            if (new_initial_state, "&") in new_automaton.transitions:
                existing_target = new_automaton.transitions[(new_initial_state, "&")]
                if isinstance(existing_target, set):
                    existing_target.add(state_mapping[automaton.initial_state])
                else:
                    new_automaton.transitions[(new_initial_state, "&")] = {existing_target, state_mapping[automaton.initial_state]}
            else:
                new_automaton.transitions[(new_initial_state, "&")] = state_mapping[automaton.initial_state]

        # Setting as non-deterministic
        new_automaton.deterministic = False

        return new_automaton
    
    def determinize(self) -> None:
        """Convert the automaton to a deterministic automaton (DFA)."""

        if self.deterministic:
            print("The automaton is already deterministic.")
            return

        e_closure = self.calculate_e_closure()

        # New states and transitions
        new_states = set()
        new_transitions = dict()
        new_accept_states = set()

        # Map from new state (set of old states) to its name
        state_name_map = {}
        
        initial_set = frozenset(e_closure[self.initial_state])
        state_name_map[initial_set] = "q0"
        new_states.add("q0")

        # Queue for processing new states
        queue = [initial_set]

        # Process each state in the queue
        while queue:
            current_set = queue.pop(0)
            current_name = state_name_map[current_set]

            for symbol in self.alphabet - {"&"}:
                next_set = set()
                
                for state in current_set:
                    next_state = self.transitions.get((state, symbol))
                    if next_state:
                        if isinstance(next_state, set):
                            for ns in next_state:
                                next_set.update(e_closure[ns])
                        else:
                            next_set.update(e_closure[next_state])

                if next_set:
                    next_set_frozen = frozenset(next_set)
                    if next_set_frozen not in state_name_map:
                        new_name = f"q{len(state_name_map)}"
                        state_name_map[next_set_frozen] = new_name
                        new_states.add(new_name)
                        queue.append(next_set_frozen)
                    else:
                        new_name = state_name_map[next_set_frozen]

                    new_transitions[(current_name, symbol)] = new_name

            if current_set & self.accept_states:
                new_accept_states.add(current_name)

        # Update automaton
        self.states = new_states
        self.transitions = new_transitions
        self.accept_states = new_accept_states
        self.initial_state = "q0"
        self.deterministic = True

    
    # Auxiliary Functions

    def calculate_e_closure(self) -> Dict[str, Set[str]]:
        """Returns e-closure for each state in the automaton as a dict"""

        if self.deterministic:
            raise ValueError(
                "&-closure is only applicable to non-deterministic automaton."
            )

        e_closure = {state: {state} for state in self.states}
        changed = True
        
        while changed:
            changed = False
            for (state, symbol), next_states in self.transitions.items():
                if symbol == "&":
                    for next_state in next_states:
                        if next_state not in e_closure[state]:
                            e_closure[state].add(next_state)
                            changed = True
                        for reachable in e_closure[next_state]:
                            if reachable not in e_closure[state]:
                                e_closure[state].add(reachable)
                                changed = True
        return e_closure

    def remove_unreachable_states(self) -> None:
        """Update states set with reachable states only."""

        # DFS
        reachable: Set[str] = set()
        stack = [self.initial_state]
        while stack:
            state = stack.pop()
            if state in reachable:
                continue
            reachable.add(state)
            for symbol in self.alphabet:
                nxt = self.transitions.get((state, symbol))
                if nxt is not None and nxt not in reachable:
                    stack.append(nxt)

        self.states = reachable
    
    def remove_dead_states(self) -> None:
        """Update states set to remove dead states"""

        not_dead: Set[str] = self.accept_states
        changed = True

        while changed:
            changed = False
            for (state, symbol), next_state in self.transitions.items():
                if next_state in not_dead and state not in not_dead:
                    not_dead.add(state)
                    changed = True

        self.states = self.states.intersection(not_dead)
    
    def merge_equivalent_states(self) -> None:
        """Merge equivalent states in the automaton."""

        if not self.deterministic:
            raise ValueError("State equivalence minimization is only applicable to deterministic automata.")

        # Initialize partition with final and non-final states
        partition = [self.accept_states, self.states - self.accept_states]
        new_partition = list()

        while True:
            for group in partition:
                # Split group into subgroups based on transitions
                subgroups = {}
                for state in group:
                    key = tuple(
                        next(
                            (i for i, g in enumerate(partition) if self.transitions.get((state, symbol)) in g),
                            None,
                        )
                        for symbol in self.alphabet
                    )
                    subgroups.setdefault(key, set()).add(state)
                new_partition.extend(subgroups.values())

            if new_partition == partition:
                break
            partition = new_partition
            new_partition = list()

        # Merge equivalent states
        state_mapping = dict()
        for group in partition:
            representative = next(iter(group))
            for state in group:
                state_mapping[state] = representative

        # Update automaton
        self.states = set(state_mapping.values())
        self.transitions = {
            (state_mapping[state], symbol): state_mapping[next_state]
            for (state, symbol), next_state in self.transitions.items()
            if state in state_mapping and next_state in state_mapping
        }
        self.initial_state = state_mapping[self.initial_state]
        self.accept_states = {state_mapping[state] for state in self.accept_states}


    # Save to File - Auxiliary
    def to_jflap_xml(self, file_name: str, directory_path: Path) -> None:
        """
        Converts the automaton to JFLAP XML format.
        """

        # Create the basic structure
        xml_structure = [
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
            "<!--Created with JFLAP 7.1.-->",
            "<structure>",
            "\t<type>fa</type>",
            "\t<automaton>",
        ]

        # Add states section
        xml_structure.append("\t\t<!--The list of states.-->")

        # Create state ID mapping
        state_to_id = {state: idx for idx, state in enumerate(self.states)}

        # Add each state
        for state in self.states:
            state_id = state_to_id[state]
            # Default coordinates (you might want to adjust these)
            x = 100 + (state_id * 100)
            y = 200

            xml_structure.append(f'\t\t<state id="{state_id}" name="{state}">')
            xml_structure.append(f"\t\t\t<x>{x}.0</x>")
            xml_structure.append(f"\t\t\t<y>{y}.0</y>")

            # Add initial/final markers
            if state == self.initial_state:
                xml_structure.append("\t\t\t<initial/>")
            if state in self.accept_states:
                xml_structure.append("\t\t\t<final/>")

            xml_structure.append("\t\t</state>")

        # Add transitions section
        xml_structure.append("\t\t<!--The list of transitions.-->")

        # Add each transition
        for (from_state, symbol), to_state in self.transitions.items():
            xml_structure.append("\t\t<transition>")
            xml_structure.append(f"\t\t\t<from>{state_to_id[from_state]}</from>")
            xml_structure.append(f"\t\t\t<to>{state_to_id[to_state]}</to>")
            xml_structure.append(f"\t\t\t<read>{symbol}</read>")
            xml_structure.append("\t\t</transition>")

        # Close tags
        xml_structure.append("\t</automaton>")
        xml_structure.append("</structure>")
        
        with open(directory_path / f"{file_name}.jff", 'w') as f:
            f.write("\n".join(xml_structure))
        
        print(f"Automaton saved to {directory_path / f'{file_name}.jff'}")

    def generate_diagram_image(self) -> bytes:
        """
        Generates a PNG image of the automaton diagram using graphviz.
        """
        if not self.states or not self.initial_state:
            raise ValueError("Autômato inválido")
        
        dot = Digraph("Automaton", format="png")
        dot.attr(dpi="300", rankdir="LR", bgcolor="transparent")
        dot.attr('graph', pad="0.5", nodesep="1.0", ranksep="2.0")
        
        # Node styling
        dot.attr('node', 
            shape='circle', 
            margin="0.1",
            fontname="Helvetica, Arial, sans-serif",
            fontsize="14",
            style="filled, rounded",
            fillcolor="#e1f5fe", 
            color="#455a64",   
            penwidth="1.5"
        )
        
        # Edge styling
        dot.attr('edge', 
            minlen="2.5",        
            fontname="Helvetica, Arial, sans-serif",
            fontsize="12",
            color="#37474f",     
            penwidth="1.2",
            arrowsize="0.8",
            decorate="true"
        )

        # Add states
        for state in sorted(self.states):
            is_final = state in self.accept_states
            dot.node(str(state), 
                shape="doublecircle" if is_final else "circle",
                fillcolor="#b3e5fc" if is_final else "#e1f5fe", 
                penwidth="2.0" if is_final else "1.5"
            )
            
        # Add initial state arrow
        dot.node("Start", shape="none", label="", width="0", height="0", style="invis")
        dot.edge("Start", str(self.initial_state), penwidth="1.5", color="#37474f")

        # Group transitions by source and destination
        groups = defaultdict(list)
        for (src, sym), dst in self.transitions.items():
            sym_display = "ε" if sym == "&" else sym
            dst_str = str(dst) if not isinstance(dst, str) else dst
            groups[(src, dst_str)].append(sym_display)
        
        # Escape special characters in labels
        escape = lambda s: {'"': '\\"', '\\': '\\\\', '|': '\\|', '{': '\\{', '}': '\\}'}.get(s, s)
        
        # Add edges with grouped symbols
        for (src, dst), syms in sorted(groups.items()):
            label_text = " | ".join(escape(s) for s in sorted(syms))
            dot.edge(str(src), dst, label=f" {label_text} ")
        
        return dot.pipe()