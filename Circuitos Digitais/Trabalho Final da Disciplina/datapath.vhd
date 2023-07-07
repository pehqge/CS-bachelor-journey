library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;

entity datapath is
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
end entity;

architecture arc of datapath is
---------------------------SIGNALS-----------------------------------------------------------
--contadores
signal tempo, X: std_logic_vector(3 downto 0);
--FSM_clock
signal CLK_1Hz, CLK_050Hz, CLK_033Hz, CLK_025Hz, CLK_020Hz: std_logic;
--Logica combinacional
signal RESULT: std_logic_vector(7 downto 0);
--Registradores
signal SEL: std_logic_vector(3 downto 0);
signal USER: std_logic_vector(14 downto 0);
signal Bonus, Bonus_reg: std_logic_vector(3 downto 0);
--ROMs
signal CODE_aux: std_logic_vector(14 downto 0);
signal CODE: std_logic_vector(31 downto 0);
--COMP
signal erro: std_logic;
--NOR enables displays
signal E23, E25, E12: std_logic;

--signals implícitos--

--dec termometrico
signal stermoround, stermobonus, andtermo: std_logic_vector(15 downto 0);
--decoders HEX 7-0
signal sdecod7, sdec7, sdecod6, sdec6, sdecod5, sdecod4, sdec4, sdecod3, sdecod2, sdec2, sdecod1, sdecod0, sdec0: std_logic_vector(6 downto 0);
signal smuxhex7, smuxhex6, smuxhex5, smuxhex4, smuxhex3, smuxhex2, smuxhex1, smuxhex0: std_logic_vector(6 downto 0);
signal edec2, edec0: std_logic_vector(3 downto 0);
--saida ROMs
signal srom0, srom1, srom2, srom3: std_logic_vector(31 downto 0);
signal srom0a, srom1a, srom2a, srom3a: std_logic_vector(14 downto 0);
--FSM_clock
signal E2orE3: std_logic;

---------------------------COMPONENTS-----------------------------------------------------------
component counter_time is 
port(
	R, E, clock: in std_logic;
	Q: out std_logic_vector(3 downto 0);
	tc: out std_logic
);
end component;

component counter_round is
port(
	R, E, clock: in std_logic;
	Q: out std_logic_vector(3 downto 0);
	tc: out std_logic
);
end component;

component decoder_termometrico is
 port(
	X: in  std_logic_vector(3 downto 0);
	S: out std_logic_vector(15 downto 0)
);
end component;

component FSM_clock_de2 is
port(
	reset, E: in std_logic;
	clock: in std_logic;
	CLK_1Hz, CLK_050Hz, CLK_033Hz, CLK_025Hz, CLK_020Hz: out std_logic
);
end component;

component FSM_clock_emu is
port(
	reset, E: in std_logic;
	clock: in std_logic;
	CLK_1Hz, CLK_050Hz, CLK_033Hz, CLK_025Hz, CLK_020Hz: out std_logic
);
end component;

component decod7seg is
port(
	C: in std_logic_vector(3 downto 0);
	F: out std_logic_vector(6 downto 0)
 );
end component;

component d_code is
port(
	C: in std_logic_vector(3 downto 0);
	F: out std_logic_vector(6 downto 0)
 );
end component;

component mux2x1_7bits is
port(
	E0, E1: in std_logic_vector(6 downto 0);
	sel: in std_logic;
	saida: out std_logic_vector(6 downto 0)
);
end component;

component mux2x1_16bits is
port(
	E0, E1: in std_logic_vector(15 downto 0);
	sel: in std_logic;
	saida: out std_logic_vector(15 downto 0)
);
end component;

component mux4x1_1bit is
port(
	E0, E1, E2, E3: in std_logic;
	sel: in std_logic_vector(1 downto 0);
	saida: out std_logic
);
end component;

component mux4x1_15bits is
port(
	E0, E1, E2, E3: in std_logic_vector(14 downto 0);
	sel: in std_logic_vector(1 downto 0);
	saida: out std_logic_vector(14 downto 0)
);
end component;

