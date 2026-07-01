library IEEE;
use IEEE.std_logic_1164.all;
use ieee.math_real.all;
use ieee.numeric_std.all;
use IEEE.std_logic_textio.all;
use std.textio.all;
 
entity testebench is
end testebench; 

architecture tb of testebench is

signal mem_A, mem_B: std_logic_vector(31 downto 0);
signal SAD: std_logic_vector(13 downto 0);
signal end_mem: std_logic_vector(3 downto 0);
signal pronto,ler: std_logic;
signal reset, iniciar, ck, finished: std_logic := '0';



CONSTANT period : TIME := 20 ns;	 

begin

  -- Connect DUV
  DUV: entity work.topo
  port map (
    ck => ck,
    iniciar => iniciar,
    reset => reset,
    mem_A => mem_A,
    mem_B => mem_B,
    end_mem => end_mem,
    pronto => pronto,
    ler => ler,
    SAD => SAD
    
  );

  ck <= not ck after period/2;

	stim: process is
		file arquivo_de_estimulos : text open read_mode is "../../estimulos.dat";
		variable linha_de_estimulos: line;
		variable espaco: character;
		variable valor_mem_a: bit_vector(31 downto 0);
		variable valor_mem_b: bit_vector(31 downto 0);
		variable valor_de_saida: bit_vector(13 downto 0);
		begin

		while not endfile(arquivo_de_estimulos) loop
			iniciar <= '1';
			wait for period*2;
			iniciar <= '0';
			
			readline(arquivo_de_estimulos, linha_de_estimulos);
			for i in 1 to 16 loop
				read(linha_de_estimulos, valor_mem_a);
				read(linha_de_estimulos, espaco);
				read(linha_de_estimulos, valor_mem_b);
				
				Mem_A <= to_stdlogicvector(valor_mem_a);
				Mem_B <= to_stdlogicvector(valor_mem_b);
				
				wait for period*3;
			end loop;
			read(linha_de_estimulos, espaco);
			read(linha_de_estimulos, valor_de_saida);
			wait for period*3;
			assert (SAD = to_stdlogicvector(valor_de_saida))
			report
			"Sad incorreta! "
			severity error;
		end loop;

		wait for period;
		assert false report "Test done." severity note;
		wait;
	end process;
end tb;