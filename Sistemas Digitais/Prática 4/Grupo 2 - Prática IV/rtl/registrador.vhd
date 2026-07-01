library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity registrador is
	generic (N : integer);
	port (
		clk, carga : in std_logic;
		d : in std_logic_vector(N - 1 downto 0);
		q : out std_logic_vector(N - 1 downto 0));
end registrador;

architecture arch of registrador is
begin
	process (clk)
	begin
		if (clk'EVENT and clk = '1' and carga = '1') then
			q <= d;
		end if;
	end process;
end arch;