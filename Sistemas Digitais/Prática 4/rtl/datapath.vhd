LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
ENTITY datapath IS
	PORT (
		---- ENTRADAS DE DADOS	
		clk : IN STD_LOGIC;
		data_kernel : IN STD_LOGIC_VECTOR(7 downto 0);
		data_mem : IN STD_LOGIC_VECTOR(7 downto 0);

		----ENTRADAS DE CONTROLE
		c_i, c_linha, c_coluna, c_soma, c_end_mem, c_end_mem_saida : IN STD_LOGIC;
		cDesCol, CDesLinha, SelDesCol, SelDesLinha : IN STD_LOGIC;
		sel_mux_coluna, sel_mux_linha, sel_mux_i, sel_mux_soma, sel_mux_mem_saida: IN STD_LOGIC;

		----SAÃDAS DE DADOS
		end_kernel : OUT STD_LOGIC_VECTOR(3 DOWNTO 0);
		end_mem, end_mem_saida : OUT STD_LOGIC_VECTOR(18 DOWNTO 0);
		data_mem_saida : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);

		---- SAÃDAS DE CONTROLE
		proxLinha, fim_linha, fim_coluna, fim_i : out STD_LOGIC

	);

END datapath;

ARCHITECTURE arc OF datapath IS

	--------- SIGNALS----------
	SIGNAL inout_desColuna, inout_desLinha, s_mux_desColuna, s_mux_desLinha, s_DesColuna, s_DesLinha, c1 : STD_LOGIC_VECTOR(2 DOWNTO 0);
	SIGNAL s_multiplicador : STD_LOGIC_VECTOR(15 DOWNTO 0);
	signal resultado_divisao : std_logic_vector(11 DOWNTO 0);
	signal ent_somador_1, temp_data_mem_saida, s_mux_soma: std_logic_vector(7 DOWNTO 0);
	signal s_somador_1: std_logic_vector(8 DOWNTO 0);
	signal ent_somador_2, ent_somador_3, s_somador_2, s_somador_3, c2_1, temp_s_somador_leitura_1, temp_s_somador_leitura_2 : std_logic_vector(10 downto 0);
	signal s_multiplicador_2, ent_somador_4: std_logic_vector(19 downto 0);
	signal operacao_leitura_1, operacao_leitura_2, ent_somador_leitura_1, ent_somador_leitura_2 : std_logic_vector(10 downto 0);
	signal s_somador_leitura_1, s_somador_leitura_2: std_LOGIC_VECTOR(10 downto 0);
	signal ent_1_somador_leitura_3, ent_2_somador_leitura_3 : std_logic_vector(19 downto 0);
	signal end_mem_saida_intermediario, s_somador_leitura_3 : std_logic_vector(20 downto 0);
	signal linha, coluna : std_LOGIC_VECTOR(9 downto 0);
	signal end_mem_in, s_mux_mem_saida : std_logic_vector(18 downto 0);
	


	--------- COMPONENTES----------
	COMPONENT MUX2X1 IS
		GENERIC (N : INTEGER);
		PORT (
			SEL : IN STD_LOGIC;
			ENT0, ENT1 : IN STD_LOGIC_VECTOR(N - 1 DOWNTO 0);
			output : OUT STD_LOGIC_VECTOR(N - 1 DOWNTO 0)
		);
	END COMPONENT;

	COMPONENT registrador IS
		GENERIC (N : INTEGER);
		PORT (
			clk, carga : IN STD_LOGIC;
			d : IN STD_LOGIC_VECTOR(N - 1 DOWNTO 0);
			q : OUT STD_LOGIC_VECTOR(N - 1 DOWNTO 0)
		);
	END COMPONENT;

	COMPONENT somador IS
		GENERIC (N : INTEGER);
		PORT (
			A, B : IN STD_LOGIC_VECTOR(N - 1 DOWNTO 0);
			S : OUT STD_LOGIC_VECTOR(N DOWNTO 0)
		);
	END COMPONENT;

	COMPONENT somador_signed IS
		GENERIC (N : INTEGER);
		PORT (
			A, B : IN signed(N - 1 DOWNTO 0);
			S : OUT STD_LOGIC_VECTOR(N - 1 DOWNTO 0));
	END COMPONENT;
	
	COMPONENT contador IS
		GENERIC (N : INTEGER);
		PORT (
			CONSTANTE, constante_comparador : IN STD_LOGIC_VECTOR(N - 1 DOWNTO 0);
			sel_mux, carga : IN STD_LOGIC;
			clk : in STD_LOGIC;
			fim : OUT STD_LOGIC;
			Saida : OUT STD_LOGIC_VECTOR(N - 1 DOWNTO 0)
		);
	END COMPONENT;

	COMPONENT multiplicador IS
		GENERIC (N : INTEGER);
		PORT (
			A, B : IN STD_LOGIC_VECTOR(N - 1 DOWNTO 0);
			S : OUT STD_LOGIC_VECTOR(N*2 - 1 DOWNTO 0));
	END COMPONENT;
