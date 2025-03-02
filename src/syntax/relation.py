from enum import Enum, auto


class Relation(Enum):
    POSSESSIVE = auto(), 'poss'
    OBJECT = auto(), 'obj'
    SUBJECT = auto(), 'subj'
    CONJUNCTION = auto(), 'conj'
    LINK = auto(), 'link'
    PREDICATE = auto(), 'pred'
    GENITIVE = auto(), 'gen'
    APPOSITION = auto(), 'app'
    SUBORDINATE = auto(), 'sub'
    ADJECTIVE = auto(), 'adj'
    PASSIVE_SUBJECT = auto(), 'pass'
    SPECIAL_SUBJECT = auto(), 'subjx'
    SPECIAL_PREDICATE = auto(), 'predx'
    CIRCUMSTANTIAL = auto(), 'circ'
    VOCATIVE = auto(), 'voc'
    EXCEPTIVE = auto(), 'exp'
    COGNATE_ACCUSATIVE = auto(), 'cog'
    SPECIFICATION = auto(), 'spec'
    PURPOSE = auto(), 'prp'
    FUTURE = auto(), 'fut'
    INTERROGATIVE = auto(), 'intg'
    EMPHASIS = auto(), 'emph'
    NEGATION = auto(), 'neg'
    PROHIBITION = auto(), 'pro'
    COMPOUND = auto(), 'cpnd'
    CONDITION = auto(), 'cond'
    RESULT = auto(), 'rslt'
    IMPERATIVE_RESULT = auto(), 'imrs'
    IMPERATIVE = auto(), 'impv'
    CERTAINTY = auto(), 'cert'
    ANSWER = auto(), 'ans'
    RESTRICTION = auto(), 'res'
    SURPRISE = auto(), 'sur'
    RETRACTION = auto(), 'ret'
    EXPLANATION = auto(), 'exl'
    PREVENTIVE = auto(), 'prev'
    AVERSION = auto(), 'avr'
    INCEPTIVE = auto(), 'inc'
    EXHORTATION = auto(), 'exh'
    EQUALIZATION = auto(), 'eq'
    CAUSE = auto(), 'caus'
    AMENDMENT = auto(), 'amd'
    SUPPLEMENTAL = auto(), 'sup'
    INTERPRETATION = auto(), 'int'
    COMITATIVE = auto(), 'com'

    def __init__(self, number_value, tag: str):
        self.number_value = number_value
        self.tag = tag

    @staticmethod
    def parse(tag: str):
        return Relation.tags.get(tag)
    
class RelationEng(Enum):
    # ROOT = auto(), 'ROOT'
    acl = auto(), 'acl'
    acomp = auto(), 'acomp'
    advcl = auto(), 'advcl'
    advmod = auto(), 'advmod'
    agent = auto(), 'agent'
    amod = auto(), 'amod'
    appos = auto(), 'appos'
    attr = auto(), 'attr'
    aux = auto(), 'aux'
    auxpass = auto(), 'auxpass'
    case = auto(), 'case'
    cc = auto(), 'cc'
    ccomp = auto(), 'ccomp'
    compound = auto(), 'compound'
    conj = auto(), 'conj'
    csubj = auto(), 'csubj'
    csubjpass = auto(), 'csubjpass'
    dative = auto(), 'dative'
    dep = auto(), 'dep'
    det = auto(), 'det'
    dobj = auto(), 'dobj'
    expl = auto(), 'expl'
    intj = auto(), 'intj'
    mark = auto(), 'mark'
    meta = auto(), 'meta'
    neg = auto(), 'neg'
    nmod = auto(), 'nmod'
    npadvmod = auto(), 'npadvmod'
    nsubj = auto(), 'nsubj'
    nsubjpass = auto(), 'nsubjpass'
    nummod = auto(), 'nummod'
    oprd = auto(), 'oprd'
    parataxis = auto(), 'parataxis'
    pcomp = auto(), 'pcomp'
    pobj = auto(), 'pobj'
    poss = auto(), 'poss'
    preconj = auto(), 'preconj'
    predet = auto(), 'predet'
    prep = auto(), 'prep'
    prt = auto(), 'prt'
    # punct = auto(), 'punct'
    # quantmod = auto(), 'quantmod'
    # relcl = auto(), 'relcl'
    # xcomp = auto(), 'xcomp'

    def __init__(self, number_value, tag: str):
        self.number_value = number_value
        self.tag = tag

    @staticmethod
    def parse(tag: str):
        return RelationEng.tags.get(tag)


Relation.tags = {
    relation.tag: relation
    for relation in Relation
}

Relation.relations = list(Relation)

RelationEng.tags = {
    relation.tag: relation
    for relation in RelationEng
}

RelationEng.relations = list(RelationEng)
