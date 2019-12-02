from shamir import *

def problem_A():
    q = 7
    s = 3
    n = 5
    t = 3
    coef = create_share_function(q, t, s)
    print("A-1 秘密の多項式f :", " + ".join(["{}X^{}".format(a, idx) for (idx, a) in enumerate(coef)]))
    secret_elements = create_secret_element(q, n)
    print("A-2 [alpha] :", secret_elements)
    shared = [calc_share_value(q, alpha, coef) for alpha in secret_elements]
    print("A-3 シェア[3](3,5) :", shared)
    Q = [0, 1, 2]
    SQ = shared[:3]
    lambda_i_Q = calc_lambda_i_Q(q, Q, SQ, secret_elements)
    print("A-4 lambda_i,Q :", ", ".join(["lambda_({},Q)={}".format(i+1, x) for (i,x) in zip(Q, lambda_i_Q)]))
    reconstructed = sum([s_i*_lambda for (s_i, _lambda) in zip(SQ, lambda_i_Q)]) % q
    print("A-5 s :", reconstructed)


if __name__ == "__main__":
    problem_A()
