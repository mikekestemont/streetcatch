#!usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


PATH_MASTER_FILE = '../data/master_list.txt'
PATH_INPUT_FILE = '../data/new_input.xlsx'
PATH_OUTPUT_FILE = '../data/norm.xlsx'

def main():
    print('::: started :::')
    # parse index:
    idx = {}
    for line in open(PATH_MASTER_FILE, 'r'):
        line = line.strip()
        if line:
            try:
                key, variants = line.split('|')
            except ValueError:
                continue
            key = key.lower().capitalize().strip()
            variants = {s.lower().strip() for s in variants.split(',') if s.strip()}
            variants.add(key.lower().strip())
            for var in variants:
                try:
                    idx[var].add(key)
                except KeyError:
                    idx[var] = set()
                    idx[var].add(key)
    
    # check for ambiguity:
    print("Ambiguous entries:")
    for variant in idx:
        if len(idx[variant]) > 2:
            print(variant, '>', idx[variant])

    # parse input:
    df = pd.read_excel(PATH_INPUT_FILE)
    norm_names = []
    for streetname in list(df['Street']):
        if not isinstance(streetname, str):
            norm_names.append('NA')
            continue
        print(streetname)
        streetname = streetname.lower()
        if streetname in idx:
            norm = ' -- '.join(sorted(idx[streetname]))
            norm_names.append(norm)
        else:
            norm_names.append('NA')
    for norm in norm_names:
        print(norm)

    # add new row:
    df.insert(len(df.columns), 'norm', norm_names)
    df.to_excel(PATH_OUTPUT_FILE)
    print('::: ended :::')
    
if __name__ == '__main__':
    main()
