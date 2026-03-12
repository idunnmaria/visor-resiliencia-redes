import json
import random
import networkx as nx
import argparse
import sys

# Script para simular daños en la red y exportar JSON para visualización.

INPUT_FILE = "syntropy_100.json"
OUTPUT_FILE = "syntropy_attacked.json"

def load_network(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] No se encuentra '{filepath}'. Ejecuta primero data_generator.py")
        sys.exit(1)

def build_graph(data):
    G = nx.Graph()
    for node in data['data']['nodes']:
        G.add_node(node['id'], **node) # Guardar todos los atributos (vector, role, etc)
    for conn in data['data']['connections']:
        G.add_edge(conn['source'], conn['target'], strength=conn['strength'])
    return G

def execute_attack(G, damage_rate):
    total = G.number_of_nodes()
    kill_count = int(total * damage_rate)
    
    print(f"[*] Objetivo: Eliminar {kill_count} nodos ({damage_rate*100}%)")
    
    victims = random.sample(list(G.nodes()), kill_count)
    G.remove_nodes_from(victims)
    
    return G, kill_count

def analyze_and_export(G, original_data, output_path):
    # Análisis básico
    if G.number_of_nodes() == 0:
        print("[!] ALERTA: Red totalmente destruida.")
        return

    components = list(nx.connected_components(G))
    print(f"[*] Estado Post-Ataque:")
    print(f"    - Nodos restantes: {G.number_of_nodes()}")
    print(f"    - Fragmentación: {len(components)} islas aisladas.")

    # Reconstruir JSON para el visor web
    nodes_export = []
    for n_id, attrs in G.nodes(data=True):
        # Limpiar atributos de networkx si es necesario y mantener estructura original
        clean_node = attrs.copy()
        clean_node['id'] = n_id
        nodes_export.append(clean_node)

    connections_export = []
    for u, v, attrs in G.edges(data=True):
        connections_export.append({
            "source": u,
            "target": v,
            "strength": attrs['strength']
        })

    output_data = {
        "metadata": {
            "timestamp": original_data['metadata']['timestamp'],
            "status": "DAMAGED",
            "damage_report": f"{len(components)} fragments"
        },
        "metrics": {
            "final_entropy": 0.0, # Asumimos orden local
            "final_syntropy": 1.0
        },
        "data": {
            "nodes": nodes_export,
            "connections": connections_export
        }
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    print(f"[SUCCESS] Datos de ataque guardados en: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default=INPUT_FILE)
    parser.add_argument('--output', type=str, default=OUTPUT_FILE)
    parser.add_argument('--damage', type=float, default=0.2)
    args = parser.parse_args()

    data = load_network(args.input)
    graph = build_graph(data)
    damaged_graph, killed = execute_attack(graph, args.damage)
    analyze_and_export(damaged_graph, data, args.output)
