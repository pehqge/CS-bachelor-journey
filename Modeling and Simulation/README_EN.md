[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5425 - Modeling and Simulation

**Authors:** Pedro Henrique Gimenez and João Vitor Curcio Sutter
**Semester:** 7th · 2026.1

The course's final project (DCS, *Desenvolvimento de Componente de Simulação*) was to extend **GenESyS**, professor Cancian's discrete-event simulator, with a component for **universal cellular automata with a user-defined local rule** (theme 6.2).

The deliverable is a pull request against the official GenESyS repository, which has since been merged. The branch we worked on comes in here as a submodule, so what is pinned below is exactly the code we delivered.

| Resource | What it is |
|---|---|
| [Genesys-Simulator-cellular-automata/](./Genesys-Simulator-cellular-automata) | Submodule pinned to the fork's `tema6-2026-1` branch, our delivery branch. |
| [#453](https://github.com/rlcancian/Genesys-Simulator/issues/453) | The pull request against `rlcancian:2026-1`, merged on 2026-07-10. |
| [apresentacao.pdf](./apresentacao.pdf) | Final presentation slides (in Portuguese). |

## The component

The component models a cellular automaton as a GenESyS simulation element: a lattice of stateful cells, a neighborhood, and a local rule that decides each cell's next state from its neighbors.

The "universal" part is being able to configure each of those pieces instead of hardcoding them: Moore or von Neumann neighborhoods, fixed, reflexive, periodic or adiabatic boundaries, bit, integer or real state sets, and synchronous, sequential, random or block update policies. That lets the same component reproduce anything from Wolfram's elementary rules (30, 90, 110) to the Game of Life.

The **user-defined local rule** is my part: instead of picking a built-in rule, the user writes the body of the function in C++ through the simulator's interface, and the component compiles that code at runtime (through the `CppCompiler` that already existed in GenESyS), loads the resulting library and calls the function on every step. The contract is `nextState(self, neighbors, numNeighbors)`, plus an extended variant that also receives the cell's position, for rules that depend on where the cell is. User code goes through a size check and a blocklist before reaching the compiler, and model persistence saves and reloads the rule along with the rest of the configuration.

The component ships **50 gtest tests**, verified on Linux, covering the elementary rules against the textbook results, the Game of Life, all four boundary types, the update policies, the user-defined rule and persistence.
