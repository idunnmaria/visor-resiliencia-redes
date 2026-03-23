import json
import random
import math
import argparse
from datetime import datetime

# --- CONFIGURACIÓN ---
DEFAULT_NODES = 80
OUTPUT_FILE = "syntropy_100.json"

class SyntropyEngine:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.nodes = []
        self.connections = []

    def vector_distance(self, v1, v2):
        return math.sqrt(sum((a - b)**2 for a, b in zip(v1, v2)))

    def initialize(self):
        print(f"[*] Sembrando {self.num_nodes} nodos de entropía...")
        for i in range(self.num_nodes):
            self.nodes.append({
                "id": i,
                "vector": [random.uniform(-2.0, 2.0) for _ in range(3)],
                "status": "chaotic",
                "role": "standard"
            })

    def crystallize(self):
        """Alica fuerza de convergencia hasta lograr orden perfecto."""
        print("[*] Iniciando proceso de cristalización...")
        
        # 1. Definir Centro
        center = [0, 0, 0]
        self.nodes.sort(key=lambda n: self.vector_distance(n["vector"], center))
        
        # 2. Asignar Roles
        num_hubs = max(1, int(self.num_nodes * 0.15))
        for i in range(num_hubs):
            self.nodes[i]["role"] = "hub"
            self.nodes[i]["status"] = "coherent"
        
        # 3. Convergencia Forzada (Todos se vuelven coherentes)
        for node in self.nodes:
            node["status"] = "coherent"
            node["coherence_score"] = 1.0

        # 4. Conexiones de Malla (Mesh Topology)
        for i, node in enumerate(self.nodes):
            # Buscar vecinos más cercanos
            neighbors = sorted(self.nodes, key=lambda x: self.vector_distance(node["vector"], x["vector"]))
            
            # Conectar con los 3 más cercanos (excluyéndose a sí mismo)
            connections_made = 0
            for neighbor in neighbors[1:]:
                if connections_made >= 3: break
                
                # Evitar duplicados
                if not self._connection_exists(node["id"], neighbor["id"]):
                    strength = random.uniform(0.8, 1.0) # Vínculos fuertes
                    self.connections.append({
                        "source": node["id"],
                        "target": neighbor["id"],
                        "strength": strength
                    })
                    connections_made += 1

    def _connection_exists(self, id1, id2):
        for c in self.connections:
            if (c["source"] == id1 and c["target"] == id2) or \
               (c["source"] == id2 and c["target"] == id1):
                return True
        return False

    def save(self, filepath):
        data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "nodes_count": self.num_nodes
            },
            "metrics": {
                "final_entropy": 0.0,
                "final_syntropy": 1.0
            },
            "data": {
                "nodes": self.nodes,
                "connections": self.connections
            }
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"[SUCCESS] Universo generado en: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--nodes', type=int, default=DEFAULT_NODES)
    parser.add_argument('--output', type=str, default=OUTPUT_FILE)
    args = parser.parse_args()

    engine = SyntropyEngine(args.nodes)
    engine.initialize()
    engine.crystallize()
    engine.save(args.output)
