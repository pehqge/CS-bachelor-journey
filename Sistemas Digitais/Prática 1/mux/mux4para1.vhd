LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY mux4para1 IS
	GENERIC (N : POSITIVE := 1);
	PORT (
			a, b, c, d : IN std_logic_vector (N-1 DOWNTO 0);
			sel : IN std_logic_vector (1 DOWNTO 0);
			y : OUT std_logic_vector (N - 1 DOWNTO 0)
	);
END mux4para1;

ARCHITECTURE arch OF mux4para1 IS
BEGIN
	y <=  a when sel = "00" else
			b when sel = "01" else
			c when sel = "10" else
			d;

END arch;
