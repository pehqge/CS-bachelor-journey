library IEEE;
use IEEE.Std_Logic_1164.all;

entity bcd7seg is
port (bcd_in:  in std_logic_vector(3 downto 0);
      out_7seg:  out std_logic_vector(6 downto 0)
     );
end bcd7seg;

architecture mydecod of bcd7seg is
begin 
  out_7seg <=  "1000000" when bcd_in = "0000" else
               "1111001" when bcd_in = "0001" else
               "0100100" when bcd_in = "0010" else
               "0110000" when bcd_in = "0011" else
               "0011001" when bcd_in = "0100" else
               "0010010" when bcd_in = "0101" else
               "0000010" when bcd_in = "0110" else
               "1111000" when bcd_in = "0111" else
               "0000000" when bcd_in = "1000" else
               "0011000" when bcd_in = "1001" else
               "1111111";
end mydecod;
