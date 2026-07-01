library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity topo is 
    
    port (
        -- Entradas:
        clk, rst, iniciar : in std_logic;
        data_kernel, data_mem: in std_logic_vector(7 downto 0);

        -- Saidas:
        pronto, read_kernel, read_mem, write_mem_saida: out std_logic;
        end_kernel: out std_logic_vector(3 downto 0);
        end_mem, end_mem_saida: out std_logic_vector(18 downto 0);
        data_mem_saida: out std_logic_vector(7 downto 0)
    );

end entity;

architecture arc of topo is

    -- Signals:
    signal c_i, c_linha, c_coluna, c_soma, cDesCol, cDesLinha, c_end_mem, c_end_mem_saida, selDesCol, selDesLinha, sel_mux_coluna, sel_mux_linha, sel_mux_i, sel_mux_mem_saida, proxLinha, fim_coluna, fim_linha, fim_i, sel_mux_soma: std_logic;

    -- Componentes:

    component controle is
        port(
            -- Entradas
            clk, rst, iniciar, proxLinha, fim_linha, fim_coluna, fim_i: in std_logic;

            -- Saidas
            pronto, write_mem_saida, read_kernel, read_mem, c_i, c_linha, c_coluna, c_soma, cDesCol, cDesLinha, c_end_mem, c_end_mem_saida, SelDesCol, SelDeslinha, sel_mux_coluna, sel_mux_linha, sel_mux_i, sel_mux_soma, sel_mux_mem_saida: out std_logic
        );
    end component;


    component datapath is
	PORT (
		---- ENTRADAS DE DADOS	
		clk : IN STD_LOGIC;
		data_kernel : IN STD_LOGIC_VECTOR(7 downto 0);
		data_mem : IN STD_LOGIC_VECTOR(7 downto 0);

		----ENTRADAS DE CONTROLE
		c_i, c_linha, c_coluna, c_soma, c_end_mem, c_end_mem_saida : IN STD_LOGIC;
		cDesCol, CDesLinha, SelDesCol, SelDesLinha : IN STD_LOGIC;
		sel_mux_coluna, sel_mux_linha, sel_mux_i, sel_mux_soma, sel_mux_mem_saida: IN STD_LOGIC;

		----SAÍDAS DE DADOS
		end_kernel : OUT STD_LOGIC_VECTOR(3 DOWNTO 0);
		end_mem, end_mem_saida : OUT STD_LOGIC_VECTOR(18 DOWNTO 0);
		data_mem_saida : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);

		---- SAÍDAS DE CONTROLE
		proxLinha, fim_linha, fim_coluna, fim_i : out STD_LOGIC

	);

    end component;

begin 
    control_e : controle port map(clk, rst, iniciar, proxLinha, fim_linha, fim_coluna, fim_i, pronto, write_mem_saida, read_kernel, read_mem, c_i, c_linha, c_coluna, c_soma, cDesCol, cDesLinha, c_end_mem, c_end_mem_saida, SelDesCol, SelDeslinha, sel_mux_coluna, sel_mux_linha, sel_mux_i, sel_mux_soma, sel_mux_mem_saida);
	operativo : datapath port map(
        clk, data_kernel, data_mem, 
        c_i, c_linha, c_coluna, c_soma,
        c_end_mem, c_end_mem_saida,
        cDesCol, CDesLinha, SelDesCol, SelDesLinha,
        sel_mux_coluna, sel_mux_linha, sel_mux_i, sel_mux_soma, sel_mux_mem_saida,
        end_kernel,end_mem,
        end_mem_saida, data_mem_saida,
        proxLinha, fim_linha, fim_coluna, fim_i);

end arc;


