from typing import List

from src.syntax.syntax_graph import SyntaxGraph
from src.syntax.syntax_service import SyntaxService
import random

def split_treebank(syntax_service: SyntaxService, fold: int):

    train_graphs: List[SyntaxGraph] = []
    test_graphs: List[SyntaxGraph] = []

    for i, graph in enumerate(syntax_service.graphs):
        if i % 10 == fold:
            test_graphs.append(graph)
        else:
            train_graphs.append(graph)

    return (train_graphs, test_graphs)

def small_sample(syntax_service: SyntaxService, n: int):

    sample_n = list(range(n))

    train_graphs =  list(random.sample(sample_n, int(n*0.9)))
    test_graphs = list(set(sample_n) - set(train_graphs))

    train_graphs = [syntax_service.graphs[x] for x in train_graphs]
    test_graphs = [syntax_service.graphs[x] for x in test_graphs]
    print("TRAINING/TEST SAMPLE:", len(train_graphs), len(test_graphs))
    return (train_graphs, test_graphs)