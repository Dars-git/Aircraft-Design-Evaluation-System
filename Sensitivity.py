import numpy as np

Wp = 0.08553
def scoreM2(W, T, MAX):
    W = np.asarray(W)
    T = np.asarray(T)
    MAX = np.asarray(MAX)
    return 0 + ((W / T) / MAX)

def scoreM3 (W, n_l, E, MAX):
    W = np.asarray(W)
    n_l = np.asarray(n_l)
    E = np.asarray(E)
    MAX = np.asarray(MAX)   
    return 0 + (((np.floor(W / Wp) * np.floor(n_l)) / E) / MAX) 

def scoreGM(T, MIN):
    T = np.asarray(T)
    MIN = np.asarray(MIN)
    return MIN / T

def scoreU(W, T, n_l, E, T_GM, W_base, T_base, n_l_base, E_base, T_GM_base):
    W = np.asarray(W)
    T = np.asarray(T)
    W_base = np.asarray(W_base)
    T_base = np.asarray(T_base)
    n_l = np.asarray(n_l)
    n_l_base = np.asarray(n_l_base)
    E = np.asarray(E)
    E_base = np.asarray(E_base)
    T_GM = np.asarray(T_GM)
    T_GM_base = np.asarray(T_GM_base)

    M2 = scoreM2(W, T, scoreM2(W_base, T_base, 1))
    M3 = scoreM3(W, n_l, E, scoreM3(W_base, n_l_base, E_base, 1))
    GM = scoreGM(T_GM, T_GM_base)
    return (4 + M2 + M3 + GM)

