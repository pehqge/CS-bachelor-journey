library IEEE;
use IEEE.Std_Logic_1164.all;

entity mux2 is
port (K:  in std_logic;
      KG: in std_logic_vector(11 downto 0);
      LBS: in std_logic_vector(11 downto 0);
      S:  out std_logic_vector(11 downto 0) );
end mux2;

architecture mux of mux2 is
begin 
  with K select 
      S <= KG when '0', 
           LBS when others;
end mux;
