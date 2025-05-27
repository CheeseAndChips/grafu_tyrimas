from main import *
import matplotlib
import matplotlib.pyplot as plt
import sys
import numpy as np
import os.path
from dataclasses import dataclass
from typing import Any

@dataclass
class State:
    settings: Any
    n: Any
    p: Any
    f: Any
    export: bool

def plot1(d, ax, state: State):
    ff = ax.pcolormesh(state.n, state.p, d, shading='auto')
    ax.set_xscale('log')
    ax.set_yscale('log')

    n_space = state.settings.get_n_space()
    def line(x):
        return np.log(x) / x

    p_values = line(n_space)
    ax.plot(n_space, p_values, color='red', linewidth=2)
    if not state.export:
        ax.set_title('Average node count of largest connected component')
    state.f.colorbar(ff, ax=ax)
    return ff

def plot2(d, ax, state: State):
    ff = ax.pcolormesh(n, p, d, shading='auto')
    ax.set_xscale('log')
    ax.set_yscale('log')
    if not state.export:
        ax.set_title('How many graphs are 2-connected')
    state.f.colorbar(ff, ax=ax)
    return ff

def plot3(d, ax, state: State):
    ff = ax.pcolormesh(n, p, d, shading='auto')
    ax.set_xscale('log')
    ax.set_yscale('log')
    if not state.export:
        ax.set_title('Average amount of bridges')
    state.f.colorbar(ff, ax=ax)
    return ff

def plot4(d, ax, state: State):
    ff = ax.pcolormesh(n, p, d, shading='auto')
    ax.set_xscale('log')
    ax.set_yscale('log')
    if not state.export:
        ax.set_title('Bridges std deviation')
    state.f.colorbar(ff, ax=ax)
    return ff

if __name__ == '__main__':
    SAVE_DIR = '../doc/plots'
    export = '--export' in sys.argv[1:]
    args = [a for a in sys.argv[1:] if a != '--export']
    
    if export:
        matplotlib.rcParams.update({
            'font.family': 'serif',
            'font.size': 9,
        })
        
    fname = args[0]
    with open(fname, 'rb') as f:
        (settings, data) = pickle.load(f)

    print(settings)

    dtype = np.dtype([('n', np.int64), ('p', np.float64), ('r', np.float64)])

    d1 = np.array(
        [(n, p, (np.average([r.graph_node_count for r in results])) / n) for i, n, p, results in data],
        dtype=dtype
    ).reshape((settings.space_size, settings.space_size))

    d2 = np.array(
        [np.average([int(r.cycle_count == 1) for r in results]) for _, n, p, results in data],
        dtype=np.float64
    ).reshape((settings.space_size, settings.space_size))

    d3 = np.array(
        [np.average([
            ((r.graph_edge_count - r.visited_edge_count) / r.graph_edge_count if r.graph_edge_count != 0 else 0)
            for r in results]) for _, n, p, results in data],
        dtype=np.float64
    ).reshape((settings.space_size, settings.space_size))

    d4 = np.array(
        [np.std([
            ((r.graph_edge_count - r.visited_edge_count) / r.graph_edge_count if r.graph_edge_count != 0 else 0)
            for r in results]) for _, n, p, results in data],
        dtype=np.float64
    ).reshape((settings.space_size, settings.space_size))

    n, p, d1 = d1['n'], d1['p'], d1['r']

    def find_closest(needed_p, needed_n):
        _, n, p, results = min(data, key=lambda t: ((t[1] - needed_n)**2 + (t[2] - needed_p)**2))
        return n, p, results

    def onclick(event):
        if event.name != 'button_press_event':
            return
        if event.inaxes != ax3:
            return

        print(f'x={event.xdata}, y={event.ydata}')
        n, p, results = find_closest(event.ydata, event.xdata)
        print(f'{n=} {p=}')
        ax5.clear()
        ax5.hist(
            [(r.graph_edge_count - r.visited_edge_count) / r.graph_edge_count if r.graph_edge_count != 0 else 0 for r in results],
            bins=20,
            range=(0, 1)
        )
        plt.show()


    if export:
        exportable = [(d1, plot1), (d2, plot2), (d3, plot3), (d4, plot4)]
        for i, (d, fn) in enumerate(exportable):
            f = plt.figure(figsize=(3.5, 3.0))
            state = State(settings, n, p, f, export)
            fn(d, plt.axes(), state)
            f.savefig(os.path.join(SAVE_DIR, f'plot{i+1}.pdf'))
    else:
        f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)
        state = State(settings, n, p, f, export)
        cid = f.canvas.mpl_connect('button_press_event', onclick)
        plot1(d1, ax1, state)
        plot2(d2, ax2, state)
        plot3(d3, ax3, state)
        plot4(d4, ax4, state)
        plt.show()

