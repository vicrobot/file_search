#!/usr/bin/env python3.8

import os
from sys import argv
from magic import from_file as test
import time
from numpy import inf
from termcolor import colored

showoff_time = 2e-1

"""
#Ideas

1. We can extend this idea to search not only for text, but also for image search, sound search etc.
2. Searching in specific directory instead of current directory.
"""

class find:
    def __init__(self, search_term, depth, word_color = 'red'):
        self.text = 'text'
        self.search_term = search_term
        self.search_depth = depth
        self.file_pathnlines = {} # k,v :: file path, file lines which have search term
        self.word_color = word_color
    
    def read(self,file_path):
        """
        reads files and searches in them the word, 
        stores lines which has the search_terms in pertaining_lines dict.
        Also, stores those dicts with corresponding file's path in file_pathnlines.
        """
        found = 0
        pertaining_lines={}  # k,v :: line_num, line
        with open(file_path, 'r') as ofile:
            for count, line in enumerate(ofile.readlines()):
                line = line.strip()
                if self.search_term in line:
                    pertaining_lines[count] = line
                    found = 1
            if found:
                self.file_pathnlines[file_path] = pertaining_lines
    
    def final_p(self):
        #does final output.
        colored_string = colored(self.search_term,self.word_color)
        total_word_count = 0
        for file_path,line_dict in self.file_pathnlines.items():
            print(f"Found in file:\n {file_path}")
            for line_num,line in line_dict.items():
                print(f"    Line No: {line_num}")
                print(f"    Line: {colored_string.join(line.split(self.search_term))}")
                total_word_count += line.count(search_term)
        print(f'Total files containing "{self.search_term}" : {len(self.file_pathnlines)}')
        print(f'Total occurings: {total_word_count}')
    
    def go(self,dir_name, base_dir = 1, curdepth=1):
        if base_dir: print(f'Looking in {dir_name}', end = '', flush = True)
        for path in os.listdir(dir_name):
            abspath = dir_name + '/' + path
            if os.path.isdir(abspath):
                if curdepth + 1 > self.search_depth: continue
                if base_dir:
                    print(f'/{path}',end = '', flush = True)
                    time.sleep(showoff_time)
                self.go(abspath, base_dir = 0, curdepth = curdepth+1)
                if base_dir:
                    size=len(path) + 1
                    print('\b'*size + ' '*size + '\b'*size ,end='',flush=True)
                    time.sleep(showoff_time)
            else:
                try:
                    if test(abspath, mime=True).strip()[:4] == self.text:
                        self.read(abspath)
                except IndexError: pass
        if base_dir:
            print("\nDone.")
            self.final_p()

if __name__ == "__main__":
    try:
        search_term = argv[1].strip()
        depth = int(argv[2]) if len(argv) >= 3 else inf
    except IndexError:
        search_term = input('What do you want to search?\n>').strip()
        try:
            depth = int(input('Depth of search:\n'))
            assert depth >= 0
        except: depth = inf
    obj = find(search_term, depth)
    obj.go(os.path.abspath(os.curdir))








