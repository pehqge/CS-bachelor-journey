library ieee;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
use std.textio.all;
use ieee.std_logic_textio.all;
-- use ieee.numeric_bit.all; 

entity mem is
  port(
    ck, read_mem : in  std_logic ;
    end_mem   : in  std_logic_vector(18 downto 0);
	 data : out std_logic_vector(7 downto 0)
  );
end mem;

architecture rtl of mem is
  type mem_type is array (0 to 362403) of std_logic_vector(7 downto 0);
  
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
	signal signal_mem : mem_type := inicializa("matriz.txt");

begin
  r: process(ck)
  begin
    if (ck='1' and ck'event) then
      if (read_mem='1') then
        data <= signal_mem(to_integer(unsigned(end_mem)));
      end if;
    end if;
  end process;
end rtl;
