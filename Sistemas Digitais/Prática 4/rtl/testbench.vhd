library IEEE;
use IEEE.std_logic_1164.all;
use ieee.math_real.all;
use ieee.numeric_std.all;
use IEEE.std_logic_textio.all;
use std.textio.all;
 
entity testbench is
end testbench; 

architecture tb of testbench is

-- Signals
signal rst, iniciar, pronto, read_kernel, read_mem, write_mem_saida:  std_logic;
signal clk, finished: std_logic := '0';
signal end_kernel: std_logic_vector(3 downto 0);
signal data_mem_saida, data_mem_goldenmodel: std_logic_vector(7 downto 0);
signal data_kernel, data_mem, data_out: std_logic_vector(7 downto 0);
signal end_mem, end_mem_saida, end_goldenmodel, end_mem_saida_comp:  std_logic_vector(18 downto 0);

-- Components

    component kernel is
        port(
          ck, read_kernel : in  std_logic ;
          end_kernel   : in  std_logic_vector(3 downto 0);
           data : out std_logic_vector(7 downto 0)
        );
    end component;

    component mem is
        port(
        ck, read_mem : in  std_logic ;
        end_mem   : in  std_logic_vector(18 downto 0);
        data : out std_logic_vector(7 downto 0)
        );
    end component;

    component mem_goldenmodel is
      port(
        end_mem   : in  std_logic_vector(18 downto 0);
       data : out std_logic_vector(7 downto 0)
      );
    end component;

    component mem_saida is
        port(
          ck, write_mem_saida : in  std_logic;
          end_mem_saida   : in  std_logic_vector(18 downto 0);
            data : in std_logic_vector(7 downto 0);
            data_out: out std_logic_vector(7 downto 0)
        );
    end component;

    component topo is 
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

    end component;
    

CONSTANT period : TIME := 10 ns; 

begin

  m_inicial: mem port map(clk, read_mem, end_mem, data_mem);
  m_kernel: kernel port map(clk, read_kernel, end_kernel, data_kernel);
  m_said: mem_saida port map(clk, write_mem_saida, end_mem_saida, data_mem_saida, data_out);
  m_goldenmodel: mem_goldenmodel port map(end_goldenmodel, data_mem_goldenmodel);

  -- Connect DUV
  DUV: entity work.topo
  port map (
    clk, rst, iniciar,
    data_kernel, data_mem,
    pronto, read_kernel, read_mem, write_mem_saida,
    end_kernel, end_mem, end_mem_saida, data_mem_saida);

  clk <= not clk after period/2 when finished /= '1' else '0';
  test: process
  begin
	  rst <= '1';
	  iniciar <= '0';
	  wait for period;
	  rst <= '0';
	  wait for period;
	  iniciar <= '1';
	  wait for period;
	  iniciar <= '0';
	 
		wait until pronto'event and pronto = '1';

   wait for period;
	for i in 0 to 359999 loop
	  end_goldenmodel <= std_logic_vector(to_unsigned(i, 19));
	  end_mem_saida_comp <= std_logic_vector(to_unsigned(i, 19));
	  assert(data_out = data_mem_goldenmodel);
		report
			"Falha na simulacao."
		severity error;
	end loop;
	finished <= '1';
	assert false report "Test done." severity note;
	

  end process;

end tb;