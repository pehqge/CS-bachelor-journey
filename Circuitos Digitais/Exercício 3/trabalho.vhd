library IEEE;
use IEEE.Std_Logic_1164.all;
use IEEE.std_logic_arith.all; 
use IEEE.std_logic_unsigned.all;


entity trabalho is
port (CLK, RST:  in std_logic;
      A, B:  out std_logic_vector(6 downto 0);
      min: out std_logic);
      
end trabalho;

architecture cont19 of trabalho is
  signal cnt: std_logic_vector(6 downto 0) := "0010011";
  signal m: std_logic := '0';
  
  component bin7seg99 is
    port (
        binaryin: in std_logic_vector (6 downto 0);
        hex1, hex0: out std_logic_vector (6 downto 0)
    );
    end component;
  
begin
    min <= m;
    process(CLK, RST)
	begin
		if (CLK'event and CLK = '1' and cnt = "0000001") then
             m <= '1';
        end if;
        if (CLK'event and CLK = '1' and cnt = "0000000") then
             m <= '0';
             cnt <= "0010011";
		elsif (CLK'event and CLK = '1') then
             cnt <= cnt - "0000001";
        end if;
	    if (RST = '0') then
	        cnt <= "0010011";
	    end if;
	end process;
	
	SEG7: bin7seg99 port map (cnt, A, B);

end cont19;

