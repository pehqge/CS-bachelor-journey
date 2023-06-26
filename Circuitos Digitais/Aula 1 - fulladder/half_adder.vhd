library IEEE;
use IEEE.Std_Logic_1164.all;

entity half_adder is
port (A, B, C, D: in std_logic;
      W, X, Y, Z: out std_logic );
end half_adder;

architecture mapas of half_adder is
begin 
  W <= (not(A) and C) or (not(A) and B) or (C and not(D)) or (A and not(B) and not(C));
  X <= (not(A) and B and D) or (B and C) or (A and not(D)) or (A and not(B));
  Y <= (not(A) and not(B) and C and D) or (B and C and not(D)) or (A and B and not(D)) or (A and not(B) and not(C) and D);
  Z <= (not(A) and not(B) and not(C)) or (not(A) and not(B) and not(D));
end mapas;
