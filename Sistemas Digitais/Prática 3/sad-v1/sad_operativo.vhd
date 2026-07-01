library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity sad_operativo is
	port (
		-- ENTRADAS DE DADOS
		Mem_A : in std_logic_vector(7 downto 0);
		Mem_B : in std_logic_vector(7 downto 0);
		clk : in std_logic;

		--ENTRADAS DE CONTROLE
		zi, ci, cpA, cpB, zsoma, csoma, csad_reg : in std_logic;

		-- SAÍDA DE CONTROLE
		menor : out std_logic;

		-- SAIDAS DE DADOS
		SAD : out std_logic_vector(13 downto 0);
		end_mem : out std_logic_vector(5 downto 0)
	);

end sad_operativo;

architecture arc of sad_operativo is

	--------- SIGNALS----------
	signal S_pA, S_pB, S_subtrator : std_logic_vector(7 downto 0);
	signal S_mux_cont, S_reg_i, S_somador_cont : std_logic_vector(6 downto 0);
	signal end_memoria : std_logic_vector(5 downto 0);
	signal eS_subtrator, S_somador_AB, S_reg_soma, S_mux_14bits : std_logic_vector(13 downto 0);

	--------- COMPONENTES----------
	component MUX2X1 is
		generic (N : integer);
		port (
			SEL : in std_logic;
			ENT0, ENT1 : in std_logic_vector(N - 1 downto 0);
			output : out std_logic_vector(N - 1 downto 0)
		);
	end component;

	component registrador is
		generic (N : integer);
		port (
			clk, carga : in std_logic;
			d : in std_logic_vector(N - 1 downto 0);
			q : out std_logic_vector(N - 1 downto 0)
		);
	end component;

	component somador is
		generic (N : integer);
		port (
			A, B : in std_logic_vector(N - 1 downto 0);
			S : out std_logic_vector(N - 1 downto 0)
		);
	end component;

	component subtrator is
		generic (N : integer);
		port (
			A, B : in std_logic_vector(N - 1 downto 0);
			S : out std_logic_vector(N - 1 downto 0)
		);
	end component;

	component somadorover is
		generic (N : integer);
		port (
			A, B : in std_logic_vector(N - 1 downto 0);
			S : out std_logic_vector(N downto 0)
		);
	end component;

	--------- MAPEAMENTO ----------
begin

	---- contador e endereçamento

	mux_i : MUX2X1
	generic map(N => 7)
	port map(zi, S_somador_cont, "0000000", S_mux_cont);

	reg_i : registrador
	generic map(N => 7)
	port map(clk, ci, S_mux_cont, S_reg_i);

	menor <= not(S_reg_i(6));
	end_memoria <= S_reg_i(5 downto 0);

	somador_i : somadorover
	generic map(N => 6)
	port map(end_memoria, "000001", S_somador_cont);

	------ somatório

	reg_pA : registrador
	generic map(N => 8)
	port map(clk, cpA, Mem_A, S_pA);

	reg_pB : registrador
	generic map(N => 8)
	port map(clk, cpB, Mem_B, S_pB);



	sub : subtrator
	generic map(N => 8)
	port map(S_pA, S_pB, S_subtrator);

	eS_subtrator <= "000000" & S_subtrator;

	somador_AB : somador
	generic map(N => 14)
	port map(S_reg_soma, eS_subtrator, S_somador_AB);

	mux_14bits : MUX2X1
	generic map(N => 14)
	port map(zsoma, S_somador_AB, "00000000000000", S_mux_14bits);

	reg_soma : registrador
	generic map(N => 14)
	port map(clk, csoma, S_mux_14bits, S_reg_soma);

	reg_SAD : registrador
	generic map(N => 14)
	port map(clk, csad_reg, S_reg_soma, SAD);

	end_mem <= end_memoria;

end arc;