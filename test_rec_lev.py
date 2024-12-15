import unittest
from hypothesis import given, settings, strategies as st
from rec_lev_distance import rec_lev_distance
from textdistance import levenshtein

class TestRecLev(unittest.TestCase):
    @settings(max_examples=1000)
    @given(st.text(max_size=40), st.text(max_size=40))
    def test_rec_lev(self, s1, s2):
        rld = rec_lev_distance(s1,s2)
        ld = levenshtein(s1,s2)
        self.assertEqual(rld, ld)  # add assertion here

if __name__ == '__main__':
    unittest.main()
