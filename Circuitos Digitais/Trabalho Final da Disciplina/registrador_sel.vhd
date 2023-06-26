library IEEE;
use IEEE.Std_Logic_1164.all;

entity registrador_sel is
port (R, E, clock:  in std_logic;
      D: in std_logic_vector(3 downto 0);
      Q:  out std_logic_vector(3 downto 0));
end registrador_sel;

architecture regs of registrador_sel is
  signal QQ: std_logic_vector(3 downto 0);
  
begin
    process(clock, R, E, D)
	begin
	    if (R = '1') then
	        QQ <= "0000";
		elsif (clock'event and clock = '1' and E = '1') then
             QQ <= D;
		end if;
	end process;
	Q <= QQ;

end regs;

