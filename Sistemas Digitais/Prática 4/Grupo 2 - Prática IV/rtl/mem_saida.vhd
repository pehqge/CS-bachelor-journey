library ieee;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;

entity mem_saida is
  port(
    ck, write_mem_saida : in  std_logic;
    end_mem_saida   : in  std_logic_vector(18 downto 0);
	  data : in std_logic_vector(7 downto 0);
    data_out: out std_logic_vector(7 downto 0)
  );
end mem_saida;

architecture rtl of mem_saida is 
  type mem_type is array (0 to 359999) of std_logic_vector(7 downto 0);
	signal signal_mem_saida : mem_type;

begin
  data_out <= signal_mem_saida(to_integer(unsigned(end_mem_saida)));

  w: process(ck)
  begin
    if (ck='1' and ck'event) then
      if (write_mem_saida = '1') then
        signal_mem_saida(to_integer(unsigned(end_mem_saida))) <= data ;
      end if;
    end if;
  end process;
end rtl;
