class Node:
    def __init__(self, name):
        self.name = name
        self.routing_table = {name: (0, name)}  # Distanza a sé stesso è 0
        self.neighbors = {}

    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
        self.routing_table[neighbor.name] = (cost, neighbor.name)

    def update_routing_table(self):
        updated = False
        for neighbor, cost_to_neighbor in self.neighbors.items():
            for dest, (cost_to_dest, next_hop) in neighbor.routing_table.items():
                new_cost = cost_to_neighbor + cost_to_dest
                if dest not in self.routing_table or new_cost < self.routing_table[dest][0]:
                    self.routing_table[dest] = (new_cost, neighbor.name)
                    updated = True
        return updated

    def print_routing_table(self):
        print(f"Routing Table for Node {self.name}")
        print("Destination | Cost | Next Hop")
        for dest, (cost, next_hop) in sorted(self.routing_table.items()):
            print(f"{dest:^11} | {cost:^4} | {next_hop:^8}")
        print("-" * 30)


def initialize_network_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Numero di nodi
    num_nodes = int(lines[0].strip())
    nodes = {i: Node(i) for i in range(num_nodes)}

    # Lettura delle connessioni
    for line in lines[1:]:
        node1, node2, cost = map(int, line.split())
        nodes[node1].add_neighbor(nodes[node2], cost)
        nodes[node2].add_neighbor(nodes[node1], cost)  # Connessione bidirezionale

    return list(nodes.values())


def simulate_routing(nodes, max_iterations=10):
    print("Inizio simulazione del protocollo Distance Vector Routing...")
    for iteration in range(max_iterations):
        print(f"\n=== Iterazione {iteration + 1} ===")
        updates = 0
        for node in nodes:
            if node.update_routing_table():
                updates += 1

        for node in nodes:
            node.print_routing_table()

        if updates == 0:
            print("Convergenza raggiunta!")
            break
    else:
        print("Massimo numero di iterazioni raggiunto, la rete potrebbe non essere stabile.")


if __name__ == "__main__":
    filename = "network.txt"  # Nome del file di input
    nodes = initialize_network_from_file(filename)
    simulate_routing(nodes)