component mux4x1_32bits is
port(
	E0, E1, E2, E3: in std_logic_vector(31 downto 0);
	sel: in std_logic_vector(1 downto 0);
	saida: out std_logic_vector(31 downto 0)
);
end component;

component registrador_sel is 
port(
	R, E, clock: in std_logic;
	D: in std_logic_vector(3 downto 0);
	Q: out std_logic_vector(3 downto 0) 
);
end component;

component registrador_user is 
port(
	R, E, clock: in std_logic;
	D: in std_logic_vector(14 downto 0);
	Q: out std_logic_vector(14 downto 0) 
);
end component;

component registrador_bonus is 
port(
	S, E, clock: in std_logic;
	D: in std_logic_vector(3 downto 0);
	Q: out std_logic_vector(3 downto 0) 
);
end component;

component COMP_erro is
port(
	E0, E1: in std_logic_vector(14 downto 0);
	diferente: out std_logic
);
end component;

component COMP_end is
port(
	E0: in std_logic_vector(3 downto 0);
	endgame: out std_logic
);
end component;

component subtracao is
port(
	E0: in std_logic_vector(3 downto 0);
	E1: in std_logic;
	resultado: out std_logic_vector(3 downto 0)
);
end component;

component logica is 
port(
	round, bonus: in std_logic_vector(3 downto 0);
	nivel: in std_logic_vector(1 downto 0);
	points: out std_logic_vector(7 downto 0)
);
end component;

component ROM0 is
port(
	address: in std_logic_vector(3 downto 0);
	output : out std_logic_vector(31 downto 0)
);
end component;

component ROM1 is
port(
	address: in std_logic_vector(3 downto 0);
	output : out std_logic_vector(31 downto 0)
);
end component;

component ROM2 is
port(
	address: in std_logic_vector(3 downto 0);
	output : out std_logic_vector(31 downto 0)
);
end component;

component ROM3 is
port(
	address: in std_logic_vector(3 downto 0);
	output : out std_logic_vector(31 downto 0)
);
end component;

component ROM0a is
port(
	address: in std_logic_vector(3 downto 0);
	output : out std_logic_vector(14 downto 0)
);
end component;

component ROM1a is
port(
	address: in std_logic_vector(3 downto 0);
	output : out std_logic_vector(14 downto 0)
);
end component;

component ROM2a is
port(
	address: in std_logic_vector(3 downto 0);
	output : out std_logic_vector(14 downto 0)
);
end component;

component ROM3a is
port(
	address: in std_logic_vector(3 downto 0);
	output : out std_logic_vector(14 downto 0)
);
end component;

-- COMECO DO CODIGO ---------------------------------------------------------------------------------------

begin	

--Conexoes e atribuicoes a partir daqui. Dica: usar os mesmos nomes e I/O ja declarados nos components. Todos os signals necessarios ja estao declarados.

-- Counters
counter_time0: counter_time port map (R1, E3, CLK_1Hz, tempo, end_time);
counter_round0: counter_round port map (R2, E4, clk, X, end_round);

-- Circuito decoder_termometrico
decoder_term0: decoder_termometrico port map (Bonus_reg, stermobonus);
decoder_term1: decoder_termometrico port map (X, stermoround);
andtermo <= stermoround and not(E1&E1&E1&E1&E1&E1&E1&E1&E1&E1&E1&E1&E1&E1&E1&E1);
mux_decorder: mux2x1_16bits port map (andtermo, stermobonus, SW(17), ledr);

-- Bloco FSM_EMU
E2orE3 <= E2 or E3;
selecionador: registrador_sel port map (R2, E1, clk, SW(3 downto 0), SEL);
FSM_emu: FSM_clock_emu port map (R1, E2orE3, clk, CLK_1Hz, CLK_050Hz, CLK_033Hz, CLK_025Hz, CLK_020Hz);
mux_clks: mux4x1_1bit port map (CLK_020Hz, CLK_025Hz, CLK_033Hz, CLK_050Hz, SEL(1 downto 0), end_FPGA);

