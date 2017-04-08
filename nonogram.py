f = open("nonogram.in", "r")
n = int(f.readline())
m = int(f.readline())
print(n, m)
conjs = []
next_free_idx = n*m + 1
for i in range(n):
    rule = list(map(int, (f.readline().split())))
    print(rule)
    # number of additional variables for each number in rule
    r_vars = n - sum(rule) - len(rule) + 2
    print(r_vars)
    for j in range(len(rule)):
        # for each number in rule at least one of its additional variables is True
        conjs.append(' '.join([str(k) for k in range(next_free_idx+j*r_vars, next_free_idx+(j+1)*r_vars)]))
        # for each number in rule at most one of its additional variables is True
        for k in range(next_free_idx+j*r_vars, next_free_idx+(j+1)*r_vars):
            for l in range(k+1, next_free_idx+(j+1)*r_vars):
                conjs.append('-'+str(k)+' -'+str(l))
    next_free_idx += r_vars*len(rule)
print(conjs)