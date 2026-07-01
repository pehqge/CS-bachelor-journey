library IEEE;
use IEEE.Std_Logic_1164.all;
entity mult3 is
port (X: in std_logic_vector(3 downto 0);
      Y: out std_logic_vector(4 downto 0) );
end mult3;

architecture mult3arch of mult3 is
 signal S: std_logic_vector(4 downto 0);
 component somador is
  port (A,B: in std_logic_vector(3 downto 0);
        S: out std_logic_vector(4 downto 0) );
 end component; 
begin
 SUM1: somador port map (A => X, 
                         B => X, 
                         S => S);
 SUM2: somador port map (A => X, 
                         B => S(3 downto 0), 
                         S => Y);
end mult3arch;
