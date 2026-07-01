library IEEE;
use IEEE.Std_Logic_1164.all;
entity somador is
port (A,B: in std_logic_vector(3 downto 0);
      S: out std_logic_vector(4 downto 0));
end somador;
architecture soma4 of somador is
 signal C0,C1,C2: std_logic;
 component halfadder is
  port (A: in std_logic;
        B: in std_logic;
        S: out std_logic;
        Cout: out std_logic);
 end component; 
 component fulladder is
  port (A: in std_logic;
        B: in std_logic;
        Cin: in std_logic;
        S: out std_logic;
        Cout: out std_logic);
 end component;
begin
 HA: halfadder port map (A => A(0),
                         B => B(0),
                         S => S(0),
                         Cout => C0);
 FA1: fulladder port map (A => A(1),
                          B => B(1), 
                          Cin => C0,
                          S => S(1),
                          Cout => C1);
 FA2: fulladder port map (A => A(2),
                          B => B(2), 
                          Cin => C1,
                          S => S(2),
                          Cout => C2);
 FA3: fulladder port map (A => A(3),
                          B => B(3), 
                          Cin => C2,
                          S => S(3),
                          Cout => S(4)); 
end soma4;
