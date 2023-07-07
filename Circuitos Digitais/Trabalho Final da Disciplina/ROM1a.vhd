library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ROM1a is
port(
	  address: in std_logic_vector(3 downto 0);
	  output : out std_logic_vector(14 downto 0)
);
end ROM1a;

architecture arc_ROM1a of ROM1a is
begin

--         switches 0 a 14
--         EDCBA9876543210                 round
output <=   "000000010101100" when address = "0000" else
            "000110100001000" when address = "0001" else
            "010000000101100" when address = "0010" else
            "001100001001000" when address = "0011" else
            "110000000001010" when address = "0100" else
            "001100001001000" when address = "0101" else
            "010001000100100" when address = "0110" else
            "000011001010000" when address = "0111" else
            "000000010001011" when address = "1000" else
            "010010110000000" when address = "1001" else
            "001010100001000" when address = "1010" else
            "000100110000010" when address = "1011" else
            "011000000010010" when address = "1100" else
            "000110001010000" when address = "1101" else
            "001100100100000" when address = "1110" else
            "000110001100000";
			 
end arc_ROM1a;