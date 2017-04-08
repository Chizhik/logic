import subprocess

f = open("nonogram.in", "r")
n = int(f.readline())
m = int(f.readline())
conjs = []
next_free_idx = n*m + 1
# n - number of rows
for i in range(n):
    clue = list(map(int, (f.readline().split())))
    # number of additional atoms for each number in clue
    c_atoms = n - sum(clue) - len(clue) + 2
    # Part 1
    for j in range(len(clue)):
        # for each number in clue at least one of its additional atoms is True
        conjs.append(' '.join([str(k) for k in range(next_free_idx + j * c_atoms, next_free_idx + (j + 1) * c_atoms)]))
    # Part 2
    for j in range(len(clue)):
        # for each number in clue at most one of its additional atoms is True
        for k in range(next_free_idx+j*c_atoms, next_free_idx+(j+1)*c_atoms):
            for l in range(k+1, next_free_idx+(j+1)*c_atoms):
                conjs.append('-'+str(k)+' -'+str(l))
    # Part 3
    for j in range(len(clue)-1):
        offset = next_free_idx+ j * c_atoms
        # if atom[offset+k] is True then atom[offset+c_atoms+k] or atom[offset+c_atoms+k+1] or ...
        # we can ignore atom[offset] because atom[offset+c_atoms] or atom[offset+c_atoms+1] or ... is already in part 1
        for k in range(1, c_atoms):
            conjs.append('-' + str(offset+k) + ' ' + ' '.join([str(offset + c_atoms + l) for l in range(k, c_atoms)]))
        # there is no need to do same things backwards because of part 1 (exactly one is true)
    # Part 4
    for j in range(m):
        # In this part we relate square atoms with our additional atoms
        corr = []
        s = 1
        # following loop can be optimized
        for idx, v in enumerate(clue):
            e = s+v-1
            for k in range(c_atoms):
                if e+k >= j+1 >= s+k:
                    corr.append(str(next_free_idx + idx * c_atoms + k))
            s = e+2
        # atom[i*m+j] is True if and only if disjunction of corresponding additional atoms is True
        conjs.append('-'+str(i*m+j+1)+' '+' '.join(corr))
        for x in corr:
            conjs.append(str(i*m+j+1)+' -'+x)
    next_free_idx += c_atoms * len(clue)
# m - number of columns
for i in range(m):
    clue = list(map(int, (f.readline().split())))
    # number of additional atoms for each number in clue
    c_atoms = m - sum(clue) - len(clue) + 2
    # Part 1
    for j in range(len(clue)):
        # for each number in clue at least one of its additional atoms is True
        conjs.append(' '.join([str(k) for k in range(next_free_idx + j * c_atoms, next_free_idx + (j + 1) * c_atoms)]))
    # Part 2
    for j in range(len(clue)):
        # for each number in clue at most one of its additional atoms is True
        for k in range(next_free_idx+j*c_atoms, next_free_idx+(j+1)*c_atoms):
            for l in range(k+1, next_free_idx+(j+1)*c_atoms):
                conjs.append('-'+str(k)+' -'+str(l))
    # Part 3
    for j in range(len(clue)-1):
        offset = next_free_idx+ j * c_atoms
        # if atom[offset+k] is True then atom[offset+c_atoms+k] or atom[offset+c_atoms+k+1] or ...
        # we can ignore atom[offset] because atom[offset+c_atoms] or atom[offset+c_atoms+1] or ... is already in part 1
        for k in range(1, c_atoms):
            conjs.append('-' + str(offset+k) +' ' +' '.join([str(offset + c_atoms + l) for l in range(k, c_atoms)]))
        # there is no need to do same things backwards because of part 1 (exactly one is true)
    # Part 4
    for j in range(n):
        # In this part we relate square atoms with our additional atoms
        corr = []
        s = 1
        for idx, v in enumerate(clue):
            e = s+v-1
            for k in range(c_atoms):
                if e+k >= j+1 >= s+k:
                    corr.append(str(next_free_idx + idx * c_atoms + k))
            s = e+2
        # atom[j*m+i] is True if and only if disjunction of corresponding additional atoms is True
        conjs.append('-'+str(j*m+i+1)+' '+' '.join(corr))
        for x in corr:
            conjs.append(str(j*m+i+1)+' -'+x)
    next_free_idx += c_atoms * len(clue)
f.close()
# prepare input for minisat
mf = open('minisat.in', 'w')
total_atoms = next_free_idx - 1
mf.write('p cnf ' + str(total_atoms) + ' ' + str(len(conjs)))
for c in conjs:
    mf.write('\n')
    mf.write(c)
    mf.write(' 0')
mf.close()

with open('minisat.result', 'w') as f:
    subprocess.call(['minisat', 'minisat.in', 'minisat.out'], stdout=f)

rf = open('minisat.out', 'r')
assert rf.readline() == 'SAT\n'
solution = rf.readline().split()
for i in range(n):
    res = []
    for j in range(m):
        if solution[i*m+j][0] == '-':
            res.append('.')
        else:
            res.append('#')
    print(' '.join(res))
rf.close()