from dataclasses import dataclass
from typing import  Sequence

@dataclass
class FromWhere:
    indices:tuple[int,int] = (-1,-1)
    modification: str = "None"

class DamerauLevenshtein[T]:

    def __init__(self, a: Sequence[T], b: Sequence[T]):
        self.seq1 = a
        self.seq2 = b
        self.distance_matrix, self.from_where = self._compute_damerau_levenshtein_distance_matrix(a,b)
        # self.from_where = None

    def _compute_damerau_levenshtein_distance_matrix[T](self, a: Sequence[T], b: Sequence[T]):
        # taken from: https://gist.github.com/badocelot/5327337
        # "Infinity" -- greater than maximum possible edit distance
        # Used to prevent transpositions for first characters
        INF = len(a) + len(b)

        # Matrix: (M + 2) x (N + 2)
        matrix = [[INF for n in range(len(b) + 2)]]
        matrix += [[INF] + list(range(len(b) + 1))]
        matrix += [[INF, m] + [0] * len(b) for m in range(1, len(a) + 1)]

        # initialize from where matrix
        from_where = [[FromWhere() for _col  in _row] for _row in matrix]
        # the "upper left" corner is empty string and empty string, so we replace nothing
        # with nothing
        from_where[1][1] = FromWhere((1,1), 'Leave Alone')
        # going across a row is an insertion
        for j in range(2, len(from_where[1])):
            from_where[1][j] = FromWhere((1,j-1), 'Insertion')

        # going down a column in a deletion
        for i in range(2, len(from_where)):
            from_where[i][1] = FromWhere((i-1, 1), 'Deletion')



        # Holds last row each element was encountered: `DA` in the Wikipedia pseudocode
        last_row = {}

        # Fill in costs
        for row in range(1, len(a) + 1):
            # Current character in `a`
            ch_a = a[row - 1]

            # Column of last match on this row: `DB` in pseudocode
            last_match_col = 0

            for col in range(1, len(b) + 1):
                # Current character in `b`
                ch_b = b[col - 1]

                # Last row with matching character; `i1` in pseudocode
                last_matching_row = last_row.get(ch_b, 0)

                # Cost of substitution
                cost = 0 if ch_a == ch_b else 1

                # Compute substring distance

                substitution_cost = matrix[row][col] + cost
                addition_cost = matrix[row + 1][col] + 1
                deletion_cost = matrix[row][col + 1] + 1
                transposition_cost = (matrix[last_matching_row][last_match_col]
                                      + (row - last_matching_row - 1) + 1
                                      + (col - last_match_col - 1))

                best_modification_cost = min(substitution_cost, addition_cost, deletion_cost, transposition_cost)

                matrix[row + 1][col + 1] = best_modification_cost

                if best_modification_cost == substitution_cost:
                    modification = 'Leave Alone' if cost == 0 else 'Substitution'
                    # cur_mod = from_where[row][col].modification
                    # modification = modification if cur_mod == "None" else cur_mod
                    from_where[row + 1][col + 1] = FromWhere((row,col), modification)
                elif best_modification_cost == addition_cost:
                    from_where[row + 1][col + 1] = FromWhere((row + 1, col), 'Insertion')
                elif best_modification_cost == deletion_cost:
                    from_where[row + 1][col + 1] = FromWhere((row,col+1), 'Deletion')
                else: # best_modification_cost == transposition_cost
                    from_where[row + 1][col + 1] =  FromWhere((last_matching_row ,last_match_col), 'Transposition')

                # If there was a match, update last_match_col
                # Doing this here lets me be rid of the `j1` variable from the original pseudocode
                if cost == 0:
                    last_match_col = col

            # Update last row for current character
            last_row[ch_a] = row

                # Return last element

        return matrix,from_where
        # return matrix[-1][-1]
