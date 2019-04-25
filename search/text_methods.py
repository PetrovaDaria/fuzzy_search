from re import split, sub


def transform_text_to_dict(text, case_sensitive):
    delimiters = '''[!"#$%&()*+,./:;<=>?@[\]^_`{|}~\n\r ]'''
    text_dict = {}
    index = 0
    if case_sensitive:
        splitted_text = split(delimiters, text)
    else:
        splitted_text = split(delimiters, text.lower())
    for element in splitted_text:
        if element not in text_dict:
            text_dict[element] = []
        text_dict[element].append(index)
        index += len(element) + 1
    return text_dict


def transform_text_to_dict_rowly(text, case_sensitive):
    delimiters = '''[!"#$%&()*+,./:;<=>?@[\]^_`{|}~\r ]'''
    text_dict = {}
    if case_sensitive:
        sequences = split('\n', text)
    else:
        sequences = split('\n', text.lower())
    for i in range(len(sequences)):
        splitted_sequence = split(delimiters, sequences[i])
        index = 0
        for element in splitted_sequence:
            if element not in text_dict:
                text_dict[element] = []
            text_dict[element].append((i+1, index))
            index += len(element) + 1
    return text_dict


def transform_words_to_list(words, case_sensitive):
    words = sub("^\s+|\n|\r|\s+$", '', words)
    if case_sensitive:
        return sorted(set(split(' *, *', words)))
    else:
        return sorted(set(split(' *, *', words.lower())))


def find_distance(word1: str, word2: str):
    len1, len2 = len(word1), len(word2)
    if len1 > len2:
        word1, word2 = word2, word1
        len1, len2 = len2, len1
    current_row = range(len1 + 1)
    previous_row = range(len1 + 1)
    pre_previous_row = range(len1 + 1)
    for i in range(1, len2 + 1):
        if i == 1:
            previous_row, current_row = current_row, [i] + [0] * len1
        else:
            pre_previous_row, previous_row, current_row = \
                previous_row, current_row, [i] + [0] * len1
        for j in range(1, len1 + 1):
            add = previous_row[j] + 1
            delete = current_row[j - 1] + 1
            change = previous_row[j - 1]
            if word1[j - 1] != word2[i - 1]:
                change += 1
            if word1[j - 1] == word2[i - 2] and word1[j - 2] == word2[i - 1]:
                transpose = pre_previous_row[j - 2] + 1
                current_row[j] = min(add, delete, change, transpose)
            else:
                current_row[j] = min(add, delete, change)
    return current_row[len1]


def is_optimal_distance(word1: str, word2: str):
    distance = find_distance(word1, word2)
    l = min(len(word1), len(word2))
    return distance <= l // 4


def find_optimal_distances_and_shifts(word1: str, word2: str, diff: int):
    distances = {}
    for current_diff in range(diff, -1, -1):
        for i in range(current_diff, -1, -1):
            start_index = current_diff - i
            end_index = len(word1) - i
            substring = word1[start_index:end_index]
            if is_optimal_distance(substring, word2):
                distances[(start_index, -i)] = find_distance(substring, word2)
    return sorted(distances.items(), key=lambda x: x[1])


def find_optimal_shifts(word1: str, word2: str, diff: int):
    distances = find_optimal_distances_and_shifts(word1, word2, diff)
    if len(distances) > 0:
        return distances[0][0]
    return None


def are_optimal_shifts(word1: str, word2: str):
    diff = len(word1) - len(word2)
    if diff >= 4:
        if is_optimal_distance(word1, word2):
            return (True, 0, 0)
        return (False, 0, 0)
    optimal_substring = find_optimal_shifts(word1, word2, diff)
    if optimal_substring is not None:
        start_shift = optimal_substring[0]
        end_shift = optimal_substring[1]
        return (True, start_shift, end_shift)
    return (False, 0, 0)
