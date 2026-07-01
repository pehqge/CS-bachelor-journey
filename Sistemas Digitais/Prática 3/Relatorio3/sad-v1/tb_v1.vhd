library IEEE;
use IEEE.std_logic_1164.all;
use ieee.math_real.all;
use ieee.numeric_std.all;
 
entity tb_v1 is
end tb_v1;

architecture tb of tb_v1 is

signal pA, pB: std_logic_vector(7 DOWNTO 0);
signal SAD: std_logic_vector(13 downto 0);
signal end_mem: std_logic_vector(5 downto 0);
signal pronto,ler: std_logic;
signal reset, iniciar, ck, finished: std_logic := '0';




CONSTANT period : TIME := 10 ns;

begin

 -- Connect DUV
 DUV: entity work.topo
 port map (
    ck => ck,
    iniciar => iniciar,
    reset => reset,
    pA => pA,
    pB => pB,
    end_mem => end_mem,
    pronto => pronto,
    ler => ler,
    SAD => SAD
    
  );


 ck <= not ck after period/2 when finished /= '1' else '0';

 process
  begin

    --- caso de teste 1

    iniciar <= '0', '1' after 10ns;
	 wait for 3*period;
    pA <= std_logic_vector(to_unsigned(1, pA'length));
    pB <= std_logic_vector(to_unsigned(2, pB'length));
    wait for 3*period;
    pA <= std_logic_vector(to_unsigned(170, pA'length));
    pB <= std_logic_vector(to_unsigned(170, pB'length));
    wait for 3*period;
    pA <= std_logic_vector(to_unsigned(40, pA'length));
    pB <= std_logic_vector(to_unsigned(60, pB'length));
    wait for 3*period;
    pA <= std_logic_vector(to_unsigned(255, pA'length));
    pB <= std_logic_vector(to_unsigned(252, pB'length));
    wait for 3*period;
    pA <= std_logic_vector(to_unsigned(0, pA'length));
    pB <= std_logic_vector(to_unsigned(0, pB'length));
    wait for 183*period;
    assert(SAD="00000000011000")
    report "Fail soma 1" severity error;
 
    --- caso teste 2
	 iniciar <= '0', '1' after 10ns;
    pA <= std_logic_vector(to_unsigned(255, pA'length));
    pB <= std_logic_vector(to_unsigned(254, pB'length));
    wait for 196*period;
    assert(SAD="00000001000000")
    report "Fail soma 2" severity error;
	 
	 wait for 10ns;
	 assert false report "Test done." severity note;
	 wait;

  end process;
end tb;
