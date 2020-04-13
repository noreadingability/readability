import hashlib
from morph.morphemizer import MecabMorphemizer
from morph import morphemes

import os

F_ASS = 0
F_SRT = 1
F_OTHER = 2


class Title():
    def __init__(self, title_name):
        """
        morphs = {
            MORPH1: [ hashed_line1, hashed_line2 ]
            ...
            MORPHN: [ hashed_line5 ]
        }
        """
        self.filenames = []
        self.total_lines = 0
        self.morphs = {}
        self.hashed_lines = {}
        self.title_name = title_name

    def add_morph(self, morph, hashed_line):
        if morph not in self.morphs:
            self.morphs[morph] = [hashed_line]

        elif hashed_line not in self.morphs[morph]:
            self.morphs[morph].append(hashed_line)
            self.total_lines += 1

    def find_morphs_from_file(self, filepath):
        morphemizer = MecabMorphemizer()
        morphs = []
        self.filenames.append(filepath.split("/")[-1])
        encoding = ["utf-8", "utf-16", "cp932", "SJIS", -1]
        with open(filepath, 'rb') as f:
            text = f.read()
            
            err = ValueError()
            for enc in encoding:
                if enc == -1:
                    raise err
                try:
                    text = str(text, encoding=enc)
                    break
                except Exception as e:
                    err = e

            lines = text.splitlines()
            for line in lines:
                morphs = morphemes.getMorphemes(morphemizer, line)
                if len(morphs) > 0:
                    hashed_line = hashlib.blake2b(line.encode()).digest()
                    self.hashed_lines[hashed_line] = self.hashed_lines.get(
                        hashed_line, 0) + 1
                    for m in morphs:
                        self.add_morph(m, hashed_line)

    def evaluate_readability(self, known_db):
        known_count = 0
        unknown_lines = {}
        
        for m in self.morphs.keys():
            if known_db.matches(m):
                known_count += 1
            else:
                for line in self.morphs[m]:
                    unknown_lines[line] = unknown_lines.get(line, 0) + 1

        total_morphs = len(self.morphs.keys())
        total_lines = len(self.hashed_lines.keys())
        unknown_lines = len(unknown_lines)
        if total_lines == 0:
            return 0, 0
        return (total_lines - unknown_lines)/total_lines, (known_count/total_morphs)

    def print_evaluation(self, known_db):
        line_result, morph_result = self.evaluate_readability(known_db)
        print(f"""
        {self.filenames}

        {self.title_name}
        Line Readability  {line_result*100}%
        Morph Readability {morph_result*100}%
        """)
