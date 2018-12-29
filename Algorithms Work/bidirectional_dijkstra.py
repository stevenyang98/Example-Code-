def bidirectional_dijkstra(Adj, w, s, t):
    """
    Return a list of vertices forming a shortest path from s to t 
    Vertices are all integers in range(len(Adj))
    Input:  Adj: undirected graph, Adj[v] is list of vertices adjacent to v
              w: weight dictionary, w[(u,v)] is integer weight of edge (u,v)
              s: source vertex
              t: target vertex
    """
    path = []
    parent_s = [None] * len(Adj)
    parent_t = [None] * len(Adj)
    parent_s[s] = s
    parent_t[t] = t
    d_s = [float("inf")] * len(Adj)
    d_t = [float("inf")] * len(Adj)
    d_s[s] = 0
    d_t[t] = 0
    Q_s = PriorityQueue()
    Q_t = PriorityQueue()
    Q_s.insert(s,0)
    Q_t.insert(t,0) #process these two before
    v_star = s #initialize v_star
    visited = set()

    while len(Q_s.A) and len(Q_t.A) > 0: #running single djikstra for this atm
        q_t_search = False
        if min(Q_s.find_min(), Q_t.find_min()) > d_s[v_star]/2 + d_t[v_star]/2:
            break
        if Q_s.find_min() > Q_t.find_min():
            u = Q_t.extract_min()
            q_t_search = True
        else:
            u = Q_s.extract_min() #choosen which one to extract
        visited.add(u)
        if q_t_search: #chooses which parent to modify and how to modify the queue
            for v in Adj[u]:
                if v not in visited:
                    if d_t[v] > d_t[u] + w[(u, v)]:
                        d_t[v] = d_t[u] + w[(u, v)]
                        parent_t[v] = u
                        if v in Q_t.label2idx:
                            Q_t.decrease_key(v, d_t[v])
                        Q_t.insert(v, d_t[v])
                        if d_t[v_star] + d_s[v_star] > d_t[v] + d_s[v]:
                            v_star = v
        else:
            for v in Adj[u]:
                if v not in visited:
                    if d_s[v] > d_s[u] + w[(u, v)]:
                        d_s[v] = d_s[u] + w[(u, v)]
                        parent_s[v] = u
                        if v in Q_s.label2idx:
                            Q_s.decrease_key(v, d_s[v])
                        Q_s.insert(v, d_s[v])
                        if d_t[v_star] + d_s[v_star] > d_t[v] + d_s[v]:
                            v_star = v
    v_star_old = v_star
    while parent_s[v_star] != v_star:
        path.append(v_star)
        v_star = parent_s[v_star]
    path.append(s)
    path.reverse()

    while parent_t[v_star_old] != v_star_old:
        v_star_old = parent_t[v_star_old]
        path.append(v_star_old)
    return path


def relax(A, w, d, parent, u, v):
    if d[v] > d[u] + w[(u, v)]:
        d[v] = d[u] + w[(u, v)]
        parent[v] = u


class Item:
    def __init__(self, label, key):
        self.label, self.key = label, key

class PriorityQueue:                      # Binary Heap Implementation
    def __init__(self):                   # stores keys with unique labels
        self.A = []
        self.label2idx = {}

    def min_heapify_up(self, c):            
        if c == 0: return
        p = (c - 1) // 2
        if self.A[p].key > self.A[c].key:   
            self.A[c], self.A[p] = self.A[p], self.A[c]         
            self.label2idx[self.A[c].label] = c
            self.label2idx[self.A[p].label] = p
            self.min_heapify_up(p)         

    def min_heapify_down(self, p):          
        if p >= len(self.A): return
        l = 2 * p + 1
        r = 2 * p + 2
        if l >= len(self.A): l = p
        if r >= len(self.A): r = p
        c = l if self.A[r].key > self.A[l].key else r 
        if self.A[p].key > self.A[c].key:             
            self.A[c], self.A[p] = self.A[p], self.A[c]         
            self.label2idx[self.A[c].label] = c
            self.label2idx[self.A[p].label] = p
            self.min_heapify_down(c)       

    def insert(self, label, key):         # insert labeled key
        self.A.append(Item(label, key))
        idx = len(self.A) - 1
        self.label2idx[self.A[idx].label] = idx
        self.min_heapify_up(idx)

    def find_min(self):                   # return minimum key
        return self.A[0].key

    def extract_min(self):                # remove a label with minimum key
        self.A[0], self.A[-1] = self.A[-1], self.A[0]
        self.label2idx[self.A[0].label] = 0
        del self.label2idx[self.A[-1].label]
        min_label = self.A.pop().label
        self.min_heapify_down(0)
        return min_label

    def decrease_key(self, label, key):   # decrease key of a given label
        if label in self.label2idx:
            idx = self.label2idx[label]
            if key < self.A[idx].key:
                self.A[idx].key = key
                self.min_heapify_up(idx)
