from unittest import TestCase
from search.searcher import FuzzySearch


class TestGetInsertionsInfo(TestCase):

    def create_fuzzy_search_object(self, text, words, case_sensitive, view):
        self.f = FuzzySearch(text, words, case_sensitive, view, 'test')
        self.f.sig_insertions.connect(self.get_insertions_info)
        self.f.get_insertions_info(text, words)

    def get_insertions_info(self, info):
        self.actual_info = info

    def test_empty_text_and_words(self):
        text = ''
        words = ''
        case_sensitive = False
        view = False
        self.create_fuzzy_search_object(text, words, case_sensitive, view)
        self.assertEqual('Не были введены слова', self.actual_info)

    def test_filled_text_empty_words(self):
        text = 'text'
        words = ''
        case_sensitive = False
        view = False
        self.create_fuzzy_search_object(text, words, case_sensitive, view)
        self.assertEqual('Не были введены слова', self.actual_info)

    def test_empty_text_filled_words(self):
        text = ''
        words = 'words'
        case_sensitive = False
        view = False
        self.create_fuzzy_search_object(text, words, case_sensitive, view)
        self.assertEqual('Вы искали слово "words"\n'
                         '  По этому запросу не было найдено слов\n',
                         self.actual_info)

    def test_one_word_in_text(self):
        text = 'text includes one necessary word'
        words = 'word'
        case_sensitive = False
        view = False
        self.create_fuzzy_search_object(text, words, case_sensitive, view)
        expected_info = 'Вы искали слово "word"\n' \
                        '  По этому запросу были найдены слова:\n' \
                        '   "word" на позициях: 28\n'
        self.assertEqual(expected_info, self.actual_info)

    def test_view_one_word_in_text(self):
        text = 'text includes one necessary word'
        words = 'word'
        case_sensitive = False
        view = True
        self.create_fuzzy_search_object(text, words, case_sensitive, view)
        expected_info = 'Вы искали слово "word"\n' \
                        '  По этому запросу были найдены слова:\n' \
                        '   "word" на позициях:\n' \
                        '      строка 1 позиция 28\n'
        self.assertEqual(expected_info, self.actual_info)

    def test_several_same_words_in_text(self):
        text = 'this text includes first necessary word and' \
               ' second necessary word'
        words = 'word'
        case_sensitive = False
        view = False
        self.create_fuzzy_search_object(text, words, case_sensitive, view)
        expected_info = 'Вы искали слово "word"\n' \
                        '  По этому запросу были найдены слова:\n' \
                        '   "word" на позициях: 35, 61\n'
        self.assertEqual(expected_info, self.actual_info)

    def test_view_several_same_words_in_text(self):
        text = 'this text includes first necessary word and' \
               ' second necessary word'
        words = 'word'
        case_sensitive = False
        view = True
        self.create_fuzzy_search_object(text, words, case_sensitive, view)
        expected_info = 'Вы искали слово "word"\n' \
                        '  По этому запросу были найдены слова:\n' \
                        '   "word" на позициях:\n' \
                        '      строка 1 позиция 35\n' \
                        '      строка 1 позиция 61\n'
        self.assertEqual(expected_info, self.actual_info)

    def test_different_words_in_text(self):
        text = 'It rains cats and dogs'
        words = 'cat, dog'
        case_sensitive = False
        view = False
        self.create_fuzzy_search_object(text, words, case_sensitive, view)
        expected_info = 'Вы искали слово "cat"\n' \
                        '  По этому запросу были найдены слова:\n' \
                        '   "cats" на позициях: 9\n' \
                        'Вы искали слово "dog"\n' \
                        '  По этому запросу были найдены слова:\n' \
                        '   "dogs" на позициях: 18\n'
        self.assertEqual(expected_info, self.actual_info)

    def test_view_different_words_in_text(self):
        text = 'It rains cats and dogs'
        words = 'cat, dog'
        case_sensitive = False
        view = True
        self.create_fuzzy_search_object(text, words, case_sensitive, view)
        expected_info = 'Вы искали слово "cat"\n' \
                        '  По этому запросу были найдены слова:\n' \
                        '   "cats" на позициях:\n' \
                        '      строка 1 позиция 9\n' \
                        'Вы искали слово "dog"\n' \
                        '  По этому запросу были найдены слова:\n' \
                        '   "dogs" на позициях:\n' \
                        '      строка 1 позиция 18\n'
        self.assertEqual(expected_info, self.actual_info)