BEGIN
	--------- CIRCUITO ----------

	---- contadores

	contador_i : contador
	GENERIC MAP(N => 4)
	PORT MAP("0000","1001", sel_mux_i, c_i, clk, fim_i, end_kernel);

	contador_linha : contador
	GENERIC MAP(N => 10)
	PORT MAP("0000000001", "1001011001", sel_mux_linha, c_linha, clk, fim_linha, linha);

	contador_coluna : contador
	GENERIC MAP(N => 10)
	PORT MAP("0000000001", "1001011001", sel_mux_coluna, c_coluna, clk, fim_coluna, coluna);

	------ calculo da memoria mem

	----coluna
	mux_desColuna : MUX2X1
	GENERIC MAP(N => 3)
	PORT MAP(selDesCol, "111", inout_desColuna, s_mux_desColuna);

	deslocaColuna : registrador
	GENERIC MAP(N => 3)
	PORT MAP(clk, cDesCol, s_mux_desColuna, s_desColuna);
	
	c1 <= "001";
	somador_signed_coluna : somador_signed
	GENERIC MAP(N => 3)
	PORT MAP(signed(c1), signed(s_desColuna), inout_desColuna);

	proxLinha <= '1' when s_desColuna = "001" else '0';

	----- linha
	mux_deslinha : MUX2X1
	GENERIC MAP(N => 3)
	PORT MAP(selDesLinha, "111", inout_desLinha, s_mux_desLinha);

	deslocaLinha : registrador
	GENERIC MAP(N => 3)
	PORT MAP(clk, cDesLinha, s_mux_desLinha, s_desLinha);

	somador_signed_linha : somador_signed
	GENERIC MAP(N => 3)
	PORT MAP(signed(c1), signed(s_desLinha), inout_desLinha);

	-- OperaÃ§Ãµes memoria
	
	operacao_leitura_1 <=  s_desLinha(2)& s_desLinha(2)& s_desLinha(2)& s_desLinha(2)& s_desLinha(2)& s_desLinha(2)& s_desLinha(2)& s_desLinha(2)& s_desLinha;
	ent_somador_leitura_1 <= '0' & linha;

	somador_leitura_1: somador_signed
	generic map(N=>11)
	port map(signed(operacao_leitura_1), signed(ent_somador_leitura_1), s_somador_leitura_1);
	
	operacao_leitura_2 <= s_desColuna(2)&s_desColuna(2)&s_desColuna(2)&s_desColuna(2)&s_desColuna(2)&s_desColuna(2)&s_desColuna(2)&s_desColuna(2)& s_desColuna;
	ent_somador_leitura_2 <= '0' & coluna;

	somador_leitura_2: somador_signed
	generic map(N=>11)
	port map(signed(operacao_leitura_2), signed(ent_somador_leitura_2), s_somador_leitura_2);

	--s_somador_leitura_1 <= '0'&temp_s_somador_leitura_1; 
	--s_somador_leitura_2 <= '0'&temp_s_somador_leitura_2;
	
	multiplicador_leitura_1: multiplicador
	generic map(N=>10)
	port map(s_somador_leitura_1(9 downto 0),"1001011010", ent_2_somador_leitura_3);

	ent_1_somador_leitura_3 <= "0000000000" & s_somador_leitura_2(9 downto 0);

	somador_leitura_3: somador
	generic map(N=>20)
	port map(ent_1_somador_leitura_3,ent_2_somador_leitura_3,s_somador_leitura_3);

-- Saida endereÃ§o memoria
	
	end_mem_in <= s_somador_leitura_3(18 downto 0);

	registrador_end_mem: registrador
	GENERIC MAP(N => 19)
	PORT MAP(clk, c_end_mem, end_mem_in, end_mem);

------ TRECHO APÃ“S LEITURA DE MEM

	multiplic : multiplicador
	GENERIC MAP(N => 8)
	PORT MAP(data_kernel, data_mem, s_multiplicador);

	---- divisÃ£o
	resultado_divisao <= s_multiplicador(15 DOWNTO 4);
	---- desconsidera 4 bits MSB
	ent_somador_1 <= resultado_divisao(7 DOWNTO 0);

	somador_1 : somador
	GENERIC MAP(N => 8)
	PORT MAP(ent_somador_1, temp_data_mem_saida, s_somador_1);

	mux_reg_soma : MUX2X1
	GENERIC MAP(N => 8)
	PORT MAP(sel_mux_soma, s_somador_1(7 downto 0), "00000000", s_mux_soma);


	reg_soma : registrador
	GENERIC MAP(N => 8)
	PORT MAP(clk, c_soma, s_mux_soma, temp_data_mem_saida);

	data_mem_saida <= temp_data_mem_saida;

	---- entrada de end_mem_saida
	c2_1 <= "11111111111";
	
	ent_somador_2 <= '0'&linha;
	somador_2 : somador_signed
	GENERIC MAP(N => 11)
	PORT MAP(signed(c2_1), signed(ent_somador_2),s_somador_2); 

	ent_somador_3 <= '0'&coluna;
	somador_3 : somador_signed
	GENERIC MAP(N => 11)
	PORT MAP(signed(c2_1), signed(ent_somador_3),s_somador_3); 


	multiplicador_2: multiplicador
	generic map(N=>10)
	port map(s_somador_2(9 downto 0), "1001011000", s_multiplicador_2);
	
	ent_somador_4 <= "0000000000"&s_somador_3(9 downto 0);
	somador_4: somador
	generic map(N=>20)
	port map(s_multiplicador_2, ent_somador_4, end_mem_saida_intermediario);

	mux_mem_saida : MUX2X1
	GENERIC MAP(N => 19)
	PORT MAP(sel_mux_mem_saida, end_mem_saida_intermediario(18 downto 0), "0000000000000000000", s_mux_mem_saida);

	registrador_end_mem_saida: registrador
	GENERIC MAP(N => 19)
	PORT MAP(clk, c_end_mem_saida, s_mux_mem_saida, end_mem_saida);

END arc;