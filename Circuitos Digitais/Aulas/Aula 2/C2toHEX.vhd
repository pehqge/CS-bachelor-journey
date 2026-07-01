library IEEE;
use IEEE.Std_Logic_1164.all;

entity C2toHEX is
port (G:  in std_logic_vector(3 downto 0);
      S:  out std_logic_vector(6 downto 0);
      N:  out std_logic_vector(6 downto 0));
end C2toHEX;

architecture decod of C2toHEX is
  signal C0,C1,C2: std_logic_vector(3 downto 0);
  
  component Compl2 is
   port (X: in std_logic_vector(3 downto 0);
         Y: out std_logic_vector(3 downto 0));
  end component;
  
  component bintodec is
   port (E: in std_logic_vector(3 downto 0);
         F: out std_logic_vector(6 downto 0));
  end component;
  
  component mux2x1 is
   port (A: in std_logic;
         B: in std_logic_vector(3 downto 0);
         C: in std_logic_vector(3 downto 0);
         D: out std_logic_vector(3 downto 0));
  end component;
  
begin 
      S <= (not G(3))&"111111";
      CO2: Compl2 port map (G, C0);
      MUX: mux2x1 port map (G(3), G, C0, C1);
      BTD: bintodec port map (C1, N);
end decod;
