from shamir import *


def problem_D():
    q = 11
    n = 9
    t = 3
    Q = list(range(9))
    secret_elements = [1,2,3,4,5,6,7,8,9]
    SQ_error = [4,10,1,10,4,5,2,8,7]
    
    lambda_i_Q = calc_lambda_i_Q(q, Q, SQ_error, secret_elements)
    print("D-1 lambda_i,Q :", ", ".join(["lambda_({},Q)={}".format(i+1, x) for (i,x) in zip(Q, lambda_i_Q)]))
    
    reconstructed = sum([s_i*_lambda for (s_i, _lambda) in zip(SQ_error, lambda_i_Q)]) % q
    print("D-1 Reconstruct エラー修正前 : ", reconstructed)
    
    ne = 2
    matrix = [[int(math.pow(x, i)) % 11 for i in range(ne+t)] + [int(math.pow(11, i)-math.pow(x, i) * y) % 11 for i in range(1, ne+1)] 
              for (x, y) in zip(secret_elements, SQ_error)]  
    print("matrix :")
    print(np.array(matrix))
    
    result = row_reduction(q, matrix, SQ_error)
    print(result)
    coef_f0 = [x[-1] for x in result[:ne+t]]
    coef_f1 = [x[-1] for x in result[ne+t:]]
    coef_f = calc_fx(q, coef_f0, coef_f1)
    SQ_fixed = [sum([pow(alpha, i) * coef for (i, coef) in enumerate(coef_f)]) % q
     for alpha in range(1,10)]
    print("coef 0", coef_f0)
    print("coef 1", coef_f1)
    print("coef fx", coef_f)
#     SQ_fixed = [calc_fx(q, corr_f0, corr_f1, i) for i in range(1, 10)]
    print("D-2 SQ エラー修正後 : ", SQ_fixed)
    
    reconstructed = recon(q, Q, SQ_fixed, secret_elements)
    print("D-2 Reconstructed エラー修正後 : ", reconstructed)


if __name__ == "__main__":
    problem_D()