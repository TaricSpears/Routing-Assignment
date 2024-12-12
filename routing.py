class Node:
    def __init__(self, name):
        # Ogni nodo ha un nome e una tabella di routing inizializzata con sé stesso (distanza 0)
        self.name = name
        self.routing_table = {name: (0, name)}  # La distanza verso sé stesso è sempre 0
        self.neighbors = {}  # Dizionario per memorizzare i vicini diretti e i costi associati

    def add_neighbor(self, neighbor, cost):
        # Aggiunge un vicino diretto alla lista dei vicini di questo nodo
        self.neighbors[neighbor] = cost
        # Aggiorna la tabella di routing per includere il vicino diretto
        self.routing_table[neighbor.name] = (cost, neighbor.name)

    def update_routing_table(self):
        # Aggiorna la tabella di routing basandosi sulle informazioni dei vicini
        updated = False
        for neighbor, cost_to_neighbor in self.neighbors.items():
            # Itera su ciascuna destinazione nella tabella di routing del vicino
            for dest, (cost_to_dest, next_hop) in neighbor.routing_table.items():
                # Calcola il costo per raggiungere la destinazione attraverso il vicino
                new_cost = cost_to_neighbor + cost_to_dest
                # Aggiorna la tabella di routing se trova un percorso migliore o una nuova destinazione
                if dest not in self.routing_table or new_cost < self.routing_table[dest][0]:
                    self.routing_table[dest] = (new_cost, neighbor.name)
                    updated = True
        return updated

    def print_routing_table(self):
        # Stampa la tabella di routing in un formato leggibile
        print(f"Routing Table for Node {self.name}")
        print("Destination - Cost - Next Hop")
        for dest, (cost, next_hop) in sorted(self.routing_table.items()):
            print(f"{dest:^11} | {cost:^4} | {next_hop:^8}")
        print("-" * 30)


def initialize_network_from_file(filename):
    # Legge un file di configurazione per inizializzare la rete
    with open(filename, 'r') as file:
        lines = file.readlines()

    # La prima riga indica il numero di nodi nella rete
    num_nodes = int(lines[0].strip())
    nodes = {i: Node(i) for i in range(num_nodes)}  # Crea i nodi

    # Le righe successive definiscono le connessioni tra i nodi
    for line in lines[1:]:
        # Ogni linea specifica due nodi connessi e il costo della connessione
        node1, node2, cost = map(int, line.split())
        # Aggiunge ciascun nodo come vicino dell'altro (connessioni bidirezionali)
        nodes[node1].add_neighbor(nodes[node2], cost)
        nodes[node2].add_neighbor(nodes[node1], cost)

    return list(nodes.values())


def simulate_routing(nodes, max_iterations=10):
    # Simula l'esecuzione del protocollo Distance Vector Routing
    for iteration in range(max_iterations):
        print(f"\n Iteration {iteration + 1} :")
        updates = 0
        for node in nodes:
            # Ogni nodo tenta di aggiornare la propria tabella di routing
            if node.update_routing_table():
                updates += 1

        # Stampa le tabelle di routing aggiornate per ogni nodo
        for node in nodes:
            node.print_routing_table()

        # Se nessun nodo ha aggiornato la propria tabella, la rete ha raggiunto la convergenza
        if updates == 0:
            print("Network has converged.")
            break
    else:
        # Se il numero massimo di iterazioni è raggiunto, la rete potrebbe non essere stabile
        print("Network may not have converged.")


if __name__ == "__main__":
    # Specifica il nome del file di input che descrive la rete
    filename = "network.txt"
    # Inizializza i nodi e le connessioni dalla configurazione del file
    nodes = initialize_network_from_file(filename)
    # Avvia la simulazione del protocollo
    simulate_routing(nodes)
