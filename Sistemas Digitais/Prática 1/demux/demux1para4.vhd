LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY demux1para4 IS
	PORT (
			f : IN std_logic;
			sel : IN std_logic_vector (1 DOWNTO 0);
			a, b, c, d : OUT std_logic
	);

END demux1para4;

ARCHITECTURE arch OF demux1para4 IS

--- implementar
BEGIN
PROCESS (f,sel) IS
BEGIN
 IF (sel ="00" and f = '1') THEN
 a <= '1';
 b <='0';
 c <= '0';
 d <= '0';
ELSIF(sel = "01" and f = '1') THEN
 a <= '0';
 b <='1';
 c <= '0';
 d <= '0';
ELSIF(sel ="10" and f = '1') THEN
 a <= '0';
 b <='0';
 c <= '1';
 d <= '0';
ELSIF(sel ="11" and f = '1') THEN
  a <= '0';
 b <='0';
 c <= '0';
 d <= '1';
ELSE
 a <= '0';
 b <='0';
 c <= '0';
 d <= '0';
END IF;
END PROCESS;
END arch;
