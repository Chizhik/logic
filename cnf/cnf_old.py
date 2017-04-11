import sys

# TODO: handle '='
class FNode:
    def __init__(self, val):
        self.v = val
        self.l = None
        self.r = None

polish = sys.argv[1]
polish = polish.split()
print(polish)


def is_op(x):
    if x in ['&', '|', '>', '<', '=', '-']:
        return True
    return False

# print(is_op(polish[0]))


def build_tree(f, idx):
    if len(f) <= idx:   # empty
        return None, len(f)
    elif not is_op(f[idx]):     # literal
        return FNode(f[idx]), idx+1
    elif f[idx] == '-':    # negation
        root = FNode(f[idx])
        assert len(f) > idx + 1
        root.l, n_idx = build_tree(f, idx+1)
        return root, n_idx
    else:   # binary op
        root = FNode(f[idx])
        root.l, r_idx = build_tree(f, idx+1)
        root.r, n_idx = build_tree(f, r_idx)
        return root, n_idx


def tree_to_list_polish(root, lst):
    if root is None:
        return
    lst.append(root.v)
    tree_to_list_polish(root.l, lst)
    tree_to_list_polish(root.r, lst)
    return


def tree_to_list_infix(root, lst):
    if root is None:
        return
    if root.v == '-':
        lst.append(root.v)
        tree_to_list_infix(root.l, lst)
        return
    if is_op(root.v) and root.v != '-':
        lst.append('(')
    tree_to_list_infix(root.l, lst)
    lst.append(root.v)
    tree_to_list_infix(root.r, lst)
    if is_op(root.v) and root.v != '-':
        lst.append(')')
    return

my_tree, _ = build_tree(polish, 0)
test1 = []
tree_to_list_infix(my_tree, test1)
print(" ".join(test1))


def impl_free(root):
    if root is None or not is_op(root.v):
        return
    elif root.v == '>':
        impl_free(root.l)
        impl_free(root.r)
        root.v = '|'
        new_l = FNode('-')
        new_l.l = root.l
        root.l = new_l
        return
    elif root.v == '<':
        impl_free(root.l)
        impl_free(root.r)
        root.v = '|'
        new_r = FNode('-')
        new_r.l = root.r
        root.r = new_r
        return
    elif root.v == '-':
        impl_free(root.l)
        return
    else:
        impl_free(root.l)
        impl_free(root.r)
    return

impl_free(my_tree)
test2 = []
tree_to_list_infix(my_tree, test2)
print(" ".join(test2))


def nnf(root):
    if root is None or not is_op(root.v):
        return root
    elif root.v == '-' and root.l.v == '-':
        return nnf(root.l.l)
    elif root.v == '-' and root.l.v == '&':
        root.v = '|'
        new_l = FNode('-')
        new_l.l = root.l.l
        new_r = FNode('-')
        new_r.l = root.l.r
        root.l = new_l
        root.r = new_r
        return nnf(root)
    elif root.v == '-' and root.l.v == '|':
        root.v = '&'
        new_l = FNode('-')
        new_l.l = root.l.l
        new_r = FNode('-')
        new_r.l = root.l.r
        root.l = new_l
        root.r = new_r
        return nnf(root)
    elif root.v == '-':
        return root
    else:
        root.l = nnf(root.l)
        root.r = nnf(root.r)
        return root

my_tree = nnf(my_tree)
test3 = []
tree_to_list_infix(my_tree, test3)
print(" ".join(test3))


def distr(f1, f2):
    if f1.v == '&':
        new_node = FNode('&')
        new_node.l = distr(f1.l, f2)
        new_node.r = distr(f1.r, f2)
        return new_node
    if f2.v == '&':
        new_node = FNode('&')
        new_node.l = distr(f1, f2.l)
        new_node.r = distr(f1, f2.r)
        return new_node
    else:
        new_node = FNode('|')
        new_node.l = f1
        new_node.r = f2
        return new_node


def cnf(root):
    if root is None:
        return root
    elif root.v == '&':
        root.l = cnf(root.l)
        root.r = cnf(root.r)
        return root
    elif root.v == '|':
        root.l = cnf(root.l)
        root.r = cnf(root.r)
        return distr(root.l, root.r)
    else:
        return root

my_tree = cnf(my_tree)
test4 = []
tree_to_list_polish(my_tree, test4)
print(" ".join(test4))


def cnf_to_list(root, lst, conj=True):
    if root.v is None:
        return
    elif not is_op(root.v):
        if conj:
            lst.append([root.v])
        else:
            lst.append(root.v)
    elif root.v == '-':
        if conj:
            lst.append(['- '+root.l.v])
        else:
            lst.append('- '+root.l.v)
    elif root.v == '&':
        cnf_to_list(root.l, lst, True)
        cnf_to_list(root.r, lst, True)
    else:
        if conj:
            new_lst = []
            cnf_to_list(root.l, new_lst, False)
            cnf_to_list(root.r, new_lst, False)
            lst.append(new_lst)
        else:
            cnf_to_list(root.l, lst, False)
            cnf_to_list(root.r, lst, False)

test5 = []
cnf_to_list(my_tree, test5)
print(test5)


def print_cnf(lst):
    pr = []
    for c in lst:
        pr.append(' | '.join(c))
    res = ') & ('.join(pr)
    if len(lst) > 1:
        print('(%s)' % res)
    else:
        print(res)

print_cnf(test5)


def is_valid(lst):
    for c in lst:
        m = dict()
        valid = False
        for d in c:
            if d[0] == '-' and d[2:0] in m:
                valid = True
                break
            elif d[0] != '-' and ('- '+d) in m:
                valid = True
                break
        if not valid:
            print('Not Valid')
            return
    print('Valid')
    return

is_valid(test5)