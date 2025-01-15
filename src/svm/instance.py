from typing import List
from enum import Enum

from ..morphology.segment_type import SegmentType
from ..morphology.part_of_speech import PartOfSpeech, PartOfSpeechEng, PartOfSpeechTagEng
from ..morphology.mood_type import MoodType
from ..morphology.voice_type import VoiceType
from ..morphology.case_type import CaseType
from ..morphology.state_type import StateType
from ..morphology.pronoun_type import PronounType
from ..morphology.special_type import SpecialType
from ..syntax.word_type import WordType
from ..syntax.syntax_node import SyntaxNode
from ..syntax.syntax_graph import SyntaxGraph
from ..syntax.relation import Relation, RelationEng
from ..syntax.phrase_type import PhraseType
from ..syntax.subgraph import subgraph_end
from ..lexicography.lemma_service import LemmaService
from ..parser.stack import Stack
from ..parser.queue import Queue


class Instance:

    def __init__(self):
        self.feature_vector: List[int] = []
        self.size: int = 0

    @staticmethod
    def instance(
            lemma_service: LemmaService,
            graph: SyntaxGraph,
            stack: Stack,
            queue: Queue,
            english_graph = None):

        instance = Instance()
        word_locs = []
        for x in [stack.node(0), stack.node(1), stack.node(2), queue.peek()]:
            if x and english_graph and x.word!=None and x.word.type==WordType.TOKEN:
                word_locs.append(str(x.word.token.location))
            elif x and english_graph and x.is_phrase:
                try:
                    start_loc = x.start.word.token.location
                    end_loc = x.end.word.token.location
                    loc = str(start_loc).split(":")
                    loc2 = str(end_loc).split(":")
                except Exception as e:
                    continue
                for newl in [loc[0]+":"+loc[1]+":"+str(i) for i in range(int(loc[2]),int(loc2[2])+1)]:
                    word_locs.append(newl)
        # print(word_locs, english_graph)
        for x in [stack.node(0), stack.node(1), stack.node(2), queue.peek()]:

            instance.add_tagged_enum(x.part_of_speech if x else None, PartOfSpeech)
            instance.add_tagged_enum(x.phrase_type if x else None, PhraseType)

            s = x.segment if x else None
            instance.add_enum(s.voice if s else None, VoiceType)
            instance.add_tagged_enum(s.mood if s else None, MoodType)
            instance.add_enum(s.case if s else None, CaseType)
            instance.add_enum(s.state if s else None, StateType)
            instance.add_enum(s.pronoun_type if s else None, PronounType)
            instance.add_enum(s.type if s else None, SegmentType)
            instance.add_tagged_enum(s.special if s else None, SpecialType)

            lemma = s.lemma if s is not None else None
            instance.add_value(lemma_service.value_of(lemma) if lemma is not None else -1, lemma_service.count)

            for relation in Relation:
                instance.add_bit(Instance._has_dependent(graph, x, relation))

            instance.add_bit(Instance._is_valid_subgraph(graph, x))
            instance.add_bit(Instance._is_edge(graph, stack))

            def return_any_eng_rel(eng_deps, relation):
                for w in eng_deps:
                    for rel in eng_deps.get(w):
                        if rel[1]==relation.tag:
                            return True
                return False
            
            def return_any_eng_pos(eng_pos, pos):
                for w in eng_pos:
                    for p in eng_pos.get(w):
                        if p==pos.tag:
                            return True
                return False
            
            if english_graph:
                eng_deps = english_graph["english_dep_g"]
                eng_pos = english_graph["english_pos"]
                eng_tag = english_graph["english_tag"]
            #     for relation in RelationEng:
            #         instance.add_bit(return_any_eng_rel(eng_deps, relation))
            #     for pos in PartOfSpeechEng:
            #         instance.add_bit(return_any_eng_pos(eng_pos, pos))
            # else:
            #     for relation in RelationEng:
            #         instance.add_bit(False)
            #     for pos in PartOfSpeechEng:
            #         instance.add_bit(False)

            if x and english_graph and x.word!=None and x.word.type==WordType.TOKEN:  
                for pos in PartOfSpeechEng:
                    instance.add_bit(Instance._has_eng_pos(eng_pos, str(x.word.token.location), pos))
                for pos in PartOfSpeechTagEng:
                    instance.add_bit(Instance._has_eng_pos(eng_tag, str(x.word.token.location), pos))
                for relation in RelationEng:
                    instance.add_bit(Instance._has_eng_dependent(eng_deps, str(x.word.token.location), relation, word_locs))
                    instance.add_bit(Instance._has_eng_dependent_within(eng_deps, str(x.word.token.location), relation, word_locs))
            elif x and english_graph and x.is_phrase:
                for pos in PartOfSpeechEng:
                    instance.add_bit(Instance._has_eng_pos_phrase(eng_pos, x, pos))
                for pos in PartOfSpeechTagEng:
                    instance.add_bit(Instance._has_eng_pos_phrase(eng_tag, x, pos))
                for relation in RelationEng:
                    instance.add_bit(Instance._has_eng_dependent_phrase(eng_deps, x, relation, word_locs))
                    instance.add_bit(Instance._has_eng_dependent_phrase_within(eng_deps, x, relation, word_locs))
            else:
                for pos in PartOfSpeechEng:
                    instance.add_bit(False)
                for pos in PartOfSpeechTagEng:
                    instance.add_bit(False)
                for relation in RelationEng:
                    instance.add_bit(False)
                    instance.add_bit(False)
                

        return instance

    def add_bit(self, bit: bool):
        if bit:
            self.feature_vector.append(self.size)
        self.size += 1

    def add_enum(self, value: Enum | None, enum_type: type[Enum]):
        if value is not None:
            self.feature_vector.append(self.size + value.value)
        self.size += len(enum_type)

    def add_tagged_enum(self, value: Enum | None, enum_type: type[Enum]):
        if value is not None:
            self.feature_vector.append(self.size + value.value[0])
        self.size += len(enum_type)

    def add_value(self, value: int, size: int):
        if value >= 0:
            self.feature_vector.append(self.size + value)
        self.size += size

    @staticmethod
    def _has_dependent(graph: SyntaxGraph, head: SyntaxNode, relation: Relation):
        for edge in graph.edges:
            if edge.head is head and edge.relation is relation:
                return True
        return False
    
    @staticmethod
    def _has_eng_dependent(eng_deps, head_loc, relation: Relation, word_locs, extra_constraints=[]):
        for a in eng_deps.get(head_loc, []):
            # if a[1] == relation.tag and (a[0] not in extra_constraints) and (a[0] != head_loc):
            if (a[1] == relation.tag and (a[0] not in extra_constraints)) and ((a[0] in word_locs) and (a[0] != head_loc)):    
                return True
                
        return False
    
    @staticmethod
    def _has_eng_dependent_within(eng_deps, head_loc, relation: Relation, word_locs, extra_constraints=[]):
        for a in eng_deps.get(head_loc, []):
            # if a[1] == relation.tag and (a[0] not in extra_constraints) and (a[0] != head_loc):
            if a[1] == relation.tag and (a[0] == head_loc or a[0] in extra_constraints):    
                return True
                
        return False
    
    @staticmethod
    def _has_eng_dependent_phrase_within(eng_deps, head, relation: Relation, word_locs):
        try:
            start_loc = head.start.word.token.location
            end_loc = head.end.word.token.location
            loc = str(start_loc).split(":")
            loc2 = str(end_loc).split(":")
            extra_constraints = [loc[0]+":"+loc[1]+":"+str(i) for i in range(int(loc[2]),int(loc2[2])+1)]
        except Exception as e:
            # print("error for getting phrase english dep", e)
            return False
        for newloc in extra_constraints:
            if Instance._has_eng_dependent_within(eng_deps, newloc, relation, word_locs, extra_constraints=extra_constraints):
                # print("returning true for ", newloc, relation)
                return True
                
        return False
    
    @staticmethod
    def _has_eng_pos(eng_pos, head_loc, pos):
        for a in eng_pos.get(head_loc, []):
            if a == pos.tag:
                return True
        return False
    
    @staticmethod
    def _has_eng_dependent_phrase(eng_deps, head, relation: Relation, word_locs):
        try:
            start_loc = head.start.word.token.location
            end_loc = head.end.word.token.location
            loc = str(start_loc).split(":")
            loc2 = str(end_loc).split(":")
            extra_constraints = [loc[0]+":"+loc[1]+":"+str(i) for i in range(int(loc[2]),int(loc2[2])+1)]
        except Exception as e:
            # print("error for getting phrase english dep", e)
            return False
        for newloc in extra_constraints:
            if Instance._has_eng_dependent(eng_deps, newloc, relation, word_locs, extra_constraints=extra_constraints):
                # print("returning true for ", newloc, relation)
                return True
                
        return False
    
    @staticmethod
    def _has_eng_pos_phrase(eng_pos, head, pos):
        try:
            start_loc = head.start.word.token.location
            end_loc = head.end.word.token.location
            loc = str(start_loc).split(":")
            loc2 = str(end_loc).split(":")
        except Exception as e:
            # print("error for getting phrase english pos", e)
            return False
        for i in range(int(loc[2]),int(loc2[2])+1):
            newloc = loc[0]+":"+loc[1]+":"+str(i)
            if Instance._has_eng_pos(eng_pos, newloc, pos):
                # print("returning true for ", newloc, pos)
                return True
            
        return False

    @staticmethod
    def _is_valid_subgraph(graph: SyntaxGraph, node: SyntaxNode):
        if node is not None and not node.is_phrase and graph.head(node) is None:
            end = subgraph_end(graph, node)
            return end is not None and graph.head(end) is not None and graph.phrase(node, end) is None
        return False

    @staticmethod
    def _is_edge(graph: SyntaxGraph, stack: Stack):
        return (stack.node(0) is not None
                and stack.node(1) is not None
                and graph.edge(stack.node(0), stack.node(1)) is not None)
