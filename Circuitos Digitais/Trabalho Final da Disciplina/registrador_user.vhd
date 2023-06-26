library IEEE;
use IEEE.Std_Logic_1164.all;

entity registrador_user is
port (R, E, clock:  in std_logic;
      D: in std_logic_vector(14 downto 0);
      Q:  out std_logic_vector(14 downto 0));
end registrador_user;

architecture regs of registrador_user is
  signal QQ: std_logic_vector(14 downto 0);
  
begin
    process(clock, R, E)
	begin
	    if (R = '1') then
	        QQ <= "000000000000000";
		elsif (clock'event and clock = '1' and E = '1') then
             QQ <= D;
		end if;
	end process;
	Q <= QQ;

end regs;

