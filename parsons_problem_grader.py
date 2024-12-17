from typing import Sequence
from textdistance import DamerauLevenshtein

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
    dl = DamerauLevenshtein(restricted=False)
    penalties = dl.distance(student_answer, answer_key)
    return penalties

def main():
    # answer_key = "APENBIDKMOJGDKHLKCK" # problem 14
    answer_key  = "ECNRBAGFMPQS" # problem 11
    with open('Problem11_Submissions.txt') as student_answers:
        for student_answer in student_answers:
            print(parsons_problem_grader(answer_key, student_answer.strip()))

if __name__ == '__main__':
    main()
