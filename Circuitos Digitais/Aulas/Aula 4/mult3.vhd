library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_arith.all; 
use IEEE.std_logic_unsigned.all;


entity mult3 is
port (X:  in std_logic_vector(3 downto 0);
      Y:  out std_logic_vector(4 downto 0));
end mult3;

architecture m3 of mult3 is
    signal outsoma1: std_logic_vector(4 downto 0);
    component soma4 is
    port (A,B:  in std_logic_vector(3 downto 0);
          C:  out std_logic_vector(4 downto 0));
    end component;
begin 
  s41: soma4 port map(X,X,outsoma1);
  s42: soma4 port map(X,outsoma1(3 downto 0),Y);
end m3;
