from src.syntax.syntax_graph import SyntaxGraph
from src.syntax.word_type import WordType
import pandas as pd

class Elas:

    def __init__(self):
        self._expected_edges: int = 0
        self._output_edges: int = 0
        self._equivalent_edges: int = 0
        self.expected_edge_count = []
        self.output_edge_count = []

    def update_dfs(self):
        self.expected_edge_df = pd.DataFrame(self.expected_edge_count)
        self.output_edge_df = pd.DataFrame(self.output_edge_count)
        return self.expected_edge_df, self.output_edge_df
    
    def get_recall_accuracy_by_x(self,x):
        rdf = self.expected_edge_df.groupby(x)["output_contains"].sum() \
                / self.expected_edge_df.groupby(x)["output_contains"].count()
        return rdf
    
    def get_precision_accuracy_by_x(self,x):
        rdf = self.output_edge_df.groupby(x)["expected_contains"].sum() \
                / self.output_edge_df.groupby(x)["expected_contains"].count()
        return rdf


    def count(self, expected_graph: SyntaxGraph, output_graph: SyntaxGraph):

        def get_loc(n):
            if n.word.type == WordType.ELIDED:
                return None, None
            else:
                l = str(n.word.token.location)
                s = n.segment_number
                return l, s
            
        for e in expected_graph.edges:
            d = {
                "relation": e.relation.tag,
                "head_index": e.head.index,
                "dependent_index": e.dependent.index,
                "output_contains": output_graph.contains_edge(e),
                "any_phrase": e.head.is_phrase or e.dependent.is_phrase
            }

            if e.head.is_phrase:
                d["head_phrase"] = e.head.phrase_type
                d["head_phrase_start"], d["head_phrase_start_seg"] = get_loc(e.head.start)
                d["head_phrase_end"], d["head_phrase_end_seg"] = get_loc(e.head.end)
            else:
                d["head_loc"], d["head_seg"] = get_loc(e.head)
            
            if e.dependent.is_phrase:
                d["dependent_phrase"] = e.dependent.phrase_type
                d["dependent_phrase_start"], d["dependent_phrase_start_seg"] = get_loc(e.dependent.start)
                d["dependent_phrase_end"], d["dependent_phrase_end_seg"] = get_loc(e.dependent.end)
            else:
                d["dependent_loc"], d["dependent_seg"] = get_loc(e.dependent)
            
            self.expected_edge_count.append(d)
        
        for e in output_graph.edges:
            d = {
                "relation": e.relation.tag,
                "head_index": e.head.index,
                "dependent_index": e.dependent.index,
                "expected_contains": expected_graph.contains_edge(e),
                "any_phrase": e.head.is_phrase or e.dependent.is_phrase
            }

            if e.head.is_phrase:
                d["head_phrase"] = e.head.phrase_type
                d["head_phrase_start"], d["head_phrase_start_seg"] = get_loc(e.head.start)
                d["head_phrase_end"], d["head_phrase_end_seg"] = get_loc(e.head.end)
            else:
                d["head_loc"], d["head_seg"] = get_loc(e.head)
            
            if e.dependent.is_phrase:
                d["dependent_phrase"] = e.dependent.phrase_type
                d["dependent_phrase_start"], d["dependent_phrase_start_seg"] = get_loc(e.dependent.start)
                d["dependent_phrase_end"], d["dependent_phrase_end_seg"] = get_loc(e.dependent.end)
            else:
                d["dependent_loc"], d["dependent_seg"] = get_loc(e.dependent)
            
            self.output_edge_count.append(d)
        return
    
    def compare(self, expected_graph: SyntaxGraph, output_graph: SyntaxGraph):
        
        self.count(expected_graph, output_graph)
        self._expected_edges += len(expected_graph.edges)

        for output_edge in output_graph.edges:
            self._output_edges += 1

            if expected_graph.contains_edge(output_edge):
                self._equivalent_edges += 1

    @property
    def precision(self):
        return self._equivalent_edges / self._output_edges

    @property
    def recall(self):
        return self._equivalent_edges / self._expected_edges

    @property
    def f1_score(self):
        precision = self.precision
        recall = self.recall
        return 2 * (precision * recall) / (precision + recall)
