from datetime import datetime, timedelta

t = int(input())

for i in range(t):
    data = datetime.strptime(input(), "%Y-%B-%d")
    
    add = int(input())
    
    resposta = data + timedelta(days=add)
    
    data_resposta = resposta.strftime("%Y-%B-%d")
    
    print(f"Case {i+1}: {data_resposta}")