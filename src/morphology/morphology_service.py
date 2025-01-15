from pathlib import Path
from typing import List

from .segment import Segment
from .segment_reader import SegmentReader
from .tsv_reader import TsvReader
from ..orthography.chapter import Chapter
from ..orthography.token import Token
from ..orthography.location import Location
from ..orthography.verse import Verse
from ..lexicography.lemma_service import LemmaService
from ..api.corpus_client import CorpusClient
from ..api.responses import SegmentResponse

import pandas as pd
import re

class MorphologyService:
    MORPHOLOGY_FILE = Path("data/quranic-corpus.txt") #Path('data/morphology.tsv')
    
    def __init__(self, client: CorpusClient, lemma_service: LemmaService):
        self._create_morph_df(lemma_service)


    def _create_morph_df(self, lemma_service):
        # NOTE: (37:130:3:1)	<ilo yaAsiyna changed to =>>> (37:130:3:1)	<iloyaAsiyna manually (removed space)
        file1 = open(self.MORPHOLOGY_FILE, 'r') #open("data/quranic-corpus.txt", 'r')
        Lines = file1.readlines()

        cols = Lines[0].strip().split()
        rows = []

        count = 0
        # Strips the newline character
        for line in Lines[1:]:
            count += 1
            # print("Line{}: {}".format(count, line.strip().split()))
            r = line.strip().split()
            if r[1:] == ['PRON', 'SUFFIX|PRON:1S']:
                r = [r[0]] + [None, 'PRON', 'SUFFIX|PRON:1S']
            if len(r)!=4:
                print(count,line)
            rows.append(r)
        
        df = pd.DataFrame(rows)
        df.columns = cols
        df[["surah","verse","word","token"]] = df[["LOCATION"]].apply(lambda x: x["LOCATION"][1:-1].split(":"), axis=1,result_type='expand')
        df["word_loc"] = df.apply(lambda x: "("+str(x["surah"])+":"+str(x["verse"])+":"+str(x["word"])+")",axis=1)
        df["FEATURES"] = df["FEATURES"].apply(lambda x: x.split("|"))
        df=df.reset_index()
        
        df["is_verb"] = (df["TAG"].isin(["V"])).astype(int)
        df["word_has_verb"] = df.groupby(["surah","verse","word"])["is_verb"].transform("sum")
        df["complete_word_form"] = df.groupby(["surah","verse","word"])["FORM"].transform("sum")
        df['complete_word_form_list'] = df['word_loc'].map(df.groupby('word_loc')['FORM'].agg(list))
        df['complete_word_tag_list'] = df['word_loc'].map(df.groupby('word_loc')['TAG'].agg(list))

        #Get root for verb
        r = re.compile("^ROOT\:(.+)")
        df["root"] = df["FEATURES"].apply(lambda x: list(filter(r.match, x)))
        mask = (df["root"].apply(lambda x: len(x))>0)
        df.loc[mask,"root"] = df[mask]["root"].apply(lambda x: r.match(x[0])[1])
        df.loc[~mask,"root"] = None

        #Get lem for verb
        r = re.compile("^LEM\:(.+)")
        df["lem"] = df["FEATURES"].apply(lambda x: list(filter(r.match, x)))
        mask = (df["lem"].apply(lambda x: len(x))>0)
        df.loc[mask,"lem"] = df[mask]["lem"].apply(lambda x: r.match(x[0])[1])
        df.loc[~mask,"lem"] = None

        #fixing errors
        df.loc[51241,"lem"] = df.loc[51241]["lem"].replace("2","")

        # get PERF/IMPF word verb
        r = re.compile("PERF|IMPF|IMPV")
        df["aspect"] = df["FEATURES"].apply(lambda x: list(filter(r.match, x)))
        mask = (df["aspect"].apply(lambda x: len(x))>0)
        df.loc[mask,"aspect"] = df[mask]["aspect"].apply(lambda x: x[0])
        df.loc[~mask,"aspect"] = None

        # get Active/passive voice verb
        r = re.compile("PASS")
        df["voice"] = df["FEATURES"].apply(lambda x: list(filter(r.match, x)))
        mask = (df["voice"].apply(lambda x: len(x))>0)
        df.loc[mask,"voice"] = df[mask]["voice"].apply(lambda x: x[0])
        df.loc[~mask,"voice"] = "ACT"

        # get Verb mood
        r = re.compile("MOOD\:SUBJ|MOOD\:SUBJ")
        df["mood"] = df["FEATURES"].apply(lambda x: list(filter(r.match, x)))
        mask = (df["mood"].apply(lambda x: len(x))>0)
        df.loc[mask,"mood"] = df[mask]["mood"].apply(lambda x: x[0].replace("MOOD:",""))
        df.loc[~mask,"mood"] = "IND"

        # get Form of verb
        r = re.compile("\(I\)|\(II\)|\(III\)|\(IV\)|\(V\)|\(VI\)|\(VII\)|\(VIII\)|\(IX\)|\(X\)|\(XII\)")
        df["verbform"] = df["FEATURES"].apply(lambda x: list(filter(r.match, x)))
        mask = (df["verbform"].apply(lambda x: len(x))>0)
        df.loc[mask,"verbform"] = df[mask]["verbform"].apply(lambda x: x[0][1:-1])
        df.loc[~mask,"verbform"] = "I"

        # get Conjugation
        r = re.compile("|".join(['1P',
        '1S',
        '2D',
        '2FD',
        '2FP',
        '2FS',
        '2MD',
        '2MP',
        '2MS',
        '3FD',
        '3FP',
        '3FS',
        '3MD',
        '3MP',
        '3MS']))
        df["conj"] = df["FEATURES"].apply(lambda x: list(filter(r.search, x)))
        mask = (df["conj"].apply(lambda x: len(x))>0)
        df.loc[mask,"conj"] = df[mask]["conj"].apply(lambda x: x[0].replace("PRON:",""))
        df.loc[~mask,"conj"] = None

        df["verbal_word_form"] = df.groupby(["surah","verse","word","conj"])["FORM"].transform("sum")


        self.service_dict = {}
        segread = SegmentReader(lemma_service)
        
        for idx, g in df.groupby(["surah","verse","word"]):
            r = g.iloc[0]
            loc = Location(int(r["surah"]),int(r["verse"]),int(r["word"]))
            
            segs = []
            i=0
            for idxr, r in g.iterrows():
                s = segread.read(" ".join(r["FEATURES"][1:]), r["FEATURES"][0]=='STEM')
                s.segment_number = i + 1
                i+=1
                segs.append(s)

            t = Token(loc)
            t.segments = segs

            self.service_dict[str(loc)] = t
        return
    
    def token(self, location: Location):
        # chapter = self._chapters[location.chapter_number - 1]
        # verse = chapter.verses[location.verse_number - 1]
        # token = verse.tokens[location.token_number - 1]
        return self.service_dict[str(location)]

    # def _read_morphology(self, lemma_service: LemmaService):

    #     # morphology
    #     tokens: List[Token]
    #     segments: List[List[Segment]]
    #     with TsvReader(lemma_service) as tsv_reader:
    #         with open(self.MORPHOLOGY_FILE, 'r') as file:
    #             for line in file:
    #                 tsv_reader.read_segment(line.strip())
    #         tokens = tsv_reader.tokens
    #         segments = tsv_reader.segments

    #     # tokens
    #     verse: Verse = None
    #     token_count = len(tokens)
    #     for i in range(token_count):
    #         token = tokens[i]
    #         token.segments = segments[i]

    #         # new verse?
    #         location = token.location
    #         chapter_number = location.chapter_number
    #         verse_number = location.verse_number
    #         if (verse is None
    #             or verse.location.chapter_number != chapter_number
    #                 or verse.location.verse_number != verse_number):
    #             verse = Verse(Location(chapter_number, verse_number, 0), [])
    #             self._chapters[chapter_number - 1].verses.append(verse)

    #         verse.tokens.append(token)

    # def _download_morphology(self, client: CorpusClient):

    #     if self.MORPHOLOGY_FILE.exists():
    #         return

    #     self.MORPHOLOGY_FILE.parent.mkdir()

    #     print('Downloading metadata...')
    #     chapters = client.metadata().chapters
    #     token_count = 0

    #     print('Downloading morphology...')
    #     with open(self.MORPHOLOGY_FILE, 'w') as writer:
    #         batch_size = 10
    #         for chapter in chapters:
    #             verse_number = 1
    #             while verse_number <= chapter.verse_count:
    #                 location = Location(chapter.chapter_number, verse_number)
    #                 count = min(batch_size, chapter.verse_count - verse_number + 1)
    #                 verses = client.morphology(location, count)
    #                 print(f'Downloaded verse {location}')
    #                 for verse in verses:
    #                     for token in verse.tokens:
    #                         location = token.location
    #                         for segment in token.segments:
    #                             writer.write(self._write_segment(location, segment))
    #                             writer.write('\n')
    #                         token_count += 1
    #                 verse_number += batch_size
    #     print(f'Downloaded: {token_count} tokens')

    # @staticmethod
    # def _write_segment(location: List[int], segment: SegmentResponse):
    #     line = []
    #     for number in location:
    #         line.append(str(number))
    #         line.append('\t')

    #     arabic = segment.arabic
    #     if arabic is not None:
    #         line.append(arabic)
    #     line.append('\t')

    #     morphology = segment.morphology
    #     if morphology is not None:
    #         line.append(morphology)
    #     return ''.join(line)
