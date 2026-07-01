library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ROM2a is
port(
	  address: in std_logic_vector(3 downto 0);
	  output : out std_logic_vector(14 downto 0)
);
end ROM2a;

architecture arc_ROM2a of ROM2a is
begin

--         switches 0 a 14
--         EDCBA9876543210                 round
output <=   "010010000011001" when address = "0000" else
            "000000010101101" when address = "0001" else
            "001000101010010" when address = "0010" else
            "100000100001110" when address = "0011" else
            "100010100010001" when address = "0100" else
            "000101100010010" when address = "0101" else
            "111000100100000" when address = "0110" else
            "110001010010000" when address = "0111" else
            "001100001001001" when address = "1000" else
            "000010010101100" when address = "1001" else
            "101010110000000" when address = "1010" else
            "000100000001111" when address = "1011" else
            "010000000001111" when address = "1100" else
            "001001000011100" when address = "1101" else
            "000000011011100" when address = "1110" else
            "000001011010001";
			 
end arc_ROM2a;