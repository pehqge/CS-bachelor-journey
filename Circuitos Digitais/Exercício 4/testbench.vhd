library ieee;
use ieee.std_logic_1164.all;

entity testbench is
end testbench;

architecture tb of testbench is
    signal s1, s2, b: std_logic;
    signal RST : std_logic;
    signal meuclock: std_logic := '0';

    
    component exercicio is port (
       clock, reset, b: in std_logic;
       s1, s2: out std_logic );
    end component;

begin
    DUT : exercicio port map (b => b, s1 => s1, s2 => s2, reset => RST, clock => meuclock);
    meuclock <= not meuclock after 5 ns;
    RST <= '0', '1' after 30 ns, '0' after 60 ns;
    b <= '0', '1' after 10 ns, '0' after 200 ns;
end tb;

