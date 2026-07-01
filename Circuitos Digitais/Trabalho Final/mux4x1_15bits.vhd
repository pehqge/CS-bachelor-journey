library IEEE;
use IEEE.Std_Logic_1164.all;

entity mux4x1_15bits is
port (E0,E1,E2,E3: in std_logic_vector(14 downto 0);
      sel:  in std_logic_vector(1 downto 0);
      saida:  out std_logic_vector(14 downto 0) );
end mux4x1_15bits;

architecture mux of mux4x1_15bits is
begin 
  with sel select 
      saida <= E0 when "00", 
           E1 when "01",
           E2 when "10",
           E3 when others;
end mux;
