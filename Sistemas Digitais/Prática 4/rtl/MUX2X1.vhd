library ieee;
use ieee.std_logic_1164.all;

entity MUX2X1 is
    generic (N : integer);
    port (
        sel : in std_logic;
        ent0, ent1 : in std_logic_vector(N - 1 downto 0);
        output : out std_logic_vector(N - 1 downto 0)
    );
end MUX2X1;

architecture circuito of MUX2X1 is
begin
    output <= ent0 when sel = '0' else
        ent1;
end circuito;