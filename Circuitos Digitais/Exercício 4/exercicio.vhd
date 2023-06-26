library ieee;
use ieee.std_logic_1164.all;
entity exercicio is port (
   clock, reset, b: in std_logic;
   s1, s2: out std_logic );
end exercicio;
architecture fsm1arq of exercicio is
   type STATES is (init, On1, Off1, On2, Off2);
   signal EAtual, PEstado: STATES;
begin
	process(clock,reset)
	begin
	    if (reset = '1') then
			EAtual <= init;
        elsif (clock'event AND clock = '1') then 
         	EAtual <= PEstado;
	    end if;
	end process;
    process(EAtual, b)
	begin
		case EAtual is
			when init =>
                         s1 <= '1';
                         s2 <= '0';
                         if (b='1') then
                		  PEstado <= On1;
                		else
                		  PEstado <= init;
                		end if;

			when On1 =>
                         s1 <= '0';
                         s2 <= '1';
                         PEstado <= Off1;
                         
            when Off1 =>
                         s1 <= '0';
                         s2 <= '0';
                         PEstado <= On2;
                         
            when On2 =>
                         s1 <= '0';
                         s2 <= '1';
                         PEstado <= Off2;
            when Off2 =>
                         s1 <= '1';
                         s2 <= '0';
                         if (b='1') then
                		  PEstado <= On1;
                		else
                		  PEstado <= Off2;
                		end if;
		end case;
	end process;
end fsm1arq;
