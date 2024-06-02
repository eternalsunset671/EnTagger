import sys
import re
import os

import time

from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QFileDialog, QTextEdit,
                              QFrame, QPushButton, QWidget, QGridLayout, QVBoxLayout, QSizePolicy)
from PyQt5.QtGui import  QFont, QTextCharFormat, QSyntaxHighlighter, QColor
from PyQt5.QtCore import QMargins, Qt, pyqtSignal

#форматировать под один стиль пунктуацию и непечатные символы а также пересмотреть регулярку и проверить как она отрабавтывает на реальном корпусе
#ключи в словарях содержат пробелы но не учитывают других символов

class EnTagger(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ignore_undo_redo_update = False

        self.title = 'EnTagger'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 500

        self.text = ''
        self.file_name = 'Untitled'
        self.open_status_name = False
        self.selected = False

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(central_widget)

        self.text_editor = TextEdit(self)
        grid_layout.addWidget(self.text_editor, 0, 0, 1, 1)

        self.control_frame = QFrame(self)
        self.control_frame.setStyleSheet("background-color: #f0f0f0;")
        grid_layout.addWidget(self.control_frame, 0, 1)

        button_layout = QVBoxLayout(self.control_frame)
        button_layout.setContentsMargins(QMargins(10, 10, 10, 10))
        button_layout.setSpacing(5)
        button_layout.setAlignment(Qt.AlignTop)

        self.questions_button = QPushButton('Questions', self)
        self.questions_button.setFixedHeight(40)
        self.questions_button.setFixedWidth(90)
        self.questions_button.clicked.connect(self.Questions)
        button_layout.addWidget(self.questions_button)

        self.tagq_button = QPushButton('TagQ', self)
        self.tagq_button.setFixedHeight(40)
        self.tagq_button.setFixedWidth(90)
        self.tagq_button.clicked.connect(lambda: self.TagQ(mode=True))
        button_layout.addWidget(self.tagq_button)

        self.cursewords_button = QPushButton('Curse Words', self)
        self.cursewords_button.setFixedHeight(40)
        self.cursewords_button.setFixedWidth(90)
        self.cursewords_button.clicked.connect(self.CurseWords)
        button_layout.addWidget(self.cursewords_button)

        self.panel_frame = QFrame(self)
        self.panel_frame.setStyleSheet("background-color: #F0F0F0;")
        self.panel_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        button_layout.addWidget(self.panel_frame)

        self.control_frame.setFixedWidth(100)

        font = QFont("Helvetica", 14)
        self.text_editor.setFont(font)

        self.text_editor.setStyleSheet("background-color: #ffffff;")

        self.text_editor.setUndoRedoEnabled(True)

        self.text_editor.setLineWrapMode(QTextEdit.NoWrap)

        self.highlighter = SyntaxHighlighter(self.text_editor.document())

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        edit_menu = menu_bar.addMenu('Edit')

        new_file_action = QAction('New', self)
        new_file_action.setShortcut('Ctrl+N')
        new_file_action.triggered.connect(self.new_file)
        file_menu.addAction(new_file_action)

        open_file_action = QAction('Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction('Save', self)
        save_file_action.setShortcut('Ctrl+S')
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        save_as_file_action = QAction('Save As', self)
        save_as_file_action.setShortcut('Ctrl+Shift+S')
        save_as_file_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_file_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(exit_action)

        cut_action = QAction('Cut', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(self.text_editor.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.text_editor.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.text_editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.text_editor.redo)
        edit_menu.addAction(redo_action)

        self.text_editor.textChanged.connect(self.on_text_changed)

        self.text_editor.modificationChanged.connect(self.on_modification_changed)

        self.show()

        screen_geometry = QApplication.desktop().availableGeometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) / 2
        y = (screen_geometry.height() - window_geometry.height()) / 2
        self.move(int(x), int(y))


    def on_modification_changed(self):
        self.update_undo_redo_status()


    def update_undo_redo_status(self):
        if not self.ignore_undo_redo_update:
            can_undo = self.text_editor.document().isUndoAvailable()
            can_redo = self.text_editor.document().isRedoAvailable()
            undo_action = self.findChild(QAction, 'undo_action')
            redo_action = self.findChild(QAction, 'redo_action')
            undo_action.setEnabled(can_undo)
            redo_action.setEnabled(can_redo)


    def update(self, mode=True):
        if mode:
            self.text_editor.setPlainText(self.text)
        self.highlighter.rehighlight()
        

    def on_text_changed(self):
        if self.text_editor.document().isModified():
            self.setWindowTitle(f'EnTagger ### {self.file_name}*')
        else:
            self.setWindowTitle(self.title)


    def new_file(self):
        self.text = ''
        self.text_editor.setPlainText(self.text)
        self.title = f'EnTagger ### {self.file_name}'
        self.setWindowTitle(self.title)
        self.open_status_name = False


    def replace_punc(self):
        self.text = re.sub(r'[‘’‚‛“”„‟′″‴‵‶‷]', '\'', self.text)
        self.text = re.sub(r'[‐‒–—―]', '-', self.text)
        if self.text.find('‥'):
            self.text = self.text.replace('‥', '..')
        if self.text.find('…'):
            self.text = self.text.replace('…', '...')
        if self.text.find('⁇'):
            self.text = self.text.replace('⁇', '??')
        if self.text.find('⁈'):
            self.text = self.text.replace('⁈', '?!')
        if self.text.find('⁉'):
            self.text = self.text.replace('⁉', '!?')

    def paste(self):
        self.text_editor.paste()
        self.text = self.text_editor.toPlainText()
        self.replace_punc()
        self.update()


    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Text files (*.txt)')

        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.text = file.read()
                self.replace_punc()
                self.file_name = file_name.split('/')[-1].replace('.txt', '')
                self.open_status_name = file_name
            self.title = f'EnTagger ### {self.file_name}'
            self.setWindowTitle(self.title)
            self.update()


    def save_file(self):
        if self.open_status_name:
            with open(self.open_status_name, 'w') as file:
                file.write(self.text_editor.toPlainText())
            self.title = f'EnTagger ### {self.file_name}'
            self.setWindowTitle(self.title)
        else:
            self.save_as_file()


    def save_as_file(self):
        default_file_name = f'{self.file_name}_is_tagged'
        downloads_folder = os.path.expanduser("~/Downloads")
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save file', os.path.join(downloads_folder, default_file_name), 'Text files (*.txt)')
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.text_editor.toPlainText())
            self.title = f'EnTagger ### {self.file_name}'
            self.setWindowTitle(self.title)


    def Questions(self):
        self.ignore_undo_redo_update = True
        cursor = self.text_editor.textCursor()
        cursor.beginEditBlock()
        self.text = self.text_editor.toPlainText()
        if '_Ques_' not in self.text:
            if '_TQ_' in self.text:
                self.text = re.sub(r'(\?)(?!_TQ_)', '?_Ques_', self.text)
            else:
                self.TagQ(mode=False)
                self.text = re.sub(r'(\?)(?!_TQ_)', '?_Ques_', self.text)
                self.text = self.text.replace('_TQ_', '')

            if "?_Ques_\'" in self.text:
                self.text = self.text.replace("?_Ques_\'", "\'?_HandCheck_")
            self.update()
        else:
            self.text = self.text.replace('_Ques_', '')
            self.update()
        cursor.endEditBlock()
        self.text_editor.document().setModified(True)
        self.text_editor.modificationChanged.emit()
        self.ignore_undo_redo_update = False


    def CurseWords(self):
        self.text = self.text_editor.toPlainText()
        if '_CW_' not in self.text:
            with open('curse words.txt') as f:
                words = f.read().split('\n')
            for x in words:
                if x not in [' ', '', '\t', '\n', '  ']:
                    self.text = re.sub(r'\b' + re.escape(x) + r'\b', f'{x}_CW_', self.text)
                    tmp = x[0].upper() + x[1:]
                    self.text = re.sub(r'\b' + re.escape(tmp) + r'\b', f'{tmp}_CW_', self.text)
            self.update()
        else:
            self.text = self.text.replace('_CW_', '')
            self.update()


    def TagQ(self, mode=True):
        self.text = self.text_editor.toPlainText()

        if '_TQ_' not in self.text:
            sentences = re.findall(r'(?s)([^\...\!\?\v\f]+[\...\!\?]+|[^\...\!\?\v\f]+$)', self.text)
            for sentence in sentences:
                if '?' in sentence:
                    parts_of_sentence = re.split(r'([,-])', sentence)
                    tmp = []
                    for part in parts_of_sentence:
                        if part == '\n' or part == ',':
                            tmp[-1] += part
                        else:
                            tmp += [part]
                    parts_of_sentence = tmp
                    if len(parts_of_sentence) != 1:

                        grammar_dict = {
                            'a': ['are', 'am'],
                            'c': ['can', 'could'],
                            'd': ['does', 'do', 'did'],
                            'h': ['has', 'have', 'had'],
                            'i': ['is', 'innit'],
                            'm': ['must', 'may'],
                            's': ['should', 'shall', "shan't"],
                            'w': ['was', 'were', 'will', 'would', "won't"]
                        }

                        extras_dict = {
                            ' ': [r'\s'],
                            'n': [r"n't\s"]
                        }

                        not_dict = {
                            ' ': [r'\snot\s']
                        }

                        pronouns_dict = {
                            'h': ['he'],
                            'i': ['I', 'it'],
                            't': ['they'],
                            's': ['she'],
                            'w': ['we'],
                            'y': ['you']
                        }

                        def check_tail(part, pattern, grammars):
                            try:
                                end = re.search(pattern, part).end()
                                for i in range(len(grammars)):
                                    grammar = grammars[i]
                                    for part_grammar in grammar[part[end].lower()]:
                                        extra = r'[\?\,]' if i == 2 else ''
                                        if re.search(pattern + part_grammar + extra, part):
                                            pattern += part_grammar + extra
                                            end = re.search(pattern, part).end()
                                            if i == 2:
                                                return True
                            except KeyError:
                                return False

                        for i in range(-1, -3, -1):
                            part = parts_of_sentence[i]
                            gap = re.findall(r'\s', part)
                            start = len(gap[0])
                            pattern = gap[0]
                            if len(gap) == 2:
                                if check_tail(part, pattern, [grammar_dict, extras_dict, pronouns_dict]):
                                    self.text = self.text.replace(sentence, sentence + '_TQ_')
                                    break
                                else:
                                    try:
                                        for pronoun in pronouns_dict[part[start]]:
                                            if re.search(r'\s' + pronoun + r'\s', part) and re.search(r'[\?\,]', part):
                                                self.text = self.text.replace(sentence, sentence + '_TQ_')
                                                break
                                        break
                                    except KeyError:
                                        pass

                            elif len(gap) == 3:
                                if check_tail(part, pattern, [grammar_dict, not_dict, pronouns_dict]):
                                    self.text = self.text.replace(sentence, sentence + '_TQ_')
                                    break
                                else:
                                    pass

                            elif len(gap) == 1:
                                if re.search(r'\sOK?', part):
                                    self.text = self.text.replace(sentence, sentence + '_TQ_')
                                    break
                                elif not re.search(r'[A-Z]', part) and re.search(r'[\?\,]', part):
                                    self.text = self.text.replace(sentence, sentence + '_TQ_')
                                    break

            self.text = re.sub(r'(_TQ_)+', '_TQ_', self.text)
            if mode:
                self.update()

        else:
            self.text = self.text.replace('_TQ_', '')
            self.update()


class TextEdit(QTextEdit):
    modificationChanged = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)


    def undo(self):
        self.document().undo()


    def redo(self):
        self.document().redo()


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)


    def highlightBlock(self, text):
        self.highlight_tags(text, 'TQ', QColor('yellow'))
        self.highlight_tags(text, 'CW', QColor('blue'))
        self.highlight_tags(text, 'Ques', QColor('green'))
        self.highlight_tags(text, 'HandCheck', QColor('red'))


    def highlight_tags(self, text, tag, color):
        pattern = f'_{tag}_'
        format = QTextCharFormat()
        format.setBackground(color)

        index = 0
        while True:
            index = text.find(pattern, index)
            if index == -1:
                break
            length = len(pattern)
            self.setFormat(index, length, format)
            index += length



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EnTagger()
    sys.exit(app.exec_())




