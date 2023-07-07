library IEEE;
use IEEE.Std_Logic_1164.all;

entity silly is
port (A: in std_logic_vector(7 downto 0);
      Y: out std_logic_vector(7 downto 0) 
  );
end silly;

architecture myarch of silly is
  signal AUX: std_logic_vector(3 downto 0);
begin 
  Y <= A(7 downto 4) & AUX;
  AUX <= not A(3 downto 0);
end myarch;