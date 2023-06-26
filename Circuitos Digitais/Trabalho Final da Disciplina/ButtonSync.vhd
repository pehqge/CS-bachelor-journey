library ieee;
use ieee.std_logic_1164.all; 

entity ButtonSync is port(

    KEY1, KEY0, CLK: in  std_logic;
    BTN1, BTN0   : out std_logic);

end ButtonSync;


architecture ButtonSyncImpl of ButtonSync is

type STATES is (EsperaApertar, SaidaAtiva, EsperaSoltar);
signal BTN1_state, BTN0_state: STATES := EsperaApertar;
signal BTN1_next, BTN0_next: STATES := EsperaApertar;

begin


	process (clk) 
	begin
		if clk'event and clk = '1' then
			BTN1_state <= BTN1_next;
			BTN0_state <= BTN0_next;
		end if;
	end process;
	
	
	process (key0, BTN0_state)
	begin
		case BTN0_state is
			when EsperaApertar =>
				if key0 = '0' then BTN0_next <= SaidaAtiva; else BTN0_next <= EsperaApertar; end if;
				BTN0 <= '0';
			when SaidaAtiva =>
				if key0 = '0' then BTN0_next <= EsperaSoltar; else BTN0_next <= EsperaApertar; end if;	
				BTN0 <= '1';
			when EsperaSoltar =>
				if key0 = '0' then BTN0_next <= EsperaSoltar;	else BTN0_next <= EsperaApertar; end if;	
				BTN0 <= '0';
		end case;		
	end process;
	
	
	process (key1, BTN1_state)
	begin
		case BTN1_state is
			when EsperaApertar =>
				if key1 = '0' then BTN1_next <= SaidaAtiva; else BTN1_next <= EsperaApertar; end if;
				BTN1 <= '0';
			when SaidaAtiva =>
				if key1 = '0' then BTN1_next <= EsperaSoltar; else BTN1_next <= EsperaApertar; end if;	
				BTN1 <= '1';
			when EsperaSoltar =>
				if key1 = '0' then BTN1_next <= EsperaSoltar;	else BTN1_next <= EsperaApertar; end if;	
				BTN1 <= '0';
		end case;		
	end process;

	
end ButtonSyncImpl;
