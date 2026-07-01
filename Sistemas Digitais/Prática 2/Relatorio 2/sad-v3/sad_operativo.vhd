library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity sad_operativo is
	port (
		-- ENTRADAS DE DADOS
		Mem_A : in std_logic_vector(31 downto 0); -- mudado para 32 bits
		Mem_B : in std_logic_vector(31 downto 0);
		clk : in std_logic;

		--ENTRADAS DE CONTROLE
		zi, ci, cpA, cpB, zsoma, csoma, csad_reg : in std_logic;

		-- SAÍDA DE CONTROLE
		menor : out std_logic;

		-- SAIDAS DE DADOS
		SAD : out std_logic_vector(13 downto 0);
		end_mem : out std_logic_vector(3 downto 0)
	);

end sad_operativo;

architecture arc of sad_operativo is

	--------- SIGNALS----------
	signal S_pA0, S_pA1, S_pA2, S_pA3, S_pB0, S_pB1, S_pB2, S_pB3, S_subtrator0, S_subtrator1, S_subtrator2, S_subtrator3 : std_logic_vector(7 downto 0);
	signal S_Somador0, S_Somador1 : std_logic_vector(8 downto 0);
	signal S_Somador2 : std_logic_vector(9 downto 0);
	signal eS_Somador2, S_reg_soma, S_mux_14bits, S_SomadorTotal : std_logic_vector(13 downto 0);
	signal S_mux_cont, S_reg_i, S_somador_cont : std_logic_vector(4 downto 0);
	signal end_memoria : std_logic_vector(3 downto 0);

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
	generic map(N => 5)
	port map(zi, S_somador_cont, "00000", S_mux_cont);

	reg_i : registrador
	generic map(N => 5)
	port map(clk, ci, S_mux_cont, S_reg_i);

	menor <= not(S_reg_i(4));
	end_memoria <= S_reg_i(3 downto 0);

	somador_i : somadorover
	generic map(N => 4)
	port map(end_memoria, "0001", S_somador_cont);

	------ somatório

	-- registradores de 8 bits

	reg_pA0 : registrador
	generic map(N => 8)
	port map(clk, cpA, Mem_A(7 downto 0), S_pA0);

	reg_pA1 : registrador
	generic map(N => 8)
	port map(clk, cpA, Mem_A(15 downto 8), S_pA1);

	reg_pA2 : registrador
	generic map(N => 8)
	port map(clk, cpA, Mem_A(23 downto 16), S_pA2);

	reg_pA3 : registrador
	generic map(N => 8)
	port map(clk, cpA, Mem_A(31 downto 24), S_pA3);

	reg_pB0 : registrador
	generic map(N => 8)
	port map(clk, cpB, Mem_B(7 downto 0), S_pB0);

	reg_pB1 : registrador
	generic map(N => 8)
	port map(clk, cpB, Mem_B(15 downto 8), S_pB1);

	reg_pB2 : registrador
	generic map(N => 8)
	port map(clk, cpB, Mem_B(23 downto 16), S_pB2);

	reg_pB3 : registrador
	generic map(N => 8)
	port map(clk, cpB, Mem_B(31 downto 24), S_pB3);

	-- subtratores e ABS

	sub0 : subtrator
	generic map(N => 8)
	port map(S_pA0, S_pB0, S_subtrator0);

	sub1 : subtrator
	generic map(N => 8)
	port map(S_pA1, S_pB1, S_subtrator1);

	sub2 : subtrator
	generic map(N => 8)
	port map(S_pA2, S_pB2, S_subtrator2);

	sub3 : subtrator
	generic map(N => 8)
	port map(S_pA3, S_pB3, S_subtrator3);

	-- somadores da memoria

	somador_0 : somadorover
	generic map(N => 8)
	port map(S_Subtrator0, S_Subtrator1, S_Somador0);

	somador_1 : somadorover
	generic map(N => 8)
	port map(S_Subtrator2, S_Subtrator3, S_Somador1);

	somador_2 : somadorover
	generic map(N => 9)
	port map(S_Somador0, S_Somador1, S_Somador2);

	-- somador total

	eS_Somador2 <= "0000" & S_Somador2;

	somador_total : somador
	generic map(N => 14)
	port map(S_reg_soma, eS_Somador2, S_SomadorTotal);

	mux_14bits : MUX2X1
	generic map(N => 14)
	port map(zsoma, S_SomadorTotal, "00000000000000", S_mux_14bits);

	reg_soma : registrador
	generic map(N => 14)
	port map(clk, csoma, S_mux_14bits, S_reg_soma);

	reg_SAD : registrador
	generic map(N => 14)
	port map(clk, csad_reg, S_reg_soma, SAD);

	end_mem <= end_memoria;

end arc;