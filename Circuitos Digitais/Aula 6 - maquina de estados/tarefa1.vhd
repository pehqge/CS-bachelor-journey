library ieee;
use ieee.std_logic_1164.all;
entity tarefa1 is port (
   clock: in std_logic;
   reset: in std_logic;
   x,y, z: out std_logic );
end tarefa1;
architecture fsm1arq of tarefa1 is
   type STATES is (A, B, C, D);
   signal EAtual, PEstado: STATES;
begin
	process(clock,reset)
	begin
	    if (reset = '1') then
			EAtual <= A;
        elsif (clock'event AND clock = '1') then 
         	EAtual <= PEstado;
	    end if;
	end process;
    process(EAtual)
	begin
		case EAtual is
			when A => 	Pestado <= B;
                     		x <= '1';
                     		y <= '1';
                     		z <= '1';
			when B => 	Pestado <= C;
                     		x <= '0';
                     		y <= '1';
                     		z <= '1';
            when C => 	Pestado <= D;
                     		x <= '0';
                     		y <= '0';
                     		z <= '1';
            when D => 	Pestado <= A;
                     		x <= '0';
                     		y <= '0';
                     		z <= '0';
		end case;
	end process;
end fsm1arq;
