from typing import Sequence
from functools import cache

def rec_lev_distance[T](seq1:Sequence[T], seq2:Sequence[T])->int:
    return _rec_lev_distance(tuple(seq1), tuple(seq2))

@cache
def _rec_lev_distance[T](seq1: tuple[T, ...], seq2: tuple[T, ...])->int:
    if len(seq1) == 0:
        return len(seq2)
    elif len(seq2) == 0:
        return len(seq1)
    elif seq1[0] == seq2[0]:
        return _rec_lev_distance(seq1[1:], seq2[1:])
    else:
        insert_distance = _rec_lev_distance(seq1, seq2[1:])
        deletion_distance = _rec_lev_distance(seq1[1:], seq2)
        substitution_difference = _rec_lev_distance(seq1[1:], seq2[1:])
        return 1 + min(insert_distance, deletion_distance, substitution_difference)

def rec_dev_lev_distance[T](seq1:Sequence[T], seq2:Sequence[T])->int:
    return _rec_dev_lev_distance(tuple(seq1), tuple(seq2))

@cache
def _rec_dev_lev_distance[T](seq1: tuple[T, ...], seq2: tuple[T, ...])->int:
    if len(seq1) == 0:
        return len(seq2)
    elif len(seq2) == 0:
        return len(seq1)
    elif seq1[0] == seq2[0]:
        return _rec_dev_lev_distance(seq1[1:], seq2[1:])
    else:
        insert_distance = _rec_dev_lev_distance(seq1, seq2[1:])
        deletion_distance = _rec_dev_lev_distance(seq1[1:], seq2)
        substitution_distance = _rec_dev_lev_distance(seq1[1:], seq2[1:])
        transposition_distance = len(seq1) + len(seq2) + 1
        if len(seq1) >= 2 and len(seq2) >= 2 and seq1[1] == seq2[1]:
            seq1_with_transposition = (seq1[0],) + seq1[2:]
            seq2_with_transposition = (seq2[0],) + seq2[2:]
            transposition_distance = _rec_dev_lev_distance(seq1_with_transposition, seq2_with_transposition)

        return 1 + min(insert_distance, deletion_distance, substitution_distance, transposition_distance)

if __name__ == '__main__':
    print(rec_dev_lev_distance("a cat", "an abct"))