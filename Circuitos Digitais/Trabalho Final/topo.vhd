library ieee;
use ieee.std_logic_1164.all;

entity topo is
port(
		CLOCK_50: in std_logic;
		CLK_500Hz: in std_logic;
		KEY: in std_logic_vector(1 downto 0);
		SW: in std_logic_vector(17 downto 0);
		HEX0, HEX1, HEX2, HEX3, HEX4, HEX5, HEX6, HEX7: out std_logic_vector(6 downto 0);
		LEDR: out std_logic_vector(15 downto 0)
);	
end topo;

architecture circuito of topo is
signal enter, reset: std_logic;
signal R1, R2, E1, E2, E3, E4, E5: std_logic;
signal end_game, end_time, end_round, end_FPGA: std_logic;		
signal clock: std_logic;

component datapath is
port(
	-- Entradas de dados
	clk: in std_logic;
	SW: in std_logic_vector(17 downto 0);
	
	-- Entradas de controle
	R1, R2, E1, E2, E3, E4, E5: in std_logic;
	
	-- Saídas de dados
	hex0, hex1, hex2, hex3, hex4, hex5, hex6, hex7: out std_logic_vector(6 downto 0);
	ledr: out std_logic_vector(15 downto 0);
	
	-- Saídas de status
	end_game, end_time, end_round, end_FPGA: out std_logic
);
end component;

component controle is
port(
-- Entradas de controle
	enter, reset, CLOCK: in std_logic;
-- Entradas de status
	end_game, end_time, end_round, end_FPGA: in std_logic;
-- Saídas de comandos
	R1, R2, E1, E2, E3, E4, E5: out std_logic
);
end component;

component ButtonSync is port( --saida ja negada

    KEY1, KEY0, CLK: in  std_logic;
    BTN1, BTN0   : out std_logic);

end component;

begin
    datapath0: datapath port map (CLK_500Hz, SW(17 downto 0), R1, R2, E1, E2, E3, E4, E5, hex0, hex1, hex2, hex3, hex4, hex5, hex6, hex7, ledr, end_game, end_time, end_round, end_FPGA);
	controle0: controle port map (enter, reset, CLK_500Hz, end_game, end_time, end_round, end_FPGA, R1, R2, E1, E2, E3, E4, E5);
	ButtonSync0: ButtonSync port map (KEY(1), KEY(0), CLK_500Hz, enter, reset);
end circuito;