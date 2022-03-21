#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===============================================
GSP (Generalized Sequential Pattern) algorithm
===============================================
GSP algorithm made with Python3 to deal with arrays as transactions.
Example:
transactions = [
                ['Bread', 'Milk'],
                ['Bread', 'Diaper', 'Beer', 'Eggs'],
                ['Milk', 'Diaper', 'Beer', 'Coke'],
                ['Bread', 'Milk', 'Diaper', 'Beer'],
                ['Bread', 'Milk', 'Diaper', 'Coke']
            ]
"""

import logging
import multiprocessing as mp
from collections import Counter
from itertools import chain
from itertools import product
import pandas as pd
import math
import numpy as np

__author__ = "Jackson Antonio do Prado Lima"
__email__ = "jacksonpradolima@gmail.com"
__license__ = "GPL"
__version__ = "1.0"


class GSP:

    def __init__(self, raw_transactions):
        self.freq_patterns = []
        self._pre_processing(raw_transactions)
        self.numRows = 0
        self.minAbsSup = 100
        self.minRelSup = 0.01

    def _pre_processing(self, raw_transactions):
        '''
        Prepare the data
        Parameters:
                raw_transactions: the data that it will be analysed
        '''
        self.max_size = max([len(item) for item in raw_transactions])
        self.transactions = [tuple(list(i)) for i in raw_transactions]
        counts = Counter(chain.from_iterable(raw_transactions))
        self.unique_candidates = [tuple([k]) for k, c in counts.items()]

    def _is_slice_in_list(self, s, l):
        len_s = len(s)  # so we don't recompute length of s on every iteration
        return any(s == l[i:len_s + i] for i in range(len(l) - len_s + 1))

    def _calc_frequency(self, results, item, minsup):
        # The number of times the item appears in the transactions
        frequency = len(
            [t for t in self.transactions if self._is_slice_in_list(item, t)])
        if frequency >= minsup:
            results[item] = frequency
        return results

    def _support(self, items, minsup=0):
        '''
        The support count (or simply support) for a sequence is defined as
        the fraction of total data-sequences that "contain" this sequence.
        (Although the word "contains" is not strictly accurate once we
        incorporate taxonomies, it captures the spirt of when a data-sequence
        contributes to the support of a sequential pattern.)
        Parameters
                items: set of items that will be evaluated
                minsup: minimum support
        '''
        results = mp.Manager().dict()
        pool = mp.Pool(processes=mp.cpu_count())

        for item in items:
            pool.apply_async(self._calc_frequency,
                             args=(results, item, minsup))
        pool.close()
        pool.join()

        return dict(results)

    def _print_status(self, run, candidates):
        logging.debug("""
        Run {}
        There are {} candidates.
        The candidates have been filtered down to {}.\n"""
                      .format(run,
                              len(candidates),
                              len(self.freq_patterns[run - 1])))

    def search(self, minsup=0.2):
        '''
        Run GSP mining algorithm
        Parameters
                minsup: minimum support
        '''
        assert (0.0 < minsup) and (minsup <= 1.0)
        minsup = len(self.transactions) * minsup
        # the set of frequent 1-sequence: all singleton sequences
        # (k-itemsets/k-sequence = 1) - Initially, every item in DB is a
        # candidate
        candidates = self.unique_candidates
        #print(candidates)
        # scan transactions to collect support count for each candidate
        # sequence & filter
        self.freq_patterns.append(self._support(candidates, minsup))

        # (k-itemsets/k-sequence = 1)
        k_items = 1

        self._print_status(k_items, candidates)

        # repeat until no frequent sequence or no candidate can be found
        while len(self.freq_patterns[k_items - 1]) and (k_items + 1 <= self.max_size):
            print("repeatExpansion")
            k_items += 1

            # Generate candidate sets Ck (set of candidate k-sequences) -
            # generate new candidates from the last "best" candidates filtered
            # by minimum support
            items = np.unique(
                list(set(self.freq_patterns[k_items - 2].keys())))
            print("afterlist")
            candidates = list(product(items, repeat=k_items))
            print("candidates")
            # candidate pruning - eliminates candidates who are not potentially
            # frequent (using support as threshold)
            self.freq_patterns.append(self._support(candidates, minsup))
            print("freq")
            self._print_status(k_items, candidates)
        return self.freq_patterns[:-1]

def main():
    '''Reads text file and sets minAbsSup to be correct'''
    filepath = "mp2_ContSeqPatterns\\review_samples.txt"
    nrows_ = 10
    df = pd.read_csv(filepath,header=None,sep="\n",nrows=nrows_)
    listDF = df[0].str.split(" ",expand=True)
    list_ = listDF.values.tolist()
    filtList = []
    for l in list_:
        filtered_list = list(filter(None,l))
        filtList.append(filtered_list)
    print("finishedReading")
    pipe = GSP(filtList)
    result = pipe.search(0.1)
    print(result)

if __name__ == "__main__":
    main()