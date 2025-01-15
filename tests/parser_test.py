from pathlib import Path
import unittest

from .elas import Elas
from .split_treebank import split_treebank, small_sample
from src.container import Container
from src.parser.oracle import Oracle
from src.parser.parser import Parser
from src.svm.train import train
from src.svm.model import load_model

import pandas as pd

class ParserTest(unittest.TestCase):
    MODEL_FOLDER = Path('.model')

    def setUp(self):
        self.container = Container()
        self.elas = Elas()

    def test_oracle(self):
        for expected_graph in self.container.syntax_service.graphs:

            output_graph = expected_graph.only_tokens()
            oracle = Oracle(expected_graph, output_graph)
            oracle.expected_actions()

            self.elas.compare(expected_graph, output_graph)

            # all output edges should be expected
            for output_edge in output_graph.edges:
                self.assertEqual(expected_graph.contains_edge(output_edge), True)

        self.elas.update_dfs()
        print(f'Oracle Running precision (should be 1..): {self.elas.precision}')
        print(self.elas.get_precision_accuracy_by_x("any_phrase"))

        print(f'Oracle Running recall (should be >0.94): {self.elas.recall}')
        print(self.elas.get_recall_accuracy_by_x("any_phrase"))
        
        # print(f'Running F1 score: {self.elas.f1_score}')
        # self.assertEqual(self.elas.precision, 1.0)
        # self.assertEqual(self.elas.recall, 0.945793687759221)

    def test_on_small_sample(self, n=500, compare_eng_models=False):
        self.elas = Elas()
        (train_graphs, test_graphs) = small_sample(self.container.syntax_service, n)
        if compare_eng_models:
            by = ["any_phrase","relation"]
            by2 = ["any_phrase"]
            self.elas = Elas()
            self._train_and_test(train_graphs, test_graphs, use_eng_models=False)
            rdf1,pdf1 = self.elas.get_recall_accuracy_by_x(by), self.elas.get_precision_accuracy_by_x(by)
            rdf1_by2,pdf1_by2 = self.elas.get_recall_accuracy_by_x(by2), self.elas.get_precision_accuracy_by_x(by2)

            self.elas = Elas()
            self._train_and_test(train_graphs, test_graphs, use_eng_models=True)
            rdf2,pdf2 = self.elas.get_recall_accuracy_by_x(by), self.elas.get_precision_accuracy_by_x(by)
            rdf2_by2,pdf2_by2 = self.elas.get_recall_accuracy_by_x(by2), self.elas.get_precision_accuracy_by_x(by2)

            print(pd.concat([pdf1, pdf2], axis=1))
            print(pd.concat([rdf1, rdf2], axis=1))

            print(pd.concat([pdf1_by2, pdf2_by2], axis=1))
            print(pd.concat([rdf1_by2, rdf2_by2], axis=1))
            
        else:
            self.elas = Elas()
            self._train_and_test(train_graphs, test_graphs, use_eng_models=True)

    def test_ten_fold_cross_validation(self):
        for fold in range(10):
            # train
            print(f'Fold {fold}')
            (train_graphs, test_graphs) = split_treebank(self.container.syntax_service, fold)
            self._train_and_test(train_graphs, test_graphs)

    def _train_and_test(self, train_graphs, test_graphs, use_eng_models=False):
        lemma_service = self.container.lemma_service
        train(lemma_service, train_graphs, self.MODEL_FOLDER, use_eng_models=use_eng_models)

        # test
        print('Evaulating...')
        model = load_model(self.MODEL_FOLDER)
        for expected_graph in test_graphs:
            output_graph = expected_graph.only_tokens()
            parser = Parser(model, lemma_service, output_graph, use_eng_models=use_eng_models)
            try:
                parser.parse()
            except Exception as e:
                print(e)
            self.elas.compare(expected_graph, output_graph)

        self.elas.update_dfs()
        print(f'Running precision: {self.elas.precision}')
        # print(self.elas.get_precision_accuracy_by_x(["any_phrase","relation"]))
        # print(self.elas.get_precision_accuracy_by_x(["any_phrase"]))

        print(f'Running recall: {self.elas.recall}')
        # print(self.elas.get_recall_accuracy_by_x(["any_phrase","relation"]))
        # print(self.elas.get_recall_accuracy_by_x(["any_phrase"]))

        print(f'Running F1 score: {self.elas.f1_score}')

if __name__ == '__main__':
    unittest.main()
