library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity subtrator is
	generic (N : integer);
	port (
		A, B : in std_logic_vector(N - 1 downto 0);
		S : out std_logic_vector(N - 1 downto 0));
end subtrator;

architecture arch of subtrator is

	signal temp : std_logic_vector(N - 1 downto 0);

begin
	process (temp)
	begin
		if A > B then
			temp <= A - B;
		else
			temp <= B - A;
		end if;
	end process;
	S <= temp;
end arch;