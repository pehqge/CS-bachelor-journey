-- Transforma o clock de 50MHz (clock_50) vindo da placa em sinais de 0.20, 0.25, 0.33, 0.50 e 1Hz.
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;

entity FSM_clock_de2 is
port(
	reset, E: in std_logic;
	clock: in std_logic;
	CLK_1Hz, CLK_050Hz, CLK_033Hz, CLK_025Hz, CLK_020Hz: out std_logic
);
end FSM_clock_de2;

architecture arc of FSM_clock_de2 is
	signal c1, c05, c033, c025, c020: std_logic_vector(27 DOWNTO 0); -- precisamos de 28 bits para representar ateh o valor 100.000.000
begin
	process(reset, E, clock, c1, c05, c033, c025, c020)
	begin
		-- Reset
		if reset = '1' then
			c1 <= x"0000000"; -- notacao para hexadecimal: x"VALOR EM HEXA"
			c05 <= x"0000000";
			c033 <= x"0000000";
			c025 <= x"0000000";
			c020 <= x"0000000";
			
		elsif (clock'event and clock = '1') then
			if E = '1' then
			-- Incrementa todos os contadores
				c1 <= c1 + 1;
				c05 <= c05 + 1;
				c033 <= c033 + 1;
				c025 <= c025 + 1;
				c020 <= c020 + 1;
			
			-- Quando o signal do contador de 0.5Hz (c05) chega a 99 999 999 ({[freq do clock]/[freq desejada] - 1}), zera o contador e ativa a saida C05Hz
	
				if c05 = x"5F5E0FF" then --5F5E0FF eh 99.999.999 em hexadecimal
					CLK_050Hz <= '1'; -- da um pulso para o clock de 0.5Hz (isto ocorrerá a cada 2s)
					c05 <= x"0000000"; -- Ao completar as 99.999.999 voltas, zera o signal do contador
				else 
					CLK_050Hz <= '0'; --	enquanto nao chegar a 99.999.999, mantem C05Hz em 0
				end if;
	
				
			-- 1Hz
				if c1 = x"2faf07f" then
					CLK_1Hz <= '1';
					c1 <= x"0000000";
				else
					CLK_1Hz <= '0';
				end if;
			
			-- 0.33Hz
				if c033 = x"907F00F" then
					CLK_033Hz <= '1';
					c033 <= x"0000000";
				else
					CLK_033Hz <= '0';
				end if;
	
			-- 0.25Hz
				if c025 = x"BEBC1FF" then
					CLK_025Hz <= '1';
					c025 <= x"0000000";
				else
					CLK_025Hz <= '0';
				end if;
	
			-- 0.20Hz
				if c020 = x"EE6B27F" then
					CLK_020Hz <= '1';
					c020 <= x"0000000";
				else
					CLK_020Hz <= '0';
				end if;
				
			end if;
		end if;
	end process;
end arc;