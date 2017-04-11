import sys

# I use tree data structure to represent formula
class FNode:
    def __init__(self, val):
        self.v = val
        self.l = None
        self.r = None

# This class contains all the functions. Most of them are declared as static functions
class Formula:
    def __init__(self, pol_not):
        self.polish = pol_not
        self.tree, _ = self.build_tree(0)
        self.cnf_list = []

    # This method performs following procedures
    # 1. Remove all equivalence expressions by changing a = b with (a > b) & (b > a)
    # 2. Remove all implications by changing a > b with -a | b
    # 3. Eliminate all non-literal negations using  De Morgan's Law
    # 4. Finally convert to CNF by recursively distributing (a & b) | c to (a | c) & (b | c)
    # 5. Convert formula tree into list of lists where each inner list is disjunction
    # 6. Print CNF in Polish Notation
    # 7. Print CNF in infix notation
    # 8. Decide whether CNF is valid
    def to_cnf(self):
        Formula.eq_free(self.tree)
        Formula.impl_free(self.tree)
        self.tree = Formula.nnf(self.tree)
        self.tree = Formula.cnf(self.tree)
        Formula.cnf_to_list(self.tree, self.cnf_list, True)
        self.print_polish()
        self.print_cnf()
        self.is_valid()

    # Uses CNF list to print cnf in infix notation
    def print_cnf(self):
        pr = []
        for c in self.cnf_list:
            s = ' | '.join(c)
            if len(c) > 1 and len(self.cnf_list) > 1:
                s = '('+s+')'
            pr.append(s)
        res = ' & '.join(pr)
        print(res)

    # Recursively builds tree from input polish notation. Each node contains either literal or operation.
    # Each operation node has two children for two operands. For negation, only left child is used.
    def build_tree(self, idx=0):
        if len(self.polish) <= idx:  # empty
            return None, len(self.polish)
        elif not Formula.is_op(self.polish[idx]):  # literal
            return FNode(self.polish[idx]), idx + 1
        elif self.polish[idx] == '-':  # negation
            root = FNode(self.polish[idx])
            assert len(self.polish) > idx + 1
            root.l, n_idx = self.build_tree(idx + 1)
            return root, n_idx
        else:  # binary op
            root = FNode(self.polish[idx])
            root.l, r_idx = self.build_tree(idx + 1)
            root.r, n_idx = self.build_tree(r_idx)
            return root, n_idx

    # Prints the tree in polish notation It uses recursive static method to create list form tree.
    def print_polish(self):
        lst = []
        Formula.tree_to_list_polish(self.tree, lst)
        print(" ".join(lst))

    # Checks validity of CNF by inspecting each inner list of CNF list.
    # For every inner list (disjunction list) it searches for complimentary literals.
    def is_valid(self):
        print(self.cnf_list)
        for c in self.cnf_list:
            m = set()
            valid = False
            for d in c:
                if d[0] == '-' and d[2:] in m:
                    valid = True
                    break
                elif d[0] != '-' and ('- ' + d) in m:
                    valid = True
                    break
                else:
                    m.add(d)
            if not valid:
                print('Not Valid')
                return
        print('Valid')
        return

    # checks if argument is an operator
    @staticmethod
    def is_op(x):
        if x in ['&', '|', '>', '<', '=', '-']:
            return True
        return False

    # converts tree into polish list. argument 'lst' should be empty
    @staticmethod
    def tree_to_list_polish(root, lst):
        if root is None:
            return
        lst.append(root.v)
        Formula.tree_to_list_polish(root.l, lst)
        Formula.tree_to_list_polish(root.r, lst)
        return

    # converts tree into polish list. argument 'lst' should be empty
    @staticmethod
    def tree_to_list_infix(root, lst):
        if root is None:
            return
        if root.v == '-':
            lst.append(root.v)
            Formula.tree_to_list_infix(root.l, lst)
            return
        if Formula.is_op(root.v) and root.v != '-':
            lst.append('(')
        Formula.tree_to_list_infix(root.l, lst)
        lst.append(root.v)
        Formula.tree_to_list_infix(root.r, lst)
        if Formula.is_op(root.v) and root.v != '-':
            lst.append(')')
        return

    # return a copy of tree starting at the root
    @staticmethod
    def copy_tree(root):
        if root is None:
            return None
        new_r = FNode(root.v)
        new_r.l = Formula.copy_tree(root.l)
        new_r.r = Formula.copy_tree(root.r)
        return new_r

    # remove all equivalences changing a = b with (a > b) and (b > a)
    @staticmethod
    def eq_free(root):
        if root is None or not Formula.is_op(root.v):
            return
        elif root.v == '=':
            print(root.l.v, root.r.v)
            Formula.eq_free(root.l)
            Formula.eq_free(root.r)
            copy_l = Formula.copy_tree(root.l)
            copy_r = Formula.copy_tree(root.r)
            root.v = '&'
            nl = FNode('>')
            nr = FNode('>')
            nl.l = root.l
            nl.r = root.r
            nr.l = copy_r
            nr.r = copy_l
            root.l = nl
            root.r = nr
            return
        elif root.v == '-':
            Formula.eq_free(root.l)
            return
        else:
            Formula.eq_free(root.l)
            Formula.eq_free(root.r)
        return

    # Remove all implications by changing a > b with -a | b
    @staticmethod
    def impl_free(root):
        if root is None or not Formula.is_op(root.v):
            return
        elif root.v == '>':
            Formula.impl_free(root.l)
            Formula.impl_free(root.r)
            root.v = '|'
            new_l = FNode('-')
            new_l.l = root.l
            root.l = new_l
            return
        elif root.v == '<':
            Formula.impl_free(root.l)
            Formula.impl_free(root.r)
            root.v = '|'
            new_r = FNode('-')
            new_r.l = root.r
            root.r = new_r
            return
        elif root.v == '-':
            Formula.impl_free(root.l)
            return
        else:
            Formula.impl_free(root.l)
            Formula.impl_free(root.r)
        return

    # Eliminate all non-literal negations using  De Morgan's Law
    @staticmethod
    def nnf(root):
        if root is None or not Formula.is_op(root.v):
            return root
        elif root.v == '-' and root.l.v == '-':
            return Formula.nnf(root.l.l)
        elif root.v == '-' and root.l.v == '&':
            root.v = '|'
            new_l = FNode('-')
            new_l.l = root.l.l
            new_r = FNode('-')
            new_r.l = root.l.r
            root.l = new_l
            root.r = new_r
            return Formula.nnf(root)
        elif root.v == '-' and root.l.v == '|':
            root.v = '&'
            new_l = FNode('-')
            new_l.l = root.l.l
            new_r = FNode('-')
            new_r.l = root.l.r
            root.l = new_l
            root.r = new_r
            return Formula.nnf(root)
        elif root.v == '-':
            return root
        else:
            root.l = Formula.nnf(root.l)
            root.r = Formula.nnf(root.r)
            return root

    # recursively distribute (a & b) | c to (a | c) & (b | c)
    @staticmethod
    def distr(f1, f2):
        if f1.v == '&':
            new_node = FNode('&')
            new_node.l = Formula.distr(f1.l, f2)
            new_node.r = Formula.distr(f1.r, f2)
            return new_node
        if f2.v == '&':
            new_node = FNode('&')
            new_node.l = Formula.distr(f1, f2.l)
            new_node.r = Formula.distr(f1, f2.r)
            return new_node
        else:
            new_node = FNode('|')
            new_node.l = f1
            new_node.r = f2
            return new_node

    # convert to CNF using distr method
    @staticmethod
    def cnf(root):
        if root is None:
            return root
        elif root.v == '&':
            root.l = Formula.cnf(root.l)
            root.r = Formula.cnf(root.r)
            return root
        elif root.v == '|':
            root.l = Formula.cnf(root.l)
            root.r = Formula.cnf(root.r)
            return Formula.distr(root.l, root.r)
        else:
            return root

    # Convert formula tree into list of lists where each inner list is disjunction
    # Input tree is not changed
    @staticmethod
    def cnf_to_list(root, lst, conj=True):
        if root.v is None:
            return
        elif not Formula.is_op(root.v):
            if conj:
                lst.append([root.v])
            else:
                lst.append(root.v)
        elif root.v == '-':
            if conj:
                lst.append(['- ' + root.l.v])
            else:
                lst.append('- ' + root.l.v)
        elif root.v == '&':
            Formula.cnf_to_list(root.l, lst, True)
            Formula.cnf_to_list(root.r, lst, True)
        else:
            if conj:
                new_lst = []
                Formula.cnf_to_list(root.l, new_lst, False)
                Formula.cnf_to_list(root.r, new_lst, False)
                lst.append(new_lst)
            else:
                Formula.cnf_to_list(root.l, lst, False)
                Formula.cnf_to_list(root.r, lst, False)


polish = sys.argv[1]
polish = polish.split()
form = Formula(polish)
form.to_cnf()
