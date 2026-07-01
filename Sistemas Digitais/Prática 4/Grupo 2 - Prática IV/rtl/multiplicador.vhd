library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity multiplicador is
    generic (N : integer);
    port (
        A, B : in std_logic_vector(N - 1 downto 0);
        S : out std_logic_vector(N*2 - 1 downto 0));
end multiplicador;

architecture arch of multiplicador is

begin
    S <= A * B;
end arch;