library IEEE;
use IEEE.Std_Logic_1164.all;

entity tarefa1_2 is
port (D, CLK, RST:  in std_logic;
      Q:  out std_logic_vector(3 downto 0));
end tarefa1_2;

architecture regs of tarefa1_2 is
  signal QQ: std_logic_vector(3 downto 0);
  
begin
    process(CLK, RST)
	begin
	    if (RST = '0') then
	        QQ <= "0000";
		elsif (CLK'event and CLK = '1') then
             QQ <= QQ(2 downto 0) & D;
		end if;
	end process;
	Q <= QQ;

end regs;