class TestFindInsertions(TestCase):
    def test_empty_text_and_words(self):
        text = ''
        words = ''
        case_sensitive = False
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions(text, words)
        expected_insertions = {}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_filled_text_empty_words(self):
        text = 'there is some text'
        words = ''
        case_sensitive = False
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions(text, words)
        expected_insertions = {}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_empty_text_filled_words(self):
        text = ''
        words = 'word'
        case_sensitive = False
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions(text, words)
        expected_insertions = {'word': {}}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_filled_text_filled_words(self):
        text = 'The too many levels of recursion error occurs when' \
               ' a statement or routine calls itself too many times.'
        words = 'too, many, times, the'
        case_sensitive = False
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions(text, words)
        expected_insertions = {'many': {'many': [8, 91]}, 'the': {'the': [0]},
                               'times': {'times': [96]},
                               'too': {'too': [4, 87]}}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_case_sensitive(self):
        text = 'For the past twenty years, Daryl Kelly has been imprisoned ' \
               'in New York State for a crime that may never have happened.'
        words = 'Daryl, York, happened'
        case_sensitive = True
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions(text, words)
        expected_insertions = {'Daryl': {'Daryl': [27]},
                               'York': {'York': [66]},
                               'happened': {'happened': [109]}}
        self.assertEqual(expected_insertions, actual_insertions)


class TestFindInsertionsOfOneWord(TestCase):
    def test_empty_text_no_words(self):
        text = ""
        words = ""
        case_sensitive = False
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("")
        expected_insertions = {'': [0]}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_empty_text(self):
        text = ""
        words = "word"
        case_sensitive = False
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("word")
        expected_insertions = {}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_empty_text_with_view(self):
        text = ""
        words = "word"
        case_sensitive = False
        view = True
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("word")
        expected_insertions = {}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_one_insertion(self):
        text = "text with word"
        words = "word"
        case_sensitive = False
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("word")
        expected_insertions = {'word': [10]}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_one_insertion_with_view(self):
        text = "text with word"
        words = "word"
        case_sensitive = False
        view = True
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("word")
        expected_insertions = {'word': [(1, 10)]}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_many_insertions(self):
        text = "text with word, actually there are eight words"
        words = "word"
        case_sensitive = False
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("word")
        expected_insertions = {'word': [10], 'words': [41]}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_many_insertions_with_view(self):
        text = "text with word, actually there are eight words"
        words = "word"
        case_sensitive = False
        view = True
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("word")
        expected_insertions = {'word': [(1, 10)], 'words': [(1, 41)]}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_many_insertions_in_different_rows(self):
        text = "let's find a word\n" \
               "and one more word"
        words = "word"
        case_sensitive = False
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("word")
        expected_insertions = {'word': [13, 31]}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_many_insertions_in_different_rows_with_view(self):
        text = "let's find a word\n" \
               "and one more word"
        words = "word"
        case_sensitive = False
        view = True
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("word")
        expected_insertions = {'word': [(1, 13), (2, 13)]}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_insertions_another_word(self):
        text = "let's find a man in a pacman"
        words = "man"
        case_sensitive = False
        view = False
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("man")
        expected_insertions = {'man': [13], 'pacman': [25]}
        self.assertEqual(expected_insertions, actual_insertions)

    def test_insertions_another_word_with_view(self):
        text = "let's find a man in a pacman"
        words = "man"
        case_sensitive = False
        view = True
        f = FuzzySearch(text, words, case_sensitive, view, 'test')
        actual_insertions = f.find_insertions_of_word("man")
        expected_insertions = {'man': [(1, 13)], 'pacman': [(1, 25)]}
        self.assertEqual(expected_insertions, actual_insertions)
