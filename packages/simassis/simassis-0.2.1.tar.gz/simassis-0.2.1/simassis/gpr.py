import numpy as np
from scipy.optimize import minimize


def gkm(x, sigma, l, K):
    k = np.zeros((K,K))
    for j in range(K):
        cd = (x - x[j])**2
        k[j,:] = sigma*np.exp(-np.sum(cd/(2*l*l), 1))
    return k

def gk(x1, x2, sigma, l, K, Pns):
    ks = np.zeros((K, Pns))
    for i in range(K):
        for j in range(Pns):
            cd = (x1[i,:] - x2[j,:])**2
            ks[i,j] = sigma*np.exp(-np.sum(cd/(2*l*l)))
    return ks

def _calc_alfa_pieces(X_t, N, K, Pn, sigma, l, se):
    #calculating L matrix - macierz sklaowania, K to liczba aotmów a N to liczba struiktur
    L = np.zeros((K, N))
    step = 0
    for n in range(N):
        L[step:step+Pn[n],n] = 1
        step = step + Pn[n]

    #    calculating covariance
    k = gkm(X_t, sigma, l, K)

    #calculating alpha
    alfa_braket = np.matmul(L.T, np.matmul(k, L))
    alfa_braket = alfa_braket + (se**2)*np.identity(len(alfa_braket))
    try:
        alfa_cholesky = np.linalg.cholesky(alfa_braket)
        alfa_cholesky_H = alfa_cholesky.T.conj()
        alfa_braket_inv = np.matmul(
            np.linalg.inv(alfa_cholesky_H),
            np.linalg.inv(alfa_cholesky)
            )
    except:
        print('cholesky decomposition failed')
        alfa_braket_inv = np.linalg.inv(alfa_braket)
    return alfa_braket, alfa_braket_inv, L

def calc_mlh(X_t, Y_l, N, K, Pn, sigma, l, se):
    alfa_braket, alfa_braket_inv, L = _calc_alfa_pieces(
        X_t, N, K, Pn,
        sigma, l, se,
        )
#    #minimise that!
    mlh =   (
            .5*np.log(np.abs(np.linalg.det(alfa_braket))) + 
            .5*np.matmul(Y_l.T, np.matmul(alfa_braket_inv, Y_l)) + 
            .5*len(alfa_braket)*np.log(2*np.pi)
            )
    return mlh

def calc_alfa(X_t, Y_t, N, K, Pn, sigma, l, se):
    alfa_braket, alfa_braket_inv, L = _calc_alfa_pieces(
        X_t, N, K, Pn,
        sigma, l, se,
        )
    alfa = np.matmul(
            L,
            np.matmul(alfa_braket_inv, Y_t),
            )
    return alfa, K

def mlh_function(X, X_t, Y_t, N, K, Pn):
    return calc_mlh(X_t, Y_t, N, K, Pn, np.abs(X[0]), np.abs(X[1]), np.abs(X[2]))

def hyperopt(X, Y, tr_split, hp0, min_type):   
    Pn = []
    for x in X:
        Pn.append(x.shape[0])
    Pn = np.array(Pn)
    
    X_all = []
    for x in X:
        for j in range(x.shape[0]):
            X_all.append(x[j,:])
    X_all = np.array(X_all)
    X_mean = np.mean(X_all, 0)
    X_std = np.std(X_all, 0)
    
    X_norm = []
    for x in X:
        X_norm.append((x-X_mean)/X_std)
        
    Y_mean = np.mean(Y)
    Y_std = np.std(Y)
    Y = (Y-Y_mean)/Y_std

    idx = np.arange(len(Y))
    np.random.shuffle(idx)
    idx_t = idx[:int(len(idx)*tr_split)]
    idx_v = idx[int(len(idx)*tr_split):]
    
    X_t_temp = []
    X_v = []
    for i in idx:
        if i in idx_t:
            X_t_temp.append(X_norm[i])
        else:
            X_v.append(X_norm[i])

    X_t = []
    for x in X_t_temp:
        for j in range(x.shape[0]):
            X_t.append(x[j,:])
    X_t = np.array(X_t)

    Y_t = Y[idx_t]
    Y_v = Y[idx_v]

    N = len(idx_t)
    K = X_t.shape[0]
    
    res = minimize(mlh_function, hp0, args=(X_t, Y_t, N, K, Pn[idx_t]), method=min_type)
    model = {}
    model['sucess'] = res.success
    model['sigma'] = res.x[0]
    model['l'] = res.x[1]
    model['se'] = res.x[2]
    
    model['X_t'] = X_t
    model['X_v'] = X_v
    model['Y_t'] = Y_t
    model['Y_v'] = Y_v
    
    model['N'] = N
    model['K'] = K
    model['Pn'] = Pn[idx_t]
    
    model['Y_mean'] = Y_mean
    model['Y_std'] = Y_std
    model['X_mean'] = X_mean
    model['X_std'] = X_std
    
    return model

def validation(model):
    alfa, K_t = calc_alfa(
        model['X_t'], model['Y_t'],
        model['N'], model['K'], model['Pn'],
        model['sigma'], model['l'], model['se'])

    Y_pr = []
    for i in range(len(model['X_v'])):
        K_v = model['X_v'][i].shape[0]
        ks = gk(model['X_t'], model['X_v'][i], model['sigma'], model['l'], model['K'], K_v)

        Y_pr_ = []
        for p in range(K_v):
            Y_pr_.append(np.sum(ks[:,p]*alfa[:]))
        Y_pr.append(np.sum(Y_pr_))
    Y_pr = np.array(Y_pr)
    
    Y_v = model['Y_v']*model['Y_std'] + model['Y_mean']
    Y_pr = Y_pr*model['Y_std'] + model['Y_mean']
    return Y_v, Y_pr

def prediction(model, X_p):
    X_p = (X_p-model['X_mean'])/model['X_std']
    alfa, K_t = calc_alfa(
        model['X_t'], model['Y_t'],
        model['N'], model['K'], model['Pn'],
        model['sigma'], model['l'], model['se'])

    Y_pr = []
    for i in range(len(X_p)):
        K_v = X_p[i].shape[0]
        ks = gk(model['X_t'], X_p[i], model['sigma'], model['l'], model['K'], K_v)

        Y_pr_ = []
        for p in range(K_v):
            Y_pr_.append(np.sum(ks[:,p]*alfa[:]))
        Y_pr.append(np.sum(Y_pr_))
    Y_pr = np.array(Y_pr)
    Y_pr = Y_pr*model['Y_std'] + model['Y_mean']
    return Y_pr
