library ieee;
use ieee.std_logic_1164.all;

entity testbench is
end testbench;

architecture tb of testbench is
    signal x,y,z: std_logic;
    signal RST : std_logic;
    signal meuclock: std_logic := '0';

    
    component tarefa1 is port (
       clock: in std_logic;
       reset: in std_logic;
       x,y, z: out std_logic );
    end component;

begin
    DUT : tarefa1 port map (x => x, y => y, z => z, reset => RST, clock => meuclock);
    meuclock <= not meuclock after 5 ns;
    RST <= '0', '1' after 30 ns, '0' after 60 ns;
end tb;

