library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity topo is

	port (
		--- entradas
		ck, iniciar, reset : in std_logic;
		pA, pB : in std_logic_vector(7 downto 0);

		--- saídas
		pronto, ler : out std_logic;
		end_mem : out std_logic_vector(5 downto 0);
		SAD : out std_logic_vector(13 downto 0)
	);

end entity;

architecture arc of topo is

	--------------- componentes--------------
	component sad_controle is
		port (
			iniciar, rst, clk, menor : in std_logic;
			pronto, read, zi, ci, cpa, cpb, zsoma, csoma, csad_reg : out std_logic
		);
	end component;

	component sad_operativo is
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

	end component;

	--------signals (antes do begin)-------------
	signal zi, ci, cpA, cpB, zsoma, csoma, csad_reg, menor : std_logic;

begin

	controle : sad_controle port map(iniciar, reset, ck, menor, pronto, ler, zi, ci, cpA, cpB, zsoma, csoma, csad_reg);
	datapath : sad_operativo port map(pA, pB, ck, zi, ci, cpA, cpB, zsoma, csoma, csad_reg, menor, SAD, end_mem);

end arc;