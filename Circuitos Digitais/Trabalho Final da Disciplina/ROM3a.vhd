library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ROM3a is
port(
	  address: in std_logic_vector(3 downto 0);
	  output : out std_logic_vector(14 downto 0)
);
end ROM3a;

architecture arc_ROM3a of ROM3a is
begin

--         switches 0 a 14
--         EDCBA9876543210                 round
output <=   "001001110000011" when address = "0000" else
            "101000110011000" when address = "0001" else
            "001101100000101" when address = "0010" else
            "000000111110100" when address = "0011" else
            "000111100001010" when address = "0100" else
            "011011000110000" when address = "0101" else
            "010100011000110" when address = "0110" else
            "011000001101001" when address = "0111" else
            "000111010000110" when address = "1000" else
            "010000011100011" when address = "1001" else
            "011001010001001" when address = "1010" else
            "100110100100100" when address = "1011" else
            "000100111000101" when address = "1100" else
            "000011011101000" when address = "1101" else
            "110100110000001" when address = "1110" else
            "010100111001000";
			 
end arc_ROM3a;