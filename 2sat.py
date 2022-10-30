from typing import List, Set, Dict, Tuple, Optional


class SATLitteral:
    def __init__(self, a: int, na: bool, b: int, nb: bool):
        self.a = a
        self.na = na
        self.b = b
        self.nb = nb
    
    def get_val_names(self):
        return set([self.a, self.b])

    def __str__(self):
        str_na = "~" if self.na else ""
        str_nb = "~" if self.nb else ""
        return "("+str_na+str(self.a) + " U " + str_nb+str(self.b)+")"

class Graph:
    def __init__(self, n: int):
        self.n = n
        self.E: List[List[int]] = [[] for _ in range(n)]
        self.E_t: List[List[int]] = [[] for _ in range(n)]

    def add_edges(self, u: int, v: int):
        self.E[u].append(v)
        self.E_t[v].append(u)

    def dfs1(self, v, vis, order):
        vis[v] = True
        for u in self.E[v]:
            if not vis[u]:
                self.dfs1(u, vis, order)
        order.append(v)

    def dfs2(self, v, curr_comp, comp):
        comp[v] = curr_comp
        for u in self.E_t[v]:
            if comp[u] == -1:
                self.dfs2(u, curr_comp, comp)


    def compute_ssc(self):
        vis = [False]*self.n
        order = []

        for i in range(self.n):
            if not vis[i]:
                self.dfs1(i, vis, order)

        comp = [-1]*self.n
        curr_comp = 0
        for v in reversed(order):
            if comp[v] == -1:
                self.dfs2(v, curr_comp, comp)
                curr_comp += 1

        return comp
     
    
class SAT:
    def __init__(self, *args: SATLitteral):
        self.sat: List[SATLitteral] = list(args)
        self.m = len(self.sat)

    def __add__(self, other: 'SAT'):
        total_sat = self.sat + other.sat
        return SAT(*total_sat)

    def get_normalization_dict(self):
        all_var = set()
        for l in self.sat:
            all_var = all_var.union(l.get_val_names())
        new_names = {name:i for i, name in enumerate(list(all_var))}
        return new_names, len(all_var)

    
    def is_satisfible(self):
        new_names, n = self.get_normalization_dict()

        graph = Graph(2*n)

        for l in self.sat:
            if (not l.na) and (not l.nb):
                graph.add_edges(n + new_names[l.a], new_names[l.b])
                graph.add_edges(n + new_names[l.b], new_names[l.a])
            if (l.na) and (not l.nb):
                graph.add_edges(new_names[l.a], new_names[l.b])
                graph.add_edges(n + new_names[l.b], n + new_names[l.a])
            if (not l.na) and (l.nb):
                graph.add_edges(n + new_names[l.a],n + new_names[l.b])
                graph.add_edges(new_names[l.b], new_names[l.a])
            if (l.na) and (l.nb):
                graph.add_edges(new_names[l.a], n + new_names[l.b])
                graph.add_edges(new_names[l.b], n +  new_names[l.a])

        scc = graph.compute_ssc()

        for i in range(n):
            if scc[i] == scc[i + n]:
                return False
        return True

    def __str__(self):
        st = ""
        for l in self.sat:
            st += str(l) + " A "
        return st
