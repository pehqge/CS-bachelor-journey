library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ROM1 is
port(
	  address: in std_logic_vector(3 downto 0);
	  output : out std_logic_vector(31 downto 0)
);
end ROM1;

architecture arc_ROM1 of ROM1 is
begin

--         HEX7      HEX6     HEX5     HEX4     HEX3     HEX2     HEX1     HEX0               round

output <=   "0111" & "1111" & "1111" & "0011" & "0010" & "1111" & "0101" & "1111" when address = "0000" else
            --7      des      des      3      2      des      5      des
            
            "1011" & "1010" & "1111" & "1111" & "1111" & "0011" & "1000" & "1111" when address = "0001" else
            --B      A      des      des      des      3      8      des
            
            "0011" & "0101" & "0010" & "1111" & "1101" & "1111" & "1111" & "1111" when address = "0010" else
            --3      5      2      des      D      des      des      des
            
            "0110" & "1111" & "0011" & "1011" & "1111" & "1111" & "1100" & "1111" when address = "0011" else
            --6      des      3      B      des      des      C      des
            
            "0001" & "1111" & "1111" & "0011" & "1111" & "1111" & "1110" & "1101" when address = "0100" else
            --1      des      des      3      des      des      E      D
            
            "1111" & "1011" & "1100" & "1111" & "0110" & "1111" & "0011" & "1111" when address = "0101" else
            --des      B      C      des      6      des      3      des
            
            "1101" & "1001" & "1111" & "0101" & "1111" & "0010" & "1111" & "1111" when address = "0110" else
            --D      9      des      5      des      2      des      des
            
            "0110" & "1111" & "1001" & "1010" & "1111" & "0100" & "1111" & "1111" when address = "0111" else
            --6      des      9      A      des      4      des      des
            
            "1111" & "1111" & "0111" & "0000" & "1111" & "1111" & "0001" & "0011" when address = "1000" else
            --des      des      7      0      des      des      1      3
            
            "1111" & "1000" & "1111" & "1111" & "1010" & "1101" & "0111" & "1111" when address = "1001" else
            --des      8      des      des      A      D      7      des
            
            "1111" & "1000" & "1111" & "1100" & "1111" & "1111" & "1010" & "0011" when address = "1010" else
            --des      8      des      C      des      des      A      3
            
            "0001" & "1000" & "1111" & "1111" & "1011" & "1111" & "1111" & "0111" when address = "1011" else
            --1      8      des      des      B      des      des      7
            
            "0001" & "1111" & "1111" & "1101" & "0100" & "1111" & "1100" & "1111" when address = "1100" else
            --1      des      des      D      4      des      C      des
            
            "0100" & "1011" & "1111" & "1111" & "0110" & "1111" & "1111" & "1010" when address = "1101" else
            --4      B      des      des      6      des      des      A
            
            "1111" & "1111" & "1111" & "1100" & "1000" & "1011" & "0101" & "1111" when address = "1110" else
            --des      des      des      C      8      B      5      des
            
            "1111" & "1111" & "0101" & "1111" & "0110" & "1010" & "1111" & "1011";
            --des      des      5      des      6      A      des      B
			 
end arc_ROM1;


