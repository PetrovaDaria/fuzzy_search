from search.searcher import FuzzySearch
from progress_bar import print_progress_bar
import sys


class ConsoleVersion:

    def __init__(self, text, words, register, view):
        self.text = text
        self.words = words
        self.register = register
        self.view = view
        self.total_progress_size = 0
        self.iteration = 0

    def search_words_in_text(self):
        if type(self.words) is str:
            with open(self.text, 'r') as t:
                self.f = FuzzySearch(t.read(), self.words,
                                     self.register, self.view, '')
                self.f.sig_words_count.connect(self.get_total_progress_size)
                self.f.sig_step.connect(self.make_step)
                self.f.sig_insertions.connect(self.get_insertions)
                self.f.sig_done.connect(self.continuation)
                self.f.start()
        else:
            with open(self.text, 'r') as t:
                with self.words:
                    self.f = FuzzySearch(t.read(), self.words.read(),
                                         self.register, self.view, '')
                    self.f.sig_words_count.connect(
                        self.get_total_progress_size)
                    self.f.sig_step.connect(self.make_step)
                    self.f.sig_insertions.connect(self.get_insertions)
                    self.f.sig_done.connect(self.finish)
                    self.f.start()

    def get_total_progress_size(self, size):
        self.total_progress_size = size
        print_progress_bar(self.iteration, self.total_progress_size)

    def make_step(self, step):
        self.iteration += 1
        print_progress_bar(self.iteration, self.total_progress_size)

    def continuation(self):
        self.total_progress_size = 0
        self.iteration = 0
        try:
            self.words = input()
        except KeyboardInterrupt:
            self.finish()
        self.search_words_in_text()

    def get_insertions(self, insertions):
        print(insertions)

    def finish(self):
        sys.exit(0)
