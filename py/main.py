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
    G = nx.fast_gnp_random_graph(n, p, seed=gen)
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

@dataclass
class RunSettings:
    space_size: int
    p_space_start: float
    p_space_end: float
    n_space_start: float
    n_space_end: float
    graph_count: int
    root_seed: int

    @staticmethod
    def get_default():
        return RunSettings(
            space_size=100,
            p_space_start=-3,
            p_space_end=np.log10(0.5),
            n_space_start=3,
            n_space_end=1.5,
            graph_count=1000,
            root_seed=1337
        )

    def get_p_space(self):
        return np.logspace(self.p_space_start, self.p_space_end, num=self.space_size)

    def get_n_space(self):
        n_space = np.round(np.logspace(self.n_space_start, self.n_space_end, num=self.space_size)).astype(int)
        assert len(n_space) == len(set(n_space))
        return n_space

if __name__ == '__main__':
    out_filename = sys.argv[1]
    settings = RunSettings.get_default()

    p_space = settings.get_p_space()
    n_space = settings.get_n_space()
    print(n_space)

    def prepare_and_solve(args):
        global settings
        i, (n, p) = args
        settings = SimulationSettings(i, n, p, settings.graph_count, settings.root_seed)
        return (i, n, p, run_simulation(settings))

    results = []
    with Pool(8) as p:
        tasks_gen = enumerate(itertools.product(n_space, p_space))
        for t in tqdm(p.imap_unordered(prepare_and_solve, tasks_gen), total=len(n_space)*len(p_space)):
            results.append(t)

    results.sort(key=lambda p: p[0])

    with open(out_filename, 'wb') as f:
        pickle.dump((settings, results), f)

