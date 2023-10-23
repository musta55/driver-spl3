from collections import deque
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, vertex, edge):
        if vertex in self.graph:
            self.graph[vertex].append(edge)
        else:
            self.graph[vertex] = [edge]

    def bfs(self, start_vertex):
        visited = set()
        queue = deque([start_vertex])

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                print(vertex, end=' ')
                visited.add(vertex)
                neighbors = self.graph.get(vertex, [])
                queue.extend(neighbors)

# Example usage:
if __name__ == "__main__":
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.bfs('A')
