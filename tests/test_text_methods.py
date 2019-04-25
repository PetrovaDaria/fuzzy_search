from unittest import TestCase
from search.text_methods import transform_text_to_dict,\
                                transform_text_to_dict_rowly, \
                                transform_words_to_list, \
                                find_distance, is_optimal_distance, \
                                find_optimal_shifts


class TestTextToDictMethods(TestCase):

    def assert_dicts_equality(self, text, case_sensitivity, expected):
        text_dict = transform_text_to_dict(text, case_sensitivity)
        self.assertEqual(text_dict, expected)

    def assert_dict_key_result(self, text, word, case_sensitivity, expected):
        text_dict = transform_text_to_dict(text, case_sensitivity)
        self.assertEqual(text_dict[word], expected)

    def test_empty_text(self):
        self.assert_dicts_equality('', False, {'': [0]})

    def test_lower_case_letters_not_case_sensitive(self):
        self.assert_dicts_equality('a b c', False,
                                   {'a': [0], 'b': [2], 'c': [4]})

    def test_lower_case_letters_case_sensitive(self):
        self.assert_dicts_equality('a b c', True,
                                   {'a': [0], 'b': [2], 'c': [4]})

    def test_capital_letters_case_sensitive(self):
        self.assert_dicts_equality('A B C', True,
                                   {'A': [0], 'B': [2], 'C': [4]})

    def test_capital_letters_not_case_sensitive(self):
        self.assert_dicts_equality('A B C', False,
                                   {'a': [0], 'b': [2], 'c': [4]})

    def test_lower_case_repeated_words(self):
        self.assert_dicts_equality('dog cat cow dog cat dog', False,
                                   {'dog': [0, 12, 20], 'cat': [4, 16],
                                    'cow': [8]})

    def test_different_case_repeated_words(self):
        self.assert_dicts_equality('dog Cat cow Dog cat dog', True,
                                   {'dog': [0, 20], 'cat': [16], 'cow': [8],
                                    'Dog': [12], 'Cat': [4]})

    def test_punctuation(self):
        self.assert_dict_key_result('(Oh, do do do, oh, do do do)', 'oh',
                                    False, [1, 15])

    def test_apostrop_and_hyphen(self):
        self.assert_dict_key_result('Santa’s coming to town - '
                                    'Santa’s coming for us', "Santa’s",
                                    True, [0, 25])


class TestTextToDictRowly(TestCase):

    def assert_dicts_equality(self, text, case_sensitivity, expected):
        text_dict_rowly = transform_text_to_dict_rowly(text, case_sensitivity)
        self.assertEqual(text_dict_rowly, expected)

    def test_empty_text(self):
        self.assert_dicts_equality('', False, {'': [(1, 0)]})

    def test_simple_text(self):
        self.assert_dicts_equality(
            'a b c', False, {'a': [(1, 0)], 'b': [(1, 2)], 'c': [(1, 4)]})

    def test_different_register(self):
        self.assert_dicts_equality(
            'a A b B c C', False,
            {'a': [(1, 0), (1, 2)], 'b': [(1, 4), (1, 6)],
             'c': [(1, 8), (1, 10)]})

    def test_different_register_case_sensitive(self):
        self.assert_dicts_equality(
            'a A b B c C', True,
            {'a': [(1, 0)], 'A': [(1, 2)], 'b': [(1, 4)], 'B': [(1, 6)],
             'c': [(1, 8)], 'C': [(1, 10)]})

    def test_several_rows(self):
        self.assert_dicts_equality(
            'a A b\nB c C', False,
            {'a': [(1, 0), (1, 2)], 'b': [(1, 4), (2, 0)],
             'c': [(2, 2), (2, 4)]})

    def test_several_rows_case_sensitive(self):
        self.assert_dicts_equality(
            'a A b\nB c C', True,
            {'a': [(1, 0)], 'A': [(1, 2)], 'b': [(1, 4)], 'B': [(2, 0)],
             'c': [(2, 2)], 'C': [(2, 4)]})


