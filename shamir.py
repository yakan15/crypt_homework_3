import random
import numpy as np
import math

def calc_inv(q):
    # Z/qZにおける各元の逆元を計算量O(q^2)で求める。
    return [[y for y in range(1,q+1) if y*x%q==1][0] for x in range(1,q)]

def create_secret_element(q, n):
    # Z/qZから要素をn個抽出する
    return random.sample(list(range(1, q)), k=n) 

def create_random_element(q, t):
    # Z/qZから重複を許してt個抽出する
    return random.choices(list(range(0, q)), k=t)

def create_share_function(q, t, secret):
    # Z/qZ上の秘密の多項式fを生成し、その各係数の配列を返す。
    coefficients = [secret]
    coefficients.extend(create_random_element(q, t-1))
#     print("Secret Function:"," + ".join(["{}X^{}".format(a, idx) for (idx, a) in enumerate(coefficients)]))
    return coefficients

def share(q, t, s, secret_elements):
    # q 有限体Fの要素数
    # t 秘密の復元に必要な人数
    # s 秘密 in F
    # secret_elements 予め決めておいた相異なるn個の要素 in F
    coef = create_share_function(q, t, s)
    return [calc_share_value(q, alpha, coef) for alpha in secret_elements]

def calc_share_value(q, alpha, coef):
    # 各シェアを計算する。
    return sum([a_i * alpha ** i for i, a_i in enumerate(coef)]) % q

def calc_lambda_i_Q(q, Q, SQ, secret_elements):
    # lambda_i,Qを計算する。
    inv_zqz = calc_inv(q)
    return [np.array([alpha_j * inv_zqz[(q + alpha_j - alpha_i) % q - 1]
                        for (idx, alpha_j) in enumerate(secret_elements) if idx in Q and idx != i]).prod() % q
                    for (i, alpha_i) in enumerate(secret_elements) if i in Q]

def recon(q, Q, SQ, secret_elements):
    # 集まった秘密の集合から基の値を復元する。
    # Q 集まった秘密のindex
    # SQ 集まった秘密
    # secret_elements 予め決めておいた相異なるn個の要素 in F
    lambda_i_Q = calc_lambda_i_Q(q, Q, SQ, secret_elements)
    return sum([s_i*_lambda for (s_i, _lambda) in zip(SQ, lambda_i_Q)]) % q

def calc_fx(q, _coef_f0, _coef_f1):
    # f(X) = f_0(X) / f_1(X) の係数を計算する。
    coef_f0 = _coef_f0[:]
    coef_f1 = [1]+_coef_f1[:]
    coef_f0.reverse()
    coef_f1.reverse()
    while coef_f0[0] == 0:
        coef_f0.pop(0)
    while coef_f1[0] == 0:
        coef_f1.pop(0)
    cur = 0
    inv_q = calc_inv(q)
    coef_f = []
    while cur + len(coef_f1) <= len(coef_f0):
        mul = coef_f0[cur] * inv_q[coef_f1[0]-1] % q
        coef_f.append(mul)
        for i in range(len(coef_f1)):
            coef_f0[cur+i] = (q*q + coef_f0[cur+i] - coef_f1[i] * mul) % q
        cur += 1
    coef_f.reverse()
    return coef_f

def row_reduction(q,mat,b):
    # 掃き出し法に則って連立方程式の解を計算する。
    inv_q = calc_inv(q)
    _mat = np.append(np.array(mat), [[v] for v in b], axis=1)
    assert(_mat.shape[0] >= _mat.shape[1]-1)
    for i in range(min(_mat.shape[0]-1, _mat.shape[1]-1)):
        if _mat[i][i] == 0:
            for j in range(i+1, _mat.shape[0]):
                if _mat[j][i] != 0:
                    tmp = _mat[i].copy()
                    _mat[i] = _mat[j]
                    _mat[j] = tmp
                    break
                elif j==_mat.shape[0]-1:
                    return _mat
                    assert(False)
        divisor = inv_q[_mat[i][i]-1]
        for j in range(_mat.shape[1]):
            _mat[i][j] = _mat[i][j] * divisor % q
        for j in range(_mat.shape[0]):
            mul = _mat[j][i]
            if i != j and mul != 0:
                for k in range(_mat.shape[1]):
                    _mat[j][k] = (q*q + _mat[j][k] - mul * _mat[i][k]) % q
    return _mat