library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ROM0 is
port(
	  address: in std_logic_vector(3 downto 0);
	  output : out std_logic_vector(31 downto 0)
);
end ROM0;

architecture arc_ROM0 of ROM0 is
begin

--         HEX7      HEX6     HEX5     HEX4     HEX3     HEX2     HEX1     HEX0               round

output <= "1111"	& "0110" & "1111" & "1111"	& "0001" & "1111" & "1101" & "1111" when address = "0000" else
--         des        6       des      des       1       des       D       des

          "0111"	& "1111" & "0100" & "1111"	& "1111" & "1010" & "1111" & "1111" when address = "0001" else
--          7        des       4       des      des       A       des       des

			 "1111"	& "1111" & "1111" & "1000"	& "1111" & "1111" & "1011" & "1100" when address = "0010" else
--         des       des      des       8       des      des       B        C

			 "1111"	& "1111" & "0111" & "1111"	& "0101" & "1111" & "1111" & "1110" when address = "0011" else
--         des       des       7       des       5       des      des       E

			 "1111"	& "1001" & "1000" & "1111"	& "1111" & "0001" & "1111" & "1111" when address = "0100" else
--         des        9       8        des      des       1       des      des

			 "0010"	& "1111" & "1111" & "1111"	& "1111" & "1110" & "1111" & "0000" when address = "0101" else
--          2        des      des      des      des       E       des       0

			 "1111"	& "0001" & "1111" & "1111"	& "1111" & "1111" & "0011" & "1100" when address = "0110" else
--         des        1       des      des      des      des       3        C			 
			 
			 "1100"	& "1111" & "1111" & "1010"	& "0011" & "1111" & "1111" & "1111" when address = "0111" else
--          C        des      des       A        3       des      des      des

			 "1111"	& "1001" & "1111" & "0110"	& "1111" & "1111" & "0010" & "1111" when address = "1000" else
--         des        9       des       6       des      des       2       des

			 "1111"	& "1111" & "1000" & "1111"	& "1111" & "0111" & "1111" & "1110" when address = "1001" else
--         des       des       8       des      des       7       des       E

			 "0001"	& "1111" & "1111" & "1011"	& "1111" & "1010" & "1111" & "1111" when address = "1010" else
--          1        des      des       B       des       A       des       des

			 "1111"	& "0011" & "1111" & "1111"	& "1011" & "1111" & "1100" & "1111" when address = "1011" else
--         des        3       des      des       B       des       C       des

			 "1111"	& "1000" & "1111" & "1101"	& "1111" & "0100" & "1111" & "1111" when address = "1100" else
--         des        8       des       D       des       4       des      des

			 "0101"	& "1111" & "1111" & "1111"	& "0000" & "1111" & "1111" & "0001" when address = "1101" else
--          5        des      des      des       0       des      des       1

			 "1111"	& "1111" & "0111" & "1111"	& "1111" & "1101" & "1110" & "1111" when address = "1110" else
--         des       des       7       des      des       D        E       des

			 "1111"	& "1011" & "1111" & "0100"	& "1111" & "1111" & "1111" & "0011";
--         des        B       des       4       des      des      des       3
			 
end arc_ROM0;