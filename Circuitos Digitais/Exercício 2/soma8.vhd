library IEEE;
use IEEE.Std_Logic_1164.all;
use IEEE.std_logic_arith.all; 
use IEEE.std_logic_unsigned.all;

entity soma8 is
port (A:  in std_logic_vector(7 downto 0);
      B:  in std_logic_vector(7 downto 0);
      S:  out std_logic_vector(7 downto 0)
     );
end soma8;

architecture mysoma8 of soma8 is
begin
    S <= A + B;
end mysoma8;