-- Bloco Roms + MUXs
rommy0: ROM0 port map (X, srom0);
rommy1: ROM1 port map (X, srom1);
rommy2: ROM2 port map (X, srom2);
rommy3: ROM3 port map (X, srom3);
mux_rommy: mux4x1_32bits port map (srom0, srom1, srom2, srom3, SEL(3 downto 2), CODE);

romma0: ROM0a port map (X, srom0a);
romma1: ROM1a port map (X, srom1a);
romma2: ROM2a port map (X, srom2a);
romma3: ROM3a port map (X, srom3a);
mux_romma: mux4x1_15bits port map (srom0a, srom1a, srom2a, srom3a, SEL(3 downto 2), CODE_aux);

-- Registrador User
reg_user: registrador_user port map (R2, E3, clk, SW(14 downto 0), USER);

-- Comp Igualdade
comp_ig: COMP_erro port map (CODE_aux, USER, erro);

-- Modulo Subtracao e Bonus
subtration: subtracao port map (Bonus_reg, erro, Bonus);
reg_bonus: registrador_bonus port map (R2, E4, clk, Bonus, Bonus_reg);
comp_zero: COMP_end port map (Bonus_reg, end_game);

-- Logica Combinacional
log_comb: logica port map (X, Bonus_reg, SEL(1 downto 0), RESULT);

-- NORs sozinhos
E23 <= E2 nor E3;
E25 <= E2 nor E5;
E12 <= E1 nor E2;

-- Parte dos HEXs
-- HEX 7
d_code7: d_code port map (CODE(31 downto 28), sdecod7);
dec7: decod7seg port map (RESULT(7 downto 4), sdec7);
mux7: mux2x1_7bits port map (sdecod7, sdec7, E5, smuxhex7);
hex7 <= smuxhex7 or E25&E25&E25&E25&E25&E25&E25;

-- HEX 6
d_code6: d_code port map (CODE(27 downto 24), sdecod6);
dec6: decod7seg port map (RESULT(3 downto 0), sdec6);
mux6: mux2x1_7bits port map (sdecod6, sdec6, E5, smuxhex6);
hex6 <= smuxhex6 or E25&E25&E25&E25&E25&E25&E25;

-- HEX 5
d_code5: d_code port map (CODE(23 downto 20), sdecod5);
mux5: mux2x1_7bits port map (sdecod5, "0000111", E3, smuxhex5);
hex5 <= smuxhex5 or E23&E23&E23&E23&E23&E23&E23;

-- HEX 4
d_code4: d_code port map (CODE(19 downto 16), sdecod4);
dec4: decod7seg port map (Tempo, sdec4);
mux4: mux2x1_7bits port map (sdecod4, sdec4, E3, smuxhex4);
hex4 <= smuxhex4 or E23&E23&E23&E23&E23&E23&E23;

-- HEX 3
d_code3: d_code port map (CODE(15 downto 12), sdecod3);
mux3: mux2x1_7bits port map (sdecod3, "1000110", E1, smuxhex3);
hex3 <= smuxhex3 or E12&E12&E12&E12&E12&E12&E12;

-- HEX 2
d_code2: d_code port map (CODE(11 downto 8), sdecod2);
edec2 <= "00"&SEL(3 downto 2);
dec2: decod7seg port map (edec2, sdec2);
mux2: mux2x1_7bits port map (sdecod2, sdec2, E1, smuxhex2);
hex2 <= smuxhex2 or E12&E12&E12&E12&E12&E12&E12;

-- HEX 1
d_code1: d_code port map (CODE(7 downto 4), sdecod1);
mux1: mux2x1_7bits port map (sdecod1, "1000111", E1, smuxhex1);
hex1 <= smuxhex1 or E12&E12&E12&E12&E12&E12&E12;

-- HEX 0
d_code0: d_code port map (CODE(3 downto 0), sdecod0);
edec0 <= "00"&SEL(1 downto 0);
dec0: decod7seg port map (edec0, sdec0);
mux0: mux2x1_7bits port map (sdecod0, sdec0, E1, smuxhex0);
hex0 <= smuxhex0 or E12&E12&E12&E12&E12&E12&E12;


end arc;