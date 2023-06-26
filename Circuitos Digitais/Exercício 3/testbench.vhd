library ieee;
use ieee.std_logic_1164.all;

entity testbench is
end testbench;

architecture tb of testbench is
    signal min: std_logic;
    signal RST : std_logic;
    signal A, B : std_logic_vector(6 downto 0);
    signal meuclock: std_logic := '0';

    
    component trabalho is port ( 
      CLK, RST:  in std_logic;
      A, B:  out std_logic_vector(6 downto 0);
      min: out std_logic);
    end component;

begin
    DUT : trabalho port map (A => A, B => B, RST =>RST, CLK => meuclock, min => min );
    meuclock <= not meuclock after 10 ns;
    RST <= '1', '0' after 30 ns, '1' after 60 ns;
end tb;