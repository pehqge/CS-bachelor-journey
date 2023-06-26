library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ROM3 is
port(
	  address: in std_logic_vector(3 downto 0);
	  output : out std_logic_vector(31 downto 0)
);
end ROM3;

architecture arc_ROM3 of ROM3 is
begin

--         HEX7      HEX6     HEX5     HEX4     HEX3     HEX2     HEX1     HEX0               round

output <=   "1111" & "0000" & "1111" & "1100" & "0001" & "1000" & "1001" & "0111" when address = "0000" else
            --des      0      des      C      1      8      9      7
            
            "0011" & "1111" & "1111" & "0100" & "1110" & "1000" & "1100" & "0111" when address = "0001" else
            --3      des      des      4      E      8      C      7
            
            "1011" & "1100" & "1111" & "1001" & "1111" & "0010" & "1000" & "0000" when address = "0010" else
            --B      C      des      9      des      2      8      0
            
            "0111" & "0100" & "0101" & "1111" & "0010" & "0110" & "1000" & "1111" when address = "0011" else
            --7      4      5      des      2      6      8      des
            
            "0011" & "1001" & "1111" & "1011" & "1010" & "0001" & "1000" & "1111" when address = "0100" else
            --3      9      des      B      A      1      8      des
            
            "1111" & "1010" & "1111" & "1100" & "0101" & "1101" & "1001" & "0100" when address = "0101" else
            --des      A      des      C      5      D      9      4
            
            "0001" & "0110" & "1011" & "1111" & "0111" & "1101" & "1111" & "0010" when address = "0110" else
            --1      6      B      des      7      D      des      2
            
            "0011" & "1100" & "1111" & "1101" & "1111" & "0110" & "0101" & "0000" when address = "0111" else
            --3      C      des      D      des      6      5      0
            
            "0010" & "1001" & "1111" & "1010" & "1111" & "0001" & "0111" & "1011" when address = "1000" else
            --2      9      des      A      des      1      7      B
            
            "1111" & "1101" & "0000" & "0111" & "1111" & "0110" & "0001" & "0101" when address = "1001" else
            --des      D      0      7      des      6      1      5
            
            "0000" & "1101" & "0111" & "1111" & "1001" & "0011" & "1100" & "1111" when address = "1010" else
            --0      D      7      des      9      3      C      des
            
            "1111" & "1000" & "0101" & "1010" & "0010" & "1111" & "1011" & "1110" when address = "1011" else
            --des      8      5      A      2      des      B      E
            
            "1011" & "1111" & "0000" & "1000" & "0111" & "0010" & "1111" & "0110" when address = "1100" else
            --B      des      0      8      7      2      des      6
            
            "1010" & "0101" & "0110" & "1001" & "0111" & "0011" & "1111" & "1111" when address = "1101" else
            --A      5      6      9      7      3      des      des
            
            "1000" & "0111" & "1101" & "1111" & "1011" & "0000" & "1110" & "1111" when address = "1110" else
            --8      7      D      des      B      0      E      des
            
            "1011" & "1101" & "1111" & "0111" & "1000" & "0110" & "0011" & "1111";
            --B      D      des      7      8      6      3      des
			 
end arc_ROM3;