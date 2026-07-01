library IEEE;
use IEEE.Std_Logic_1164.all;
use IEEE.std_logic_unsigned.all;

entity counter_time is
port (R, E, clock:  in std_logic;
      Q: out std_logic_vector(3 downto 0);
      tc:  out std_logic);
end counter_time;

architecture counter of counter_time is
  signal time_reg: std_logic_vector(3 downto 0);
  
begin
    process(clock, R, E, time_reg)
	begin
	    if (R = '1') then
	        time_reg <= "1010";
            tc <= '0';
		elsif clock'event and clock = '1' then
		if E = '1' then
             time_reg <= time_reg - '1';
		if time_reg = "0000" then
		    tc <= '1';
		else 
		    tc <= '0';
		end if;
		end if;
		end if;
	end process;
	Q <= time_reg;

end counter;

