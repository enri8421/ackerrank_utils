from heapq import heappop, heappush


def Dijkstra(n, s, G):
    """
    n: number of nodes in the graph
    s: index of source node
    G: adjacency list [[(v1,w1), ...],[(v1,w1,...],...]
    """
    dist = [-1 for _ in range(n)]
    dist[s] = 0
    vis = [False for _ in range(n)]
    Q = [(0, s)]
    while Q:
        _, v = heappop(Q)
        if vis[v]:
            continue
        vis[v] = True
        for u, w in G[v]:
            if (dist[v] + w < dist[u]) or (dist[u] < 0):
                dist[u] = dist[v] + w
                heappush(Q, (dist[u],u))
                
    return dist
