from enum import Enum, auto


class PartOfSpeech(Enum):
    NOUN = auto(), 'N'
    PROPER_NOUN = auto(), 'PN'
    PRONOUN = auto(), 'PRON'
    DEMONSTRATIVE = auto(), 'DEM'
    RELATIVE = auto(), 'REL'
    ADJECTIVE = auto(), 'ADJ'
    VERB = auto(), 'V'
    PREPOSITION = auto(), 'P'
    INTERROGATIVE = auto(), 'INTG'
    VOCATIVE = auto(), 'VOC'
    NEGATIVE = auto(), 'NEG'
    EMPHATIC = auto(), 'EMPH'
    PURPOSE = auto(), 'PRP'
    IMPERATIVE = auto(), 'IMPV'
    FUTURE = auto(), 'FUT'
    CONJUNCTION = auto(), 'CONJ'
    DETERMINER = auto(), 'DET'
    INITIALS = auto(), 'INL'
    TIME = auto(), 'T'
    LOCATION = auto(), 'LOC'
    ACCUSATIVE = auto(), 'ACC'
    CONDITIONAL = auto(), 'COND'
    SUBORDINATING_CONJUNCTION = auto(), 'SUB'
    RESTRICTION = auto(), 'RES'
    EXCEPTIVE = auto(), 'EXP'
    AVERSION = auto(), 'AVR'
    CERTAINTY = auto(), 'CERT'
    RETRACTION = auto(), 'RET'
    PREVENTIVE = auto(), 'PREV'
    ANSWER = auto(), 'ANS'
    INCEPTIVE = auto(), 'INC'
    SURPRISE = auto(), 'SUR'
    SUPPLEMENTAL = auto(), 'SUP'
    EXHORTATION = auto(), 'EXH'
    IMPERATIVE_VERBAL_NOUN = auto(), 'IMPN'
    EXPLANATION = auto(), 'EXL'
    EQUALIZATION = auto(), 'EQ'
    RESUMPTION = auto(), 'REM'
    CAUSE = auto(), 'CAUS'
    AMENDMENT = auto(), 'AMD'
    PROHIBITION = auto(), 'PRO'
    CIRCUMSTANTIAL = auto(), 'CIRC'
    RESULT = auto(), 'RSLT'
    INTERPRETATION = auto(), 'INT'
    COMITATIVE = auto(), 'COM'

    def __init__(self, number_value, tag: str):
        self.number_value = number_value
        self.tag = tag

    @staticmethod
    def parse(tag: str):
        return PartOfSpeech.tags.get(tag)


PartOfSpeech.tags = {
    part_of_speech.tag: part_of_speech
    for part_of_speech in PartOfSpeech
}

class PartOfSpeechEng(Enum):
    ADJ = auto(), "ADJ"
    ADP = auto(), "ADP"
    ADV = auto(), "ADV"
    AUX = auto(), "AUX"
    CONJ = auto(), "CONJ"
    CCONJ = auto(), "CCONJ"
    DET = auto(), "DET"
    INTJ = auto(), "INTJ"
    NOUN = auto(), "NOUN"
    NUM = auto(), "NUM"
    PART = auto(), "PART"
    PRON = auto(), "PRON"
    PROPN = auto(), "PROPN"
    PUNCT = auto(), "PUNCT"
    SCONJ = auto(), "SCONJ"
    SYM = auto(), "SYM"
    VERB = auto(), "VERB"
    X = auto(), "X"
    EOL = auto(), "EOL"
    SPACE = auto(), "SPACE"

    def __init__(self, number_value, tag: str):
        self.number_value = number_value
        self.tag = tag

    @staticmethod
    def parse(tag: str):
        return PartOfSpeechEng.tags.get(tag)


PartOfSpeechEng.tags = {
    part_of_speech.tag: part_of_speech
    for part_of_speech in PartOfSpeechEng
}

class PartOfSpeechTagEng(Enum):
    # MONEY = auto(), "$"
    # SINGLE_QUOTES = auto(), "''"
    # COMMA = auto(), ","
    # LRB = auto(), "-LRB-"
    # RRB = auto(), "-RRB-"
    PERIOD = auto(), "."
    COLON = auto(), ":"
    ADD = auto(), "ADD"
    AFX = auto(), "AFX"
    CC = auto(), "CC"
    CD = auto(), "CD"
    DT = auto(), "DT"
    EX = auto(), "EX"
    FW = auto(), "FW"
    HYPH = auto(), "HYPH"
    IN = auto(), "IN"
    JJ = auto(), "JJ"
    JJR = auto(), "JJR"
    JJS = auto(), "JJS"
    LS = auto(), "LS"
    MD = auto(), "MD"
    NFP = auto(), "NFP"
    NN = auto(), "NN"
    NNP = auto(), "NNP"
    NNPS = auto(), "NNPS"
    NNS = auto(), "NNS"
    PDT = auto(), "PDT"
    POS = auto(), "POS"
    PRP = auto(), "PRP"
    PRPS = auto(), "PRP$"
    RB = auto(), "RB"
    RBR = auto(), "RBR"
    RBS = auto(), "RBS"
    RP = auto(), "RP"
    SYM = auto(), "SYM"
    TO = auto(), "TO"
    UH = auto(), "UH"
    VB = auto(), "VB"
    VBD = auto(), "VBD"
    VBG = auto(), "VBG"
    VBN = auto(), "VBN"
    VBP = auto(), "VBP"
    VBZ = auto(), "VBZ"
    WDT = auto(), "WDT"
    WP = auto(), "WP"
    WPS = auto(), "WP$"
    WRB = auto(), "WRB"
    # XX = auto(), "XX"
    # SP = auto(), "_SP"
    # APOSTROPHE = auto(), "``"

    def __init__(self, number_value, tag: str):
        self.number_value = number_value
        self.tag = tag

    @staticmethod
    def parse(tag: str):
        return PartOfSpeechTagEng.tags.get(tag)


PartOfSpeechTagEng.tags = {
    part_of_speech.tag: part_of_speech
    for part_of_speech in PartOfSpeechTagEng
}
