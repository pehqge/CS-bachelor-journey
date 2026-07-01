def rps(play1, play2):
    if play1 == "rock" and play2 == "scissors":
        return True
    elif play1 == "scissors" and play2 == "paper":
        return True
    elif play1 == "paper" and play2 == "rock":
        return True
    else:
        return False

while True:
    inputt = input()
    
    if inputt == "0":
        break
    
    n, k = map(int, inputt.split())
    
    total = k*n*(n-1)/2

    players = [0]*(n+1)

    for _ in range(k):
        player1, play1, player2, play2 = input().split()
        
        if rps(play1, play2):
            players[int(player1)] += 1
        elif play1 == play2:
            total-=1
        else:
            players[int(player2)] += 1
            
    for i in range(n):
        if total == 0:
            print("-")
        else:
            print(f"{players[i+1]/total:.3f}" )
    print()
