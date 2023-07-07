library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ROM0a is
port(
	  address: in std_logic_vector(3 downto 0);
	  output : out std_logic_vector(14 downto 0)
);
end ROM0a;

architecture arc_ROM0a of ROM0a is
begin

--         switches 0 a 14
--         EDCBA9876543210                 round
output <= "010000001000010" when address = "0000" else --ROM0 possui os valores 6, 1 e D no round 0.
		    "000010010010000" when address = "0001" else
			 "001100100000000" when address = "0010" else
			 "100000010100000" when address = "0011" else
			 "000001100000010" when address = "0100" else
			 "100000000000101" when address = "0101" else
			 "001000000001010" when address = "0110" else
			 "001010000001000" when address = "0111" else
			 "000001001000100" when address = "1000" else
			 "100000110000000" when address = "1001" else
			 "000110000000010" when address = "1010" else
			 "001100000001000" when address = "1011" else
			 "010000100010000" when address = "1100" else
			 "000000000100011" when address = "1101" else
			 "110000010000000" when address = "1110" else
			 "000100000011000";
			 
end arc_ROM0a;