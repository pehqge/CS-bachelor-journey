library IEEE;
use IEEE.Std_Logic_1164.all;

entity registrador_bonus is
port (S, E, clock:  in std_logic;
      D: in std_logic_vector(3 downto 0);
      Q:  out std_logic_vector(3 downto 0));
end registrador_bonus;

architecture regs of registrador_bonus is
  signal QQ: std_logic_vector(3 downto 0);
  
begin
    process(clock, S, E, D)
	begin
	    if (S= '1') then
	        QQ <= "1000";
		elsif (clock'event and clock = '1') then
		    if E = '1' then
                QQ <= D;
        end if;
		end if;
	end process;
	Q <= QQ;

end regs;

