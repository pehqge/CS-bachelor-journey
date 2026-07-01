while True:
    h, m = map(int,input().split(":"))
    if h == 0 and m == 0:
        break
    
    angleH = h * 30 + m * 0.5
    angleM = m * 6
    
    dif = abs(angleH - angleM)
    
    if dif > 180:
        dif = 360 - dif
    print(f"{dif:.3f}")