LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY decodificadorBCD7Seg IS
 PORT (
   bcd : IN std_logic_vector(3 DOWNTO 0);
   abcdefg : OUT std_logic_vector(6 DOWNTO 0)
 );
END decodificadorBCD7Seg;

ARCHITECTURE arch OF decodificadorBCD7Seg IS
BEGIN
  PROCESS (bcd)
  BEGIN
    CASE bcd IS
      WHEN "0000" => abcdefg <= "0000001"; -- 0
      WHEN "0001" => abcdefg <= "1001111"; -- 1
      WHEN "0010" => abcdefg <= "0010010"; -- 2
      WHEN "0011" => abcdefg <= "0000110"; -- 3
      WHEN "0100" => abcdefg <= "1001100"; -- 4
      WHEN "0101" => abcdefg <= "0100000"; -- 5
      WHEN "0110" => abcdefg <= "0100000"; -- 6
      WHEN "0111" => abcdefg <= "0001111"; -- 7
      WHEN "1000" => abcdefg <= "0000000"; -- 8
      WHEN OTHERS => abcdefg <= "0000100"; -- 9
    END CASE;
  END PROCESS;
END ARCHITECTURE arch;
