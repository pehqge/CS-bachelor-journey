[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5425 - Modeling and Simulation

**Authors:** Pedro Henrique Gimenez and João Vitor Curcio Sutter

The course's final project was to extend GenESyS, professor Cancian's discrete-event simulator, with a universal cellular automaton component. Universal because the neighborhood, boundary, state set and update policy are all configurable, which covers everything from Wolfram's elementary rules to the Game of Life; and because the user can write their own local rule in C++ through the simulator's interface, compiled and loaded at runtime. It ships 50 gtest tests, verified on Linux.

The deliverable was a pull request against the official GenESyS repository, since merged. The branch we worked on comes in here as a submodule, pinned at the delivery commit.

| Resource | What it is |
|---|---|
| [Genesys-Simulator-cellular-automata/](./Genesys-Simulator-cellular-automata) | The code, on the fork's `tema6-2026-1` branch. |
| [#453](https://github.com/rlcancian/Genesys-Simulator/issues/453) | The pull request against `rlcancian:2026-1`, merged on 2026-07-10. |
| [apresentacao.pdf](./apresentacao.pdf) | Final presentation slides. In Portuguese. |
