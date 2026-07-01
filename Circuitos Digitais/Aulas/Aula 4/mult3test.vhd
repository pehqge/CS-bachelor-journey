library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
entity mult3test is
end mult3test;

architecture tb of mult3test is
    signal X : std_logic_vector(3 downto 0);
    signal Y : std_logic_vector(4 downto 0);
    signal cnt : std_logic_vector(3 downto 0) := "0000";
    
    component mult3 is port (
               X:  in std_logic_vector(3 downto 0);
               Y:  out std_logic_vector(4 downto 0));
    end component;
    
begin
    DUT : mult3 port map (X => X, Y => Y);
    X <= cnt;
    process 
        constant period: time := 10 ns;
            begin
                for k in 1 to 16 loop
                    wait for period;
                    cnt <= cnt + '1';
                end loop;
                wait;
 end process;
end tb;