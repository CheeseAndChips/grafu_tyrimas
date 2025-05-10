import networkx as nx
import numpy as np
import itertools
import pickle
import sys
from tqdm import tqdm
from dataclasses import dataclass
from typing import Any

@dataclass
class SimulationSettings:
    i: int
    n: int
    p: float
    graph_count: int
    max_retries: int
    root_seed: int

@dataclass
class GeneratorState:
    retries_left: int
    rng_state: np.random.Generator

@dataclass
class Result:
    edge_count: int
    cycle_count: int

def generate_graph(n, p, generator_state: GeneratorState) -> nx.Graph | None:
    while generator_state.retries_left > 0:
        G = nx.gnp_random_graph(n, p, seed=generator_state.rng_state)
        if nx.is_connected(G):
            return G
        else:
            generator_state.retries_left -= 1
    return None

def run_simulation(settings: SimulationSettings):
    generator_state = GeneratorState(
        settings.max_retries,
        np.random.default_rng([settings.i, settings.root_seed])
    )
    results = []
    for i in range(settings.graph_count):
        G = generate_graph(settings.n, settings.p, generator_state)
        if G is None:
            return None
        edge_count = 0
        cycle_count = 0
        for chain in nx.chain_decomposition(G):
            if chain[0][0] == chain[-1][1]:
                cycle_count += 1
            edge_count += len(chain)
        results.append(Result(edge_count, cycle_count))
    return results


out_filename = sys.argv[1]
num = 10
p_space = np.logspace(-3, np.log10(0.6), num=num)
n_space = np.round(np.logspace(2, 2.5, num=num)).astype(int)
assert len(n_space) == len(set(n_space))

graph_count = 10
max_retries = graph_count
root_seed = 1337

results = dict()
for i, (n, p) in tqdm(enumerate(itertools.product(n_space, p_space)), total=len(n_space)*len(p_space)):
    settings = SimulationSettings(i, n, p, graph_count, max_retries, root_seed)
    results[(n, p)] = run_simulation(settings)

with open(out_filename, 'wb') as f:
    pickle.dump(results, f)

