library IEEE;
use IEEE.Std_Logic_1164.all;

entity tarefa1 is
port (D, CLK:  in std_logic;
      Q0, Q1, Q2, Q3:  out std_logic);
end tarefa1;

architecture regs of tarefa1 is
  signal D1, D2, D3, S: std_logic;
  
  component D_FF is 
  port (CLK: in std_logic;
        D: in std_logic;
      	Q: out std_logic );
  end component;
  
begin
      FF1: D_FF port map (CLK, D, D1);
      FF2: D_FF port map (CLK, D1, D2);
      FF3: D_FF port map (CLK, D2, D3);
      FF4: D_FF port map (CLK, D3, S);
      Q0 <= D1;
      Q1 <= D2;
      Q2 <= D3;
      Q3 <= S;
end regs;
