def read_data():
    f = input()
    init = (f.rstrip('\n')).split(" ")
    N = int(init[0])
    S = int(init[1]) 
    T = int(init[2])
    P = float(init[3])
    pos = []
    v = []
    for i in range(1, N+1):
        f = input()
        particle = f.rstrip('\n').split(" ")
        pos.append(( float(particle[0]) , float( particle[1])))
        v.append(( float(particle[2]) , float( particle[3])))
    return N, S, T, P, pos, v

def calculate_time(v, pos):
    return (sum( [v[i][0]*pos[i][0] + v[i][1]*pos[i][1] for i in range(N)] )) / (sum( [v[i][0]*v[i][0] + v[i][1]*v[i][1] for i in range(N)] ))

sign = lambda x: (1, -1)[x<0]

def hit_time(S, v, p):
    return (S-sign(v)*p)/(v*sign(v))

def hit_time_wall(S, v,):
    return 2*S/(sign(v)*v)

def calculate_hits_particles(S, v, pos):
    Nhits = []
    for i in range(N):
        ni=0
        hitx = hit_time(S, v[i][0], pos[i][0])
        hity = hit_time(S, v[i][1], pos[i][1])
        if T > hitx: 
            ni += 1
        if T > hity: 
            ni += 1
        wtx = hit_time_wall(S,v[i][0])
        wty = hit_time_wall(S,v[i][1])
        if wtx <= (T-hitx): 
            ni += int(((T-hitx)/wtx)) 
        if wty <= (T-hity): 
            ni += int(((T-hity)/wty))
        Nhits.append(ni)
    return Nhits

if __name__ == '__main__':
    N, S, T, P, pos, v = read_data()
    time = calculate_time(v, pos)
    Nhits = calculate_hits_particles(S, v, pos)
    Probability = sum([P**(n) for n in Nhits])
    print(round(time), sum(Nhits), Probability)