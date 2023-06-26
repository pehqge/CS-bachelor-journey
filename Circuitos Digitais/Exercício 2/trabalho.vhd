library IEEE;
use IEEE.Std_Logic_1164.all;

entity trabalho is
port (A: in std_logic;
      X: in std_logic_vector(7 downto 0);
      S1,S2,S3: out std_logic_vector(6 downto 0)
      );
end trabalho;

architecture conversor of trabalho is
    signal M2,D4,L: std_logic_vector(7 downto 0);
    signal BCD,BCDL,BCDK: std_logic_vector(11 downto 0);
    signal B1,B2,B3: std_logic_vector(3 downto 0);
            

    component soma8 is
    port (A:  in std_logic_vector(7 downto 0);
          B:  in std_logic_vector(7 downto 0); 
          S:  out std_logic_vector(7 downto 0)
          );
    end component;
    
    component div4 is
    port (A:  in std_logic_vector(7 downto 0);
          S:  out std_logic_vector(7 downto 0)
          );
    end component;
    
    component binbcd is
    port (bin_in: in std_logic_vector (7 downto 0);
          bcd_out: out std_logic_vector (11 downto 0)
          );
    end component;
    
    component bcd7seg is
    port (bcd_in:  in std_logic_vector(3 downto 0);
          out_7seg:  out std_logic_vector(6 downto 0)
          );
    end component;
    
    component mux2 is
    port (K:  in std_logic;
          KG: in std_logic_vector(11 downto 0);
          LBS: in std_logic_vector(11 downto 0);
          S:  out std_logic_vector(11 downto 0)
          );
    end component;

begin
    S8: soma8 port map (X, X, M2);
    DI4: div4 port map (X, D4);
    S28: soma8 port map (D4, M2, L);
    BBL: binbcd port map (L, BCDL);
    BBK: binbcd port map (X, BCDK);
    MUX: mux2 port map (A, BCDK, BCDL, BCD);
    B1 <=  BCD(3 downto 0);
    B2 <= BCD(7 downto 4);
    B3 <= BCD(11 downto 8);
    H1: bcd7seg port map (B1, S1);
    H2: bcd7seg port map (B2, S2);
    H3: bcd7seg port map (B3, S3);
end conversor;
    
    
    