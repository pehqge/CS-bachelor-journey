LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY regD IS 
	GENERIC (N : INTEGER :=4);
	PORT(
	clk, sel: IN STD_LOGIC;
	D: IN STD_LOGIC_VECTOR (N-1 DOWNTO 0);
	Q: OUT STD_LOGIC_VECTOR(N-1 DOWNTO 0)
	);

END regD;
ARCHITECTURE comportamento OF regD IS
BEGIN
	PROCESS (clk)
	BEGIN
		IF (rising_edge(clk)) THEN
			IF (sel= '1') THEN
				Q <= '0' & D(N-1 DOWNTO 1);
			ELSE
				Q <= D;
			END IF;
		END IF;
	END PROCESS;
END comportamento;
			 