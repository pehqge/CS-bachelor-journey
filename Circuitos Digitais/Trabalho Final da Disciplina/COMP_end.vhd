library ieee;
use ieee.std_logic_1164.all;

entity COMP_end is
port(
	E0: in std_logic_vector(3 downto 0);
	endgame: out std_logic
	);
end COMP_end;

architecture comp of COMP_end is
begin
    endgame <= '1' when E0 = "0000" else '0';
    

end comp;