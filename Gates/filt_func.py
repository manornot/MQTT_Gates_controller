def kalm_filt_iter(val,params):
    reac, var, Pc, G, P, Xp, Zp, Xe = params[:]
    Pc = P + reac
    G = Pc/(Pc + var)
    P = (1-G) * Pc
    Xp = Xe
    Zp = Xp
    Xe = G*(val - Zp) + Xp
    params = [reac, var, Pc, G, P, Xp, Zp, Xe]
    return [Xe,params]

def hist_th(val,up_th,down_th,state):
    if state:
        if val > down_th:
            return 1, state
        else: 
            state = 0
            return 0, state
    else:
        if val < up_th:
            return 0, state
        else:
            state = 1
            return 1, state