class TestWordsToListMethods(TestCase):

    def assert_lists_equality(self, words, case_sensitivity, expected):
        words_list = transform_words_to_list(words, case_sensitivity)
        self.assertEqual(words_list, expected)

    def test_empty(self):
        self.assert_lists_equality('', False, [''])

    def test_lower_case_words(self):
        self.assert_lists_equality('first, second, third', False,
                                   ['first', 'second', 'third'])

    def test_different_case_words_sensitive_case(self):
        self.assert_lists_equality('first, Second, Third, fourth', True,
                                   ['Second', 'Third', 'first', 'fourth'])

    def test_different_case_words_not_sensitive_case(self):
        self.assert_lists_equality('first, Second, Third, fourth', False,
                                   ['first', 'fourth', 'second', 'third'])

    def test_repeated_words(self):
        self.assert_lists_equality('first, first, second', False,
                                   ['first', 'second'])

    def test_words_with_apostrophs_and_hyphens(self):
        self.assert_lists_equality("so-so, it's, its", False,
                                   ["it's", 'its', 'so-so'])

    def test_words_with_newlines(self):
        self.assert_lists_equality('first, \n second', False,
                                   ['first', 'second'])

    def test_phrases(self):
        self.assert_lists_equality('first phrase, second phrase', False,
                                   ['first phrase', 'second phrase'])

    def test_punctuation(self):
        self.assert_lists_equality('th:is, t.he, e!nd', False,
                                   ['e!nd', 't.he', 'th:is'])


class TestFindDistanceMethods(TestCase):

    def assert_distances_equality(self, word1, word2, expected_distance):
        distance = find_distance(word1, word2)
        self.assertEqual(distance, expected_distance)

    def test_empty(self):
        self.assert_distances_equality('', '', 0)

    def test_one_empty(self):
        self.assert_distances_equality('hello', '', 5)

    def test_same_words(self):
        self.assert_distances_equality('hello', 'hello', 0)

    def test_delete_letter(self):
        self.assert_distances_equality('hello', 'helo', 1)

    def test_change_letter(self):
        self.assert_distances_equality('hello', 'hillo', 1)

    def test_add_letter(self):
        self.assert_distances_equality('hello', 'helllo', 1)

    def test_replace_two_neighbor_letters(self):
        self.assert_distances_equality('hello', 'helol', 1)


class TestIsOptimalDistanceMethods(TestCase):

    def test_short_words_zero_distance(self):
        self.assertTrue(is_optimal_distance('who', 'who'))

    def test_short_words_one_distance(self):
        self.assertFalse(is_optimal_distance('who', 'wha'))

    def test_medium_words_one_distance(self):
        self.assertTrue(is_optimal_distance('hello', 'hallo'))

    def test_medium_words_two_distance(self):
        self.assertFalse(is_optimal_distance('hello', 'halle'))

    def test_long_words_two_distance(self):
        self.assertTrue(is_optimal_distance('frustrated', 'frestratid'))

    def test_long_words_three_distance(self):
        self.assertFalse(is_optimal_distance('frustrated', 'frestatid'))


class TestFindOptimalShiftsMethods(TestCase):

    def assert_shifts_equality(self, word1, word2, max_diff, expected):
        shifts = find_optimal_shifts(word1, word2, max_diff)
        self.assertEqual(shifts, expected)

    def test_substring_at_beginning(self):
        self.assert_shifts_equality('барабанщик', 'барабан', 3, (0, -3))

    def test_substring_at_end(self):
        self.assert_shifts_equality('микроэкономика', 'экономика', 3, (3, 0))

    def test_similar_words(self):
        self.assert_shifts_equality('шефствовать', 'шествовать', 1, (0, 0))

    def test_same_words(self):
        self.assert_shifts_equality('барабан', 'барабан', 1, (0, 0))

    def test_small_substring(self):
        self.assert_shifts_equality('барабанщик', 'барабан', 0, None)
