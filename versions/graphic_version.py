from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QWidget,\
                            QLabel, QPushButton, QTextEdit, QFileDialog,\
                            QMessageBox, QProgressBar, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from search.searcher import FuzzySearch
import sys


class OpenButton(QPushButton):
    def __init__(self, name, font, textedit):
        super().__init__(name, font=font)
        self.textedit = textedit
        self.clicked.connect(self.open_dialog)

    def open_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            with open(fname[0], 'r') as f:
                data = f.read()
                self.textedit.setText(data)


class FindButton(QPushButton):
    def __init__(self, name, font, window):
        super().__init__(name, font=font)
        self.textedit = window.text_edit
        self.wordsedit = window.words_edit
        self.resultedit = window.result_edit
        self.casebox = window.case_sensitive_checkbox
        self.viewbox = window.view_checkbox
        self.openbtns = [window.open_btn1, window.open_btn2]
        self.progress_bar = window.progress_bar
        self.clicked.connect(self.find_insertions)

    def enable(self):
        self.setEnabled(True)
        [openbtn.setEnabled(True) for openbtn in self.openbtns]

    def disable(self):
        self.setDisabled(True)
        [openbtn.setDisabled(True) for openbtn in self.openbtns]

    def connect_signals_to_slots(self):
        self.fuzzy_search.sig_words_count.connect(self.progress_bar.setMaximum)
        self.fuzzy_search.sig_step.connect(self.progress_bar.setValue)
        self.fuzzy_search.sig_done.connect(self.enable)
        self.fuzzy_search.sig_insertions.connect(self.resultedit.setText)
        self.fuzzy_search.sig_insertions_indexes.connect(self.text_editor.mark)

    def find_insertions(self):
        text = self.textedit.toPlainText()
        words = self.wordsedit.toPlainText()
        if text == '':
            QMessageBox.information(self, 'Нет текста',
                                    'Текст не был введен. \nВведите текст.')
        elif words == '':
            QMessageBox.information(self, 'Нет слов',
                                    'Слова не были введены. \n'
                                    'Введите слова через запятую.')
        else:
            self.disable()
            self.progress_bar.setValue(0)
            self.text_editor = TextEditor(text, self.textedit)
            self.fuzzy_search = FuzzySearch(text, words,
                                            self.casebox.checkState(),
                                            self.viewbox.checkState(), '')
            self.connect_signals_to_slots()
            self.fuzzy_search.start()


class TextEditor:
    def __init__(self, text, textedit):
        self.text = text
        self.textedit = textedit

    def mark(self, to_mark):
        self.textedit.clear()
        current_index = 0
        for item in to_mark:
            self.write_not_marked_text(self.text[current_index:item[0]])
            self.write_marked_text(self.text[item[0]:item[1]])
            current_index = item[1]
        self.write_not_marked_text(self.text[current_index:])

    def write_not_marked_text(self, text):
        font = QFont("Times", 10)
        font.setItalic(False)
        font.setBold(False)
        self.textedit.setCurrentFont(font)
        self.textedit.setTextColor(Qt.black)
        self.textedit.insertPlainText(text)

    def write_marked_text(self, text):
        font = QFont("Times", 10)
        font.setItalic(True)
        font.setBold(True)
        self.textedit.setCurrentFont(font)
        self.textedit.setTextColor(Qt.red)
        self.textedit.insertPlainText(text)


class Window(QWidget):
    def __init__(self, font):
        super().__init__()
        self.standard_font = font
        self.text_edit_font = QFont("Times", 10)

        text_label = QLabel("Введите или откройте текст",
                            font=self.standard_font)
        words_label = QLabel("Введите или откройте слова (через запятую)",
                             font=self.standard_font)
        result_label = QLabel("Результат",
                              font=self.standard_font)

        self.text_edit = QTextEdit(font=self.text_edit_font)
        self.words_edit = QTextEdit(font=self.text_edit_font)
        self.result_edit = QTextEdit(font=self.text_edit_font)

        self.case_sensitive_checkbox = QCheckBox('Учитывать регистр')
        self.case_sensitive_checkbox.setFont(self.standard_font)

        self.view_checkbox = QCheckBox('Построчно')
        self.view_checkbox.setFont(self.standard_font)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.open_btn1 = OpenButton("Открыть", self.standard_font,
                                    self.text_edit)
        self.open_btn2 = OpenButton("Открыть", self.standard_font,
                                    self.words_edit)
        find_btn = FindButton("Найти слова в тексте", self.standard_font, self)

        text_label_box = QHBoxLayout()
        text_label_box.addWidget(text_label, alignment=Qt.AlignLeft)
        text_label_box.addWidget(self.open_btn1, alignment=Qt.AlignRight)

        words_label_box = QHBoxLayout()
        words_label_box.addWidget(words_label, alignment=Qt.AlignLeft)
        words_label_box.addWidget(self.open_btn2, alignment=Qt.AlignRight)

        words_box = QVBoxLayout()
        words_box.addLayout(words_label_box)
        words_box.addWidget(self.words_edit)

        result_box = QVBoxLayout()
        result_box.addWidget(result_label, alignment=Qt.AlignLeft)
        result_box.addWidget(self.result_edit)

        bottom_box = QHBoxLayout()
        bottom_box.addLayout(words_box)
        bottom_box.addLayout(result_box)

        find_and_progress_box = QHBoxLayout()
        find_and_progress_box.addWidget(find_btn, alignment=Qt.AlignLeft)
        find_and_progress_box.addWidget(self.case_sensitive_checkbox)
        find_and_progress_box.addWidget(self.view_checkbox)
        find_and_progress_box.addWidget(self.progress_bar)

        main_box = QVBoxLayout()
        main_box.addLayout(text_label_box)
        main_box.addWidget(self.text_edit)
        main_box.addLayout(bottom_box)
        main_box.addLayout(find_and_progress_box)

        self.setLayout(main_box)

        self.setGeometry(300, 300, 1100, 700)
        self.setWindowTitle('Нечеткий поиск')
        self.show()


def start_application():
    app = QApplication(sys.argv)
    w = Window(QFont("Times", 12))
    sys.exit(app.exec_())
