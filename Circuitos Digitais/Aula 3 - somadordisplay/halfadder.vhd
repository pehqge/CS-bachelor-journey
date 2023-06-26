library IEEE;
use IEEE.Std_Logic_1164.all;

entity halfadder is
    port (A, B: in std_logic;
          S, Cout: out std_logic);
end halfadder;

architecture behavior of halfadder is
begin
  S <= A xor B;
  Cout <= A and B;
end behavior;
