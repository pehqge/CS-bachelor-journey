LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
ENTITY reg4 IS 
	GENERIC (N : INTEGER :=4);
	PORT(
	clk, rst, carga: IN STD_LOGIC;
	D: IN STD_LOGIC_VECTOR (N-1 DOWNTO 0);
	Q: OUT STD_LOGIC_VECTOR(N-1 DOWNTO 0)
	);

END reg4;
ARCHITECTURE comportamento OF reg4 IS
BEGIN
	PROCESS (rst, clk)
	BEGIN
		IF (rst = '0') THEN
			Q <=(OTHERS => '0');
		ELSIF (rising_edge(clk)) THEN
			IF (carga= '1') THEN
				Q <= D;
			END IF;
		END IF;
	END PROCESS;
END comportamento;
			 