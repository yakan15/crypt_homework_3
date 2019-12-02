from shamir import *

def problem_B():
    n = 4
    t = 2
    q = 7
    secret_elements = [1,2,3,4]
    share_a = [0,4,1,5]
    share_b = [2,0,5,3] 
    # B-1
    ab = [a*b%7 for a,b in zip(share_a,share_b)]
    print("B-1 ab :", ab)
    # B-2
    share_c = [share(q, t, c, secret_elements) for c in ab]
    print("B-2 share_c :",share_c)
    # B3
    shared_c = np.array(share_c).T
    dist_d = []
    Q = [0,1,2,3]
    for shared in shared_c:
        lambda_i_Q = calc_lambda_i_Q(q, Q, shared, secret_elements)
        print("B-3 lambda_i,Q :", ", ".join(["lambda_({},Q)={}".format(i+1, x) for (i,x) in zip(Q, lambda_i_Q)]))
        dist_d.append(sum([s_i*_lambda for (s_i, _lambda) in zip(shared, lambda_i_Q)]) % q)
    # B-4
    print("d: ", dist_d)
    reconstructed = recon(7, [0,1], dist_d[:2], secret_elements)
    print("B-4 [ss'] : ",reconstructed)


if __name__ == "__main__":
    problem_B()