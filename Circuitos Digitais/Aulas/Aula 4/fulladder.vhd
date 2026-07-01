library IEEE;
use IEEE.Std_Logic_1164.all;

entity fulladder is
    port (A: in std_logic;
          B: in std_logic;
          Cin: in std_logic;
          S: out std_logic;
          Cout: out std_logic
          );
end fulladder;

architecture behavior of fulladder is
    signal S1, C1, C2: std_logic;
begin
    -- Primeiro half adder
    S1 <= A xor B;
    C1 <= A and B;
    
    -- Segundo half adder
    S <= S1 xor Cin;
    C2 <= S1 and Cin;
    
    -- OR gate para combinar os carry
    Cout <= C1 or C2;
end behavior;
