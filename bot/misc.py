import random

# ================================================
# Discord name handling

def sanitize(string)
    string = re.sub(r'[^a-z0-9 ]', '', string, flags=re.IGNORECASE)
    return string.strip()

def split_discord_name(dname):
    m = re.match(r'^(.+)#([0-9]{4})$', dname)
    name = sanitize(m.group(1))
    discriminator = m.group(2)
    return name, discriminator

# ================================================
# Player statistics

def confidence(games):
    return games/(1+games)

def win_rate(games, wins):
    return wins/games

def p_value(games, wins):
    r = random.random()
    wr = winrate(games, wins)
    cf = confidence(games)
    l = max(0, wr-cf)
    u = min(1, wr+cf)
    return l + (u-l)*r

# ================================================
# Team balancing

def balance(L):
    assert len(L) % 2 == 0
    N = len(L)-1
    I = list(range(int((N-1)/2)))
    Iopt = I + [N]
    S = sum(L)
    while I:
        LL = L.copy()
        J = I + [N]
        J.reverse()
        s = sum([LL.pop(j) for j in J])
        s = abs(s - sum(LL))
        if s < S:
            S = s
            Iopt = I + [N]
        I = incr(I, N)
    A = Iopt.copy()
    J = list(range(N+1))
    Iopt.reverse()
    [J.pop(i) for i in Iopt]
    B = J.copy()
    return [A,B]

def incr(I, N):
    k = 1
    while k <= len(I):
        if I[-k]+k < N:
            return I[:-k] + [I[-k]+i+1 for i in range(k)]
        k += 1
    return False