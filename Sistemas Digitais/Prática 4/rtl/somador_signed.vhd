library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;

entity somador_signed is
    generic (N : integer);
    port (
        A, B : in signed(N - 1 downto 0);
        S : out std_logic_vector(N - 1 downto 0));
end somador_signed;

architecture arch of somador_signed is

signal intermediario : signed(N - 1 downto 0);

begin
    intermediario <= A + B;
    S <= STD_LOGIC_VECTOR(intermediario);
	 
end arch;