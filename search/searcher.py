from search.text_methods import transform_text_to_dict,\
                                transform_text_to_dict_rowly, \
                                transform_words_to_list, \
                                are_optimal_shifts
from PyQt5.QtCore import pyqtSignal, QThread


class FuzzySearch(QThread):
    sig_words_count = pyqtSignal(int)
    sig_step = pyqtSignal(int)
    sig_done = pyqtSignal()
    sig_insertions = pyqtSignal(str)
    sig_insertions_indexes = pyqtSignal(list)

    def __init__(self, text, words, case_sensitive, view, mode):
        super().__init__()
        self.mode = mode
        self.text = text
        self.words = words
        self.case_sensitive = case_sensitive
        self.view = view
        self.insertions_indexes = {}
        if self.mode == 'test':
            self.text_dict = transform_text_to_dict(text, self.case_sensitive)
            self.row_text_dict = transform_text_to_dict_rowly(
                text, self.case_sensitive)
        else:
            self.text_dict = {}
            self.row_text_dict = {}
        self.ticks = 1

    def run(self):
        if self.mode != 'test':
            self.text_dict = transform_text_to_dict(self.text,
                                                    self.case_sensitive)
            self.row_text_dict = transform_text_to_dict_rowly(
                self.text, self.case_sensitive)
        self.get_insertions_info(self.text, self.words)

    def find_insertions_of_word(self, word):
        word_insertions = {}
        count = 1
        for textword in self.text_dict.keys():
            if count % 1000 == 0:
                self.sig_step.emit(self.ticks)
                self.ticks += 1
            are_optimal, start_shift, end_shift = \
                are_optimal_shifts(textword, word)
            if are_optimal:
                if self.view:
                    word_insertions[textword] = \
                        [(pair[0], pair[1] + start_shift)
                         for pair in self.row_text_dict[textword]]
                else:
                    word_insertions[textword] = \
                        [index + start_shift
                         for index in self.text_dict[textword]]
                for index in self.text_dict[textword]:
                    self.insertions_indexes[index+start_shift] = \
                        index + len(textword) + end_shift
            count += 1
        return word_insertions

    '''Получение информации о вхождениях слов в текст'''
    def find_insertions(self, text, words):
        insertions = {}
        if words == '':
            self.insertions_indexes = []
            return {}
        words_list = transform_words_to_list(words, self.case_sensitive)
        ticks_count = (len(words_list) +
                       len(words_list) * (len(self.text_dict.keys())//1000))
        self.sig_words_count.emit(ticks_count)
        for word in words_list:
            insertions[word] = self.find_insertions_of_word(word)
            self.sig_step.emit(self.ticks)
            self.ticks += 1
        self.insertions_indexes = sorted(self.insertions_indexes.items())
        return insertions

    '''Получение информации о вхождениях слов в текст в текстовом формате'''
    def get_insertions_info(self, text, words):
        insertions = self.find_insertions(text, words)
        insertions_info = ''
        if not len(insertions.keys()):
            insertions_info = 'Не были введены слова'
        for word in insertions.keys():
            insertions_info += 'Вы искали слово "' + word + '"\n'
            if not insertions[word]:
                insertions_info += '  По этому запросу не было найдено слов\n'
            else:
                insertions_info += '  По этому запросу были найдены слова:\n'
                for textword in insertions[word].keys():
                    if self.view:
                        insertions_info += '   "' + textword + \
                                           '" на позициях:\n'
                        insertions_info += \
                            "\n".join(["      строка " + str(pair[0]) +
                                      " позиция " + str(pair[1])
                                       for pair in insertions[word][textword]])
                        insertions_info += "\n"
                    else:
                        insertions_info += '   "' + textword + \
                                           '" на позициях: '
                        insertions_info += \
                            ", ".join([str(i)
                                       for i in insertions[word][textword]])
                        insertions_info += '\n'
        self.sig_insertions.emit(insertions_info)
        self.sig_done.emit()
        self.sig_insertions_indexes.emit(self.insertions_indexes)
        self.quit()
