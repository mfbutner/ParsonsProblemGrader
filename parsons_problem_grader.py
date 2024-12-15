from typing import Sequence
from damerau_levenshtein import DamerauLevenshtein


def find_longest_common_substring[T](str1: Sequence[T], str2: Sequence[T]) -> tuple[int, int, int]:
    # Get lengths of the strings
    m, n = len(str1), len(str2)

    # Create a 2D DP table to store lengths of common substrings
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Variables to store the length and the ending indices of the longest substring
    max_length = 0
    end_index_str1 = 0
    end_index_str2 = 0

    # Build the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:  # Check for matching characters
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_index_str1 = i
                    end_index_str2 = j
            else:
                dp[i][j] = 0  # No match, reset to 0

    # Calculate the starting indices of the substring in both strings
    start_index_str1 = end_index_str1 - max_length
    start_index_str2 = end_index_str2 - max_length

    return max_length, start_index_str1, start_index_str2


def gpt_damerau_levenshtein[T](s1: Sequence[T], s2: Sequence[T]):
    # Lengths of the input strings
    len1, len2 = len(s1), len(s2)

    # Initialize the DP table with (cost, edits)
    dp = [[(0, []) for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    # Base case: cost to transform to/from an empty string
    for i in range(1, len1 + 1):
        dp[i][0] = (i, dp[i - 1][0][1] + [f"delete {s1[i - 1]} from position {i - 1}"])
    for j in range(1, len2 + 1):
        dp[0][j] = (j, dp[0][j - 1][1] + [f"insert {s2[j - 1]} at position {j - 1}"])

    # Fill the DP table
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost_substitute = 0 if s1[i - 1] == s2[j - 1] else 1

            # Costs for basic operations
            cost_delete = dp[i - 1][j][0] + 1
            cost_insert = dp[i][j - 1][0] + 1
            cost_substitute = dp[i - 1][j - 1][0] + cost_substitute

            # Find the minimum cost and corresponding operation
            operations = [
                (cost_delete, dp[i - 1][j][1] + [f"delete {s1[i - 1]} from position {i - 1}"]),
                (cost_insert, dp[i][j - 1][1] + [f"insert {s2[j - 1]} at position {j - 1}"]),
                (cost_substitute, dp[i - 1][j - 1][1] + (
                    [f"substitute {s1[i - 1]} with {s2[j - 1]} at position {i - 1}"] if cost_substitute -
                                                                                        dp[i - 1][j - 1][
                                                                                            0] == 1 else [])),
            ]

            # Add transposition if possible
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                cost_transpose = dp[i - 2][j - 2][0] + 1
                operations.append((cost_transpose, dp[i - 2][j - 2][1] + [
                    f"transpose {s1[i - 2]} and {s1[i - 1]} at positions {i - 2} and {i - 1}"]))

            # Choose the operation with the minimum cost
            dp[i][j] = min(operations, key=lambda x: x[0])

    # Result: minimum edit distance and operations to achieve it
    return dp[len1][len2]


def parsons_problem_grader(answer_key: str, student_answer: str):
    answer_key = list(answer_key)
    student_answer = list(student_answer)

    length, answer_key_start_index, student_answer_start_index = find_longest_common_substring(answer_key,
                                                                                               student_answer)
    while length > 1:
        common_string = tuple(answer_key[answer_key_start_index:answer_key_start_index + length])
        answer_key[answer_key_start_index:answer_key_start_index + length] = [common_string]
        student_answer[student_answer_start_index:student_answer_start_index + length] = [common_string]
        length, answer_key_start_index, student_answer_start_index = find_longest_common_substring(answer_key,
                                                                                                   student_answer)
    penalties = my_damerau_levenshtein(answer_key, student_answer)
    return penalties


def test_parsons_problem_grader():
    s1 = "geeksforgeeks"
    s2 = "ggeegeeksquizpractice"

    print(parsons_problem_grader(s1, s2))


# def test_longest_substring_code():
#     s1 = "c"
#     s2 = "a"
#     length, start_index1, start_index2 = find_longest_common_substring(s1, s2)
#     print(f"""    The longest string is {s1[start_index1:start_index1 + length]}
#     Length: {length},
#     Start Index in str1: {start_index1},
#     Start Index in str2: {start_index2}
# """)

def test_my_damerau_levenshtein():
    # from textdistance import DamerauLevenshtein
    # DamerauLevenshtein()
    s1 = "a cat"
    s2 = "an abct"
    dl = DamerauLevenshtein(s1, s2)
    print(dl.distance_matrix[-1][-1])
    # distance = my_damerau_levenshtein(s1, s2)
    # print(distance)


# def test_damerau_levenshtein():
#     s1 = "ca"
#     s2 = "abc"
#     distance, edits = damerau_levenshtein(s1, s2)
#     print(f"Distance: {distance}")
#     print("Edits:")
#     for edit in edits:
#         print(f"  - {edit}")



if __name__ == '__main__':
    # test_longest_substring_code()
    # test_parsons_problem_grader()
    test_my_damerau_levenshtein()
    # print(damerau_levenshtein_distance("a","anba"))
