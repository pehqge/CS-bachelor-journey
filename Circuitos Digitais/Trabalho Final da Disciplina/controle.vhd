library ieee;
use ieee.std_logic_1164.all;

entity controle is
port(
-- Entradas de controle
	enter, reset, CLOCK: in std_logic;
-- Entradas de status
	end_game, end_time, end_round, end_FPGA: in std_logic;
-- Saídas de comandos
	R1, R2, E1, E2, E3, E4, E5: out std_logic
);
end controle;

architecture cnt of controle is
    type STATES is (init, setup, play_fpga, play_user, count_round, check, waity, result);
    signal EAtual, PEstado: STATES;
begin
    	process(CLOCK, reset)
	begin
	    if reset = '1' then
			EAtual <= init;
        elsif (clock'event and clock = '1') then 
         	EAtual <= PEstado;
	    end if;
	end process;
	

    process(EAtual, enter, end_game, end_time, end_round, end_FPGA)
	begin
		case EAtual is
			when init =>
                         R1 <= '1';
                         R2 <= '1';
                         E1 <= '0';
                         E2 <= '0';
                         E3 <= '0';
                         E4 <= '0';
                         E5 <= '0';
                		 PEstado <= setup;

			when setup =>
                         R1 <= '0';
                         R2 <= '0';
                         E1 <= '1';
                         E2 <= '0';
                         E3 <= '0';
                         E4 <= '0';
                         E5 <= '0';
                         if enter = '0' then
                		    PEstado <= setup;
                		 else 
                		    PEstado <= play_fpga;
                		 end if;
                         
            when play_fpga =>
                         R1 <= '0';
                         R2 <= '0';
                         E1 <= '0';
                         E2 <= '1';
                         E3 <= '0';
                         E4 <= '0';
                         E5 <= '0';
                         if end_fpga = '1' then
                		    PEstado <= play_user;
                		 else 
                		    PEstado <= play_fpga;
                		 end if;
                         
            when play_user =>
                         R1 <= '0';
                         R2 <= '0';
                         E1 <= '0';
                         E2 <= '0';
                         E3 <= '1';
                         E4 <= '0';
                         E5 <= '0';
                         if end_time = '1' then 
                            PEstado <= result;
                		 elsif enter = '1' then
                		    PEstado <= count_round;
                		 else 
                		    PEstado <= play_user;
                		 end if;
                		 
            when count_round =>
                         R1 <= '0';
                         R2 <= '0';
                         E1 <= '0';
                         E2 <= '0';
                         E3 <= '0';
                         E4 <= '1';
                         E5 <= '0';
                		 PEstado <= check;
                		 
            when check =>
                     R1 <= '0';
                     R2 <= '0';
                     E1 <= '0';
                     E2 <= '0';
                     E3 <= '0';
                     E4 <= '0';
                     E5 <= '0';
            		 if end_game = '1' or end_round = '1' then 
            		    PEstado <= result;
            		 else
            		    PEstado <= waity;
            		 end if;
                		 
            when waity =>
                     R1 <= '1';
                     R2 <= '0';
                     E1 <= '0';
                     E2 <= '0';
                     E3 <= '0';
                     E4 <= '0';
                     E5 <= '0';
            		 if enter = '1' then 
            		    PEstado <= play_fpga;
            		 else
            		    PEstado <= waity;
            		 end if;
            
            when result =>
                     R1 <= '0';
                     R2 <= '0';
                     E1 <= '0';
                     E2 <= '0';
                     E3 <= '0';
                     E4 <= '0';
                     E5 <= '1';
            		 if enter = '1' then 
            		    PEstado <= init;
            		 else
            		    PEstado <= result;
            		 end if;
		end case;
	end process;
end cnt;