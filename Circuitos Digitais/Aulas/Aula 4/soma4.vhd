library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_arith.all; 
use IEEE.std_logic_unsigned.all;


entity soma4 is
port (A,B:  in std_logic_vector(3 downto 0);
      C:  out std_logic_vector(4 downto 0));
end soma4;

architecture s4 of soma4 is
begin 
  C <= ("0" & A) + ("0" & B);
end s4;
