library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ROM2 is
port(
	  address: in std_logic_vector(3 downto 0);
	  output : out std_logic_vector(31 downto 0)
);
end ROM2;

architecture arc_ROM2 of ROM2 is
begin

--          HEX7      HEX6     HEX5     HEX4     HEX3     HEX2     HEX1     HEX0               round

output <=   "0011" & "0000" & "1111" & "1111" & "0100" & "1111" & "1101" & "1010" when address = "0000" else
            --3      0      des      des      4      des      D      A

            "1111" & "0101" & "1111" & "1111" & "0000" & "0010" & "0111" & "0011" when address = "0001" else
            --des      5      des      des      0      2      7      3
            
            "1111" & "1111" & "1000" & "1100" & "0110" & "0100" & "0001" & "1111" when address = "0010" else
            --des      des      8      C      6      4      1      des
            
            "1110" & "1111" & "1111" & "0011" & "1000" & "0010" & "1111" & "0001" when address = "0011" else
            --E      des      des      3      8      2      des      1
            
            "1111" & "1111" & "0100" & "1110" & "1111" & "0000" & "1000" & "1010" when address = "0100" else
            --des      des      4      E      des      0      8      A
            
            "0100" & "1111" & "1001" & "0001" & "1111" & "1111" & "1011" & "1000" when address = "0101" else
            --4      des      9      1      des      des      B      8
            
            "1110" & "1111" & "1100" & "0101" & "1111" & "1101" & "1111" & "1000" when address = "0110" else
            --E      des      C      5      des      D      des      8
            
            "1111" & "0111" & "1101" & "1111" & "1110" & "1001" & "0100" & "1111" when address = "0111" else
            --des      7      D      des      E      9      4      des
            
            "0000" & "1111" & "0110" & "1011" & "1111" & "1100" & "1111" & "0011" when address = "1000" else
            --0      des      6      B      des      C      des      3
            
            "0111" & "0011" & "0010" & "0101" & "1111" & "1010" & "1111" & "1111" when address = "1001" else
            --7      3      2      5      des      A      des      des
            
            "1110" & "1111" & "1000" & "0111" & "1100" & "1111" & "1010" & "1111" when address = "1010" else
            --E      des      8      7      C      des      A      des
            
            "1111" & "0001" & "1111" & "1011" & "1111" & "0011" & "0000" & "0010" when address = "1011" else
            --des      1      des      B      des      3      0      2
            
            "1111" & "0000" & "1101" & "0011" & "0001" & "0010" & "1111" & "1111" when address = "1100" else
            --des      0      D      3      1      2      des      des
            
            "0010" & "0011" & "1111" & "0100" & "1100" & "1111" & "1001" & "1111" when address = "1101" else
            --2      3      des      4      C      des      9      des
            
            "1111" & "0110" & "0111" & "0011" & "1111" & "0010" & "0100" & "1111" when address = "1110" else
            --des      6      7      3      des      2      4      des
            
            "1111" & "0110" & "0100" & "1111" & "0111" & "0000" & "1001" & "1111";
            --des      6      4      des      7      0      9      des
			 
end arc_ROM2;