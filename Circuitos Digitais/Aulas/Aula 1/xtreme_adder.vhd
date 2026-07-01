library IEEE;
use IEEE.Std_Logic_1164.all;

entity xtreme_adder is
port (A0, A1, B0, B1: in std_logic;
      S0, S1, S2, S3: out std_logic );
end xtreme_adder;

architecture soma of xtreme_adder is
    signal C, D, E, F: std_logic;
begin
  C <= A0 and B0;
  D <= A1 xor B1;
  E <= D and C;
  F <= A1 and B1;
  S0 <= A0 xor B0;
  S1 <= D xor C;
  S2 <= E or F;
 end soma;
