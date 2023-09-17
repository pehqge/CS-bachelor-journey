#força a entrada cin para 0 no tempo 0 ns
#força cin para 1 no tempo 80 ns, repete a cada 160
force /clk 0 0 ns, 1 50 ns -r 100 ns
force /rst 1 0 ns, 0 80 ns, 1 130 ns
force /carga 1 0 ns, 0 180 ns, 1 380 ns
force /D 0001 0 ns, 0101 20 ns, 0111 40 ns, 1011 60 ns

