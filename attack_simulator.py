#!/usr/bin/env python3
import argparse
import json
import random
from dataclasses import dataclass
from typing import Any, Dict, Tuple, List

import networkx as nx


@dataclass(frozen=True)
class Metrics:
    nodes: int
    edges: int
    avg_degree: float
    density: float
    components: int
    gcc_nodes: int
    gcc_pct: float
    avg_clustering: float
    global_efficiency: float | None  # puede ser costosa en grafos grandes


def build_graph(data: Dict[str, Any]) -> nx.Graph:
    """
    Admite formatos típicos:
    - data["nodes"] = [{"id": "...", ...}, ...]
    - data["edges"] = [{"source": "...", "target": "..."}, ...]
      o ["links"] en vez de "edges" (por compatibilidad)
    """
    nodes = data.get("nodes", [])
    edges = data.get("edges", data.get("links", []))

    G = nx.Graph()

    # nodos
    for n in nodes:
        nid = n.get("id") if isinstance(n, dict) else n
        if nid is None:
            continue
        attrs = n if isinstance(n, dict) else {}
        G.add_node(nid, **attrs)

    # aristas
    for e in edges:
        if not isinstance(e, dict):
            continue
        s = e.get("source")
        t = e.get("target")
        if s is None or t is None:
            continue
        attrs = {k: v for k, v in e.items() if k not in ("source", "target")}
        G.add_edge(s, t, **attrs)

    return G


def compute_metrics(G: nx.Graph, *, compute_efficiency: bool) -> Metrics:
    n = G.number_of_nodes()
    m = G.number_of_edges()

    avg_degree = (2 * m / n) if n > 0 else 0.0
    density = nx.density(G) if n > 1 else 0.0

    if n == 0:
        components = 0
        gcc_nodes = 0
        gcc_pct = 0.0
        avg_clustering = 0.0
        ge = None
    else:
        components = nx.number_connected_components(G)
        gcc = max(nx.connected_components(G), key=len) if components > 0 else set()
        gcc_nodes = len(gcc)
        gcc_pct = (gcc_nodes / n) * 100.0 if n > 0 else 0.0
        avg_clustering = nx.average_clustering(G) if n > 1 else 0.0

        # global_efficiency es O(n^3) en el peor caso; en grafos pequeños está bien
        ge = None
        if compute_efficiency and n <= 400:
            try:
                ge = nx.global_efficiency(G)
            except Exception:
                ge = None

    return Metrics(
        nodes=n,
        edges=m,
        avg_degree=avg_degree,
        density=density,
        components=components,
        gcc_nodes=gcc_nodes,
        gcc_pct=gcc_pct,
        avg_clustering=avg_clustering,
        global_efficiency=ge,
    )


def attack_random_node_removal(G: nx.Graph, attack_rate: float, rng: random.Random) -> Tuple[nx.Graph, List[str]]:
    """
    Elimina aleatoriamente un % de nodos. attack_rate en [0,1].
    """
    if G.number_of_nodes() == 0 or attack_rate <= 0:
        return G.copy(), []

    k = int(round(G.number_of_nodes() * attack_rate))
    k = max(0, min(k, G.number_of_nodes()))

    nodes = list(G.nodes())
    rng.shuffle(nodes)
    removed = nodes[:k]

    H = G.copy()
    H.remove_nodes_from(removed)
    return H, removed


def graph_to_json_like(original_data: Dict[str, Any], G: nx.Graph) -> Dict[str, Any]:
    """
    Reconstruye nodes/edges manteniendo atributos conocidos del JSON original si existen.
    """
    orig_nodes_by_id: Dict[str, Dict[str, Any]] = {}
    for n in original_data.get("nodes", []):
        if isinstance(n, dict) and "id" in n:
            orig_nodes_by_id[str(n["id"])] = n

    nodes_out = []
    for nid, attrs in G.nodes(data=True):
        base = orig_nodes_by_id.get(str(nid), {"id": nid})
        merged = dict(base)
        merged.update(attrs or {})
        merged["id"] = nid
        nodes_out.append(merged)

    edges_out = []
    for u, v, attrs in G.edges(data=True):
        e = {"source": u, "target": v}
        if attrs:
            e.update(attrs)
        edges_out.append(e)

    out = dict(original_data)
    out["nodes"] = nodes_out
    out["edges"] = edges_out
    out.pop("links", None)  # normalizamos a "edges"
    return out


def main() -> None:
    p = argparse.ArgumentParser(description="Visor Resiliencia Redes — simulador de ataque (eliminación aleatoria de nodos).")
    p.add_argument("--input", default="syntropy_100.json", help="Archivo JSON de entrada (legacy: syntropy_100.json).")
    p.add_argument("--output", default="syntropy_attacked.json", help="Archivo JSON de salida.")
    p.add_argument("--attack-rate", type=float, default=0.30, help="Proporción de nodos eliminados (0..1).")
    p.add_argument("--seed", type=int, default=None, help="Semilla RNG para reproducibilidad.")
    p.add_argument("--compute-efficiency", action="store_true", help="Calcula global_efficiency (solo recomendable en grafos pequeños).")
    args = p.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    G = build_graph(data)
    rng = random.Random(args.seed)

    before = compute_metrics(G, compute_efficiency=args.compute_efficiency)

    H, removed_nodes = attack_random_node_removal(G, args.attack_rate, rng)
    after = compute_metrics(H, compute_efficiency=args.compute_efficiency)

    out = graph_to_json_like(data, H)
    out["metadata"] = {
        "app": "visor-resiliencia-redes",
        "model": "random_node_removal",
        "attack_rate": args.attack_rate,
        "seed": args.seed,
        "removed_nodes": removed_nodes,
    }
    out["metrics_before"] = before.__dict__
    out["metrics_after"] = after.__dict__

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"[OK] Output: {args.output}")
    print(f"[INFO] Nodes before/after: {before.nodes} → {after.nodes}")
    print(f"[INFO] GCC% before/after: {before.gcc_pct:.1f}% → {after.gcc_pct:.1f}%")
    print(f"[INFO] Components before/after: {before.components} → {after.components}")


if __name__ == "__main__":
    main()
