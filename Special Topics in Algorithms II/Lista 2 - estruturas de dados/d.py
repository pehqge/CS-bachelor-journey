while True:
    n = int(input())
    if n == 0:
        break
    discard = []
    
    cards = [x for x in range(1, n+1)]
    
    while len(cards) > 1:
        discard.append(cards.pop(0))
        cards.append(cards.pop(0))
    
    discarded_str = ', '.join(str(x) for x in discard)
    print(f"Discarded cards: {discarded_str}" if discard else "Discarded cards:")
    print(f"Remaining card: {cards[0]}")