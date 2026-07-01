library IEEE;
use IEEE.Std_Logic_1164.all;
use IEEE.std_logic_unsigned.all;

entity counter_round is
port (R, E, clock:  in std_logic;
      Q: out std_logic_vector(3 downto 0);
      tc:  out std_logic);
end counter_round;

architecture counter of counter_round is
  signal round_reg: std_logic_vector(3 downto 0);
  
begin
    process(clock, R, E)
	begin
	    if (R = '1') then
	        round_reg <= "0000";
            tc <= '0';
		elsif clock'event and clock = '1' then
		    if E = '1' then
             round_reg <= round_reg + '1';
            if round_reg > "1110" then
                tc <= '1';
                round_reg <= "1111";
		else
		    tc <= '0';
		end if;
		end if;
		end if;
	end process;
	Q <= round_reg;

end counter;

