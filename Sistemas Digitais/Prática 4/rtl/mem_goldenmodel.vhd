library ieee;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
use std.textio.all;
use ieee.std_logic_textio.all;

entity mem_goldenmodel is
  port(
    end_mem   : in  std_logic_vector(18 downto 0);
	 data : out std_logic_vector(7 downto 0)
  );
end mem_goldenmodel;

architecture rtl of mem_goldenmodel is
  type mem_type is array (0 to 359999) of std_logic_vector(7 downto 0);
  
  impure function inicializa(nome_do_arquivo : in string) return mem_type is
	  file     arquivo  : text open read_mode is nome_do_arquivo;
	  variable linha    : line;
	  variable temp_bv  : std_logic_vector(7 downto 0);
	  variable temp_mem : mem_type;
	  begin
		 for i in mem_type'range loop
			readline(arquivo, linha);
			read(linha, temp_bv);
			temp_mem(i) := temp_bv;
		 end loop;
		 return temp_mem;
  end;
	signal mem : mem_type := inicializa("matriz_filtrada.txt");

begin
  data <= mem(to_integer(unsigned(end_mem)));
  
end rtl;
