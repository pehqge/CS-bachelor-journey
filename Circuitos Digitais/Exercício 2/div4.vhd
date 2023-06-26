library IEEE;
use IEEE.Std_Logic_1164.all;
use IEEE.std_logic_arith.all; 
use IEEE.std_logic_unsigned.all;

entity div4 is
port (A:  in std_logic_vector(7 downto 0);
      S:  out std_logic_vector(7 downto 0)
     );
end div4;

architecture mydiv4 of div4 is
begin
    S <= "00" & A(7 downto 2);
end mydiv4;