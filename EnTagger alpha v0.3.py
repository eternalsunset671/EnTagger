from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import *
import tkinter as tk
import tkinter.font as tkFont

import re

#форматировать под один стиль пунктуацию и непечатные символы а также пересмотреть регулярку и проверить как она отрабавтывает на реальном корпусе
#ключи в словарях содержат пробелы но не учитывают других символов
#undo redo

class App(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        self.title('EnTagger')
        self.geometry('800x500')

        bg_color = '#f0f0f0' # Light gray
        text_bg_color = '#ffffff' # White
        button_bg_color = '#d9d9d9' # Darker gray
        button_fg_color = '#000000' # Black
        button_hover_bg_color = '#c0c0c0' # Lighter gray

        self.configure(bg=bg_color)

        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=0)

        self.text_editor = ScrolledText(self, wrap=tk.WORD, bg=text_bg_color)
        self.text_editor.grid(column=0, row=0, sticky='nsew')

        self.text = ''
        self.file_name = ''

        self.control_frame = tk.Frame(self, relief=tk.RAISED, bd=2, bg=bg_color)
        self.control_frame.grid(column=1, row=0, sticky='ns')

        self.open_button = tk.Button(self.control_frame, text='Open file', command=self.open_file, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.open_button.grid(column=0, row=0, sticky='ew', padx=(10, 0), pady=(10, 0))

        self.Questions_button = tk.Button(self.control_frame, text='Questions', command=self.Questions, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.Questions_button.grid(column=0, row=1, sticky='ew', padx=(10, 0), pady=(10, 0))

        self.TagQ_button = tk.Button(self.control_frame, text='TagQ', command=self.TagQ, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.TagQ_button.grid(column=0, row=2, sticky='ew', padx=(10, 0), pady=(10, 0))

        self.CurseWords_button = tk.Button(self.control_frame, text='Curse Words', command=self.CurseWords, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.CurseWords_button.grid(column=0, row=3, sticky='ew', padx=(10, 0), pady=(10, 0))

        self.save_button = tk.Button(self.control_frame, text='Save file', command=self.save_file, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.save_button.grid(column=0, row=4, sticky='ew', padx=(10, 0), pady=(10, 0))

        for button in (self.open_button, self.TagQ_button, self.CurseWords_button, self.save_button, self.Questions_button):
            button.config(font=tkFont.Font(family='Helvetica', size=12))

        self.text_editor.tag_configure('TQ', background='yellow')
        self.text_editor.tag_configure('Ques', background='green')
        self.text_editor.tag_configure('HandCheck', background='red')
        self.text_editor.tag_configure('CW', background='blue')


    def update(self):
        self.highlight_tags('TQ')
        self.highlight_tags('CW')
        self.highlight_tags('Ques')
        self.highlight_tags('HandCheck')


    def highlight_tags(self, tag):
        pattern = f'_{tag}_'
        index = '1.0'
        while True:
            index = self.text_editor.search(pattern, index, stopindex=END)
            if not index:
                break
            end_index = f'{index}+{len(pattern)}c'
            self.text_editor.tag_add(tag, index, end_index)
            index = end_index


    def open_file(self):
        filepath = filedialog.askopenfilename(defaultextension='txt')
        self.file_name = filepath.split('/')[-1].replace('.txt', '')
        if filepath != '':
            with open(filepath, 'r', encoding='utf-8') as file:
                self.text = file.read()
                self.text_editor.delete('1.0', END)
                self.text_editor.insert('1.0', self.text)
            self.CurseWords_button.config(state='normal')
            self.Questions_button.config(state='normal')
            self.TagQ_button.config(state='normal')
            self.undo_stack = []
            self.redo_stack = []


    def save_file(self):
        filepath = filedialog.asksaveasfilename(
        filetypes=[('txt file', '.txt')],
        defaultextension='.txt',
        initialdir='F:\\data\\',
        initialfile=f'{self.file_name}_tagged',
        confirmoverwrite=False,
    )
        if filepath != '':
            self.text = self.text_editor.get('1.0', END)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(self.text)
            self.text = ''


    def Questions(self):
        self.text = self.text_editor.get('1.0', tk.END)
        if re.search('_TQ_', self.text):
            self.text = re.sub(r'(\?)(?!_TQ_)', '?_Ques_', self.text)
        else:
            self.TagQ(mode=False)
            self.text = re.sub(r'(\?)(?!_TQ_)', '?_Ques_', self.text)
            self.text = re.sub(r'_TQ_', '', self.text)

        if self.text.find('?_Ques_\'') != -1:
            self.text = self.text.replace('?_Ques_\'', '\'?_HandCheck_')
        self.text_editor.delete('1.0', END)
        self.text_editor.insert('1.0', self.text)
        self.Questions_button.config(state='disabled')
        self.update()
        

    def CurseWords(self):
        self.text = self.text_editor.get('1.0', tk.END)
        with open('curse words.txt') as f:
            words = f.read().split('\n')
        for x in words:
            if x not in [' ', '', '\t', '\n', '  ']:
                self.text = re.sub(r'\b' + re.escape(x) + r'\b', f'{x}_CW_', self.text)
                tmp = x[0].upper() + x[1:]
                self.text = re.sub(r'\b' + re.escape(tmp) + r'\b', f'{tmp}_CW_', self.text)
        self.text_editor.delete('1.0', END)
        self.text_editor.insert('1.0', self.text)
        self.CurseWords_button.config(state='disabled')
        self.update()


    def TagQ(self, mode=True):
        self.text = self.text_editor.get('1.0', tk.END)
        sentences = re.findall(r'(?s)([^\...\!\?\v\f]+[\...\!\?]+|[^\...\!\?\v\f]+$)', self.text)
        for sentence in sentences:
            if re.search(r'\?', sentence):
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
                        's': ['should', 'shall', 'shan\'t'],
                        'w': ['was', 'were', 'will', 'would', 'won\'t']
                        }

                    extras_dict = {
                        ' ': [r'\s'],
                        'n': [r'n\'t\s']
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
                                    extra = r'[\?\,]' if i == 2 else  ''
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
            self.text_editor.delete('1.0', END)
            self.text_editor.insert('1.0', self.text)
            self.TagQ_button.config(state='disabled')
            self.update()


if __name__ == '__main__':
    app = App()
    app.mainloop()







#for gram in grammar_dict[part[start]]:
#    if part.find(gram) != -1:
#        pattern += gram
#        match = re.search(pattern, part)
#        print(pattern, parts_of_sentence)
#        for ex in extras_dict[part[match.end()]]:
#            if re.search(pattern + ex, part):
#                pattern += ex
#                match = re.search(pattern, part)
#                for pronoun in pronouns_dict[part[match.end()].lower()]:
#                    if re.search(pattern + pronoun + r'[\?\,]', part):
#                        pattern += pronoun + r'[\?\,]'
#                        self.text = self.text.replace(sentence, sentence + '_TQ_')
#                        break
#                break
#        break