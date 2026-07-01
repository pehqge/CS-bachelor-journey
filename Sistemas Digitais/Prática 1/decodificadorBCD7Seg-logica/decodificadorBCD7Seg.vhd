LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY decodificadorBCD7Seg IS
	PORT (
		bcd : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		abcdefg : OUT std_logic_vector(6 DOWNTO 0)
	);
END decodificadorBCD7Seg;

ARCHITECTURE arch OF decodificadorBCD7Seg IS
BEGIN
	abcdefg(6) <= NOT bcd(3) AND NOT bcd(1) AND (bcd(2) XOR bcd(0));
	abcdefg(5) <= bcd(2) AND (bcd(1) XOR bcd(0));
	abcdefg(4) <= NOT bcd(2) AND bcd(1) AND NOT bcd(0);
	abcdefg(3) <= (NOT bcd(3) AND NOT bcd(2) AND NOT bcd(1) AND bcd(0)) OR (bcd(2) AND ((NOT bcd(1) AND NOT bcd(0)) OR (bcd(1) AND bcd(0))));
	abcdefg(2) <= (bcd(2) AND NOT bcd(1)) OR bcd(0);
	abcdefg(1) <= (bcd(1) AND bcd(0)) OR (NOT bcd(3) AND NOT bcd(2) AND (bcd(0) OR bcd(1)));
	abcdefg(0) <= (NOT bcd(3) AND NOT bcd(2) AND NOT bcd(1)) OR (bcd(2) AND bcd(1) AND bcd(0));

END ARCHITECTURE;
