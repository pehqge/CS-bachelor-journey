library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity somadorover is
    generic (N : integer);
    port (
        A, B : in std_logic_vector(N - 1 downto 0);
        S : out std_logic_vector(N downto 0));
end somadorover;

architecture arch of somadorover is

begin
    S <= ('0' & A) + ('0' & B);
end arch;