import networkx as nx
import numpy as np
import itertools
import pickle
import sys
from multiprocessing import Pool
from tqdm import tqdm
from dataclasses import dataclass

@dataclass
class SimulationSettings:
    i: int
    n: int
    p: float
    graph_count: int
    root_seed: int

@dataclass
class Result:
    graph_node_count: int
    graph_edge_count: int
    visited_edge_count: int
    cycle_count: int

def generate_graph(n, p, gen) -> nx.Graph:
    G = nx.gnp_random_graph(n, p, seed=gen)
    component = max(nx.connected_components(G), key=len)
    Gp = G.subgraph(component)
    return Gp

def run_simulation(settings: SimulationSettings):
    generator_state = np.random.default_rng([settings.i, settings.root_seed])
    results = []
    for _ in range(settings.graph_count):
        G = generate_graph(settings.n, settings.p, generator_state)
        visited_edge_count = 0
        cycle_count = 0
        for chain in nx.chain_decomposition(G):
            if chain[0][0] == chain[-1][1]:
                cycle_count += 1
            visited_edge_count += len(chain)
        results.append(Result(len(G.nodes), len(G.edges), visited_edge_count, cycle_count))
    return results

if __name__ == '__main__':
    out_filename = sys.argv[1]
    num = 30
    p_space = np.logspace(-3, np.log10(0.6), num=num)
    n_space = np.round(np.logspace(2.5, 2, num=num)).astype(int)
    assert len(n_space) == len(set(n_space))
    print(n_space)

    graph_count = 100
    root_seed = 1337

    def prepare_and_solve(args):
        i, (n, p) = args
        settings = SimulationSettings(i, n, p, graph_count, root_seed)
        return (i, n, p, run_simulation(settings))

    results = []
    with Pool(8) as p:
        tasks_gen = enumerate(itertools.product(n_space, p_space))
        for t in tqdm(p.imap_unordered(prepare_and_solve, tasks_gen), total=len(n_space)*len(p_space)):
            results.append(t)

    results.sort(key=lambda p: p[0])
    print(results)

    with open(out_filename, 'wb') as f:
        pickle.dump(results, f)

