ibrary IEEE;
use IEEE.Std_Logic_1164.all;

entity fulladder is
port (A, B, C: in std_logic;
      S, CO: out std_logic );
end fulladder;

architecture soma of fulladder is
    signal D, E, F: std_logic;
begin
  D <= A xor B;
  E <= D and C;
  F <= A and B;
  S <= D xor C;
  CO <= E or F;
end soma;