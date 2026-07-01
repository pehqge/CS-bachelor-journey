library ieee;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
use std.textio.all;
use ieee.std_logic_textio.all;
-- use ieee.numeric_bit.all;

entity kernel is
  port(
    ck, read_kernel : in  std_logic ;
    end_kernel   : in  std_logic_vector(3 downto 0);
	 data : out std_logic_vector(7 downto 0)
  );
end kernel;

architecture rtl of kernel is
  type mem_type is array (0 to 8) of std_logic_vector(7 downto 0);
  
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
	signal signal_kernel : mem_type := inicializa("kernel.txt");

begin
  r: process(ck)
  begin
    if (ck='1' and ck'event) then
      if (read_kernel='1') then
        data <= signal_kernel(to_integer(unsigned(end_kernel)));
      end if;
    end if;
  end process;
end rtl;
