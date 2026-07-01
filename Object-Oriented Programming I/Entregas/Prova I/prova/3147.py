#a batalha dos exercitos eh sobre um time (h, e, a) contra outro (o, w). Nisso, vence o que tiver mais quantidade. Sobre a aguia entrar no time, nao altera muito na logica do codigo, eh so somar junto com o time 1

h, e, a, o, w, x = map(int, input().split()) 
if h+e+a+x < o+w:
  print("Sauron has returned.")
else:
  print("Middle-earth is safe